"""
Local (no-Databricks) reproduction of the Bronze -> Silver -> Gold pipeline and the search evaluation
in Execution.ipynb, using pandas instead of Spark. Same cleaning rules, same Gold sampling, same model.

Evaluates three methods on the notebook's 10 intent queries:
  - Keyword Search (baseline)
  - Semantic Search (FAISS, cosine)
  - Hybrid Search (semantic top-50 re-ranked with a popularity signal)
and benchmarks FAISS vs. NumPy brute force on the REAL Gold embeddings (same metric, many queries).

Usage: pip install kagglehub sentence-transformers faiss-cpu pandas && python local_eval.py
"""
import os
import time
import json
import numpy as np
import pandas as pd
import faiss
import kagglehub
from sentence_transformers import SentenceTransformer

SEED = 42
HYBRID_WEIGHT = 0.15     # fixed a priori (not tuned on the test queries)
HYBRID_CANDIDATES = 50
K = 5
CACHE = "gold_vectors_cache.npy"

# ---------------- Bronze ----------------
path = kagglehub.dataset_download("lokeshparab/amazon-products-dataset")
cols = ["name", "main_category", "sub_category", "image", "link",
        "ratings", "no_of_ratings", "discount_price", "actual_price"]
frames = []
for root, _, files in os.walk(path):
    for f in files:
        if f.endswith(".csv"):
            t = pd.read_csv(os.path.join(root, f), dtype=str, on_bad_lines="skip", low_memory=False)
            for c in cols:
                if c not in t.columns:
                    t[c] = ""
            frames.append(t[cols])
bronze = pd.concat(frames, ignore_index=True).fillna("").astype(str)

# ---------------- Silver (same rules as notebook cell 2) ----------------
s = bronze[bronze["name"] != ""].copy()
s["_p"], s["_r"] = s["actual_price"].str.len(), s["ratings"].str.len()
s = s.sort_values(["name", "_p", "_r"], ascending=[True, False, False]).drop_duplicates("name")
r = pd.to_numeric(s["ratings"].str.extract(r"([0-9]+\.?[0-9]*)")[0], errors="coerce")
s["ratings_final"] = r.where(r.between(1, 5), 4.0).round(1)
p = pd.to_numeric(s["actual_price"].str.replace(r"[^0-9.]", "", regex=True), errors="coerce")
s["price_final"] = p.where((p > 0) & (p < 1_000_000), 1499.0)
s["no_of_ratings"] = pd.to_numeric(s["no_of_ratings"].str.replace(r"[^0-9]", "", regex=True),
                                   errors="coerce").fillna(0).astype(int)
price_tier = np.select([p < 500, p < 5000, p >= 5000], ["budget", "mid-range", "premium"], "unknown price")
rating_tier = np.select([s["ratings_final"] >= 4.5, s["ratings_final"] >= 3.5],
                        ["top rated", "well rated"], "average rated")
s["combined_text"] = (s["name"] + " | " + s["main_category"] + " | " + s["sub_category"]
                      + " | " + price_tier + " | " + rating_tier).str.strip()
silver = s[["name", "main_category", "sub_category", "ratings_final", "no_of_ratings",
            "price_final", "combined_text"]].reset_index(drop=True)

# ---------------- Gold (same sampling as notebook cell 4) ----------------
silver["pop"] = silver["ratings_final"] * np.log1p(silver["no_of_ratings"])
top = silver.sort_values("pop", ascending=False).groupby("main_category").head(500)
rest = silver[~silver["name"].isin(top["name"])].sample(frac=0.05, random_state=SEED)
gold = pd.concat([top, rest]).drop_duplicates("name").sort_values("name").head(30000).reset_index(drop=True)
print(f"Pipeline: Bronze ({len(bronze):,}) -> Silver ({len(silver):,}) -> Gold ({len(gold):,})")

model = SentenceTransformer("all-MiniLM-L6-v2")
if os.path.exists(CACHE) and len(np.load(CACHE)) == len(gold):
    vecs = np.load(CACHE).astype("float32")
else:
    vecs = model.encode(gold["combined_text"].tolist(), batch_size=64, show_progress_bar=True,
                        convert_to_numpy=True).astype("float32")
    np.save(CACHE, vecs)
faiss.normalize_L2(vecs)
index = faiss.IndexFlatIP(vecs.shape[1])
index.add(vecs)

# ---------------- search methods ----------------
def encode(q):
    v = model.encode([q]).astype("float32")
    faiss.normalize_L2(v)
    return v

def semantic(q, k=10):
    sc, ix = index.search(encode(q), k)
    out = gold.iloc[ix[0]].copy()
    out["score"] = sc[0]
    return out

def hybrid(q, k=10):
    cand = semantic(q, HYBRID_CANDIDATES)
    pop = cand["pop"]
    pop_n = (pop - pop.min()) / (pop.max() - pop.min() + 1e-9)
    cand["score"] = cand["score"] + HYBRID_WEIGHT * pop_n
    return cand.sort_values("score", ascending=False).head(k)

def keyword(q, k=10):
    kws = q.lower().split()
    d = gold.copy()
    d["score"] = d["name"].str.lower().apply(lambda x: sum(kw in x for kw in kws))
    return d.sort_values(["score", "ratings_final"], ascending=[False, False]).head(k)

TESTS = [
    ("low priced device for online classes", ["laptop", "tablet", "webcam", "headphone", "lenovo", "asus"]),
    ("protection for expensive smartphones", ["case", "cover", "screen", "guard", "tempered"]),
    ("equipment for brewing coffee at home", ["maker", "machine", "grinder", "press", "filter"]),
    ("professional tools for vlogging", ["tripod", "ring", "light", "mic", "microphone", "gimbal"]),
    ("apparel for winter sports", ["jacket", "thermal", "glove", "sweater", "hoodie"]),
    ("storage solution for high res photos", ["hard", "drive", "ssd", "memory", "card", "sandisk"]),
    ("cooking appliance for healthy oil free meals", ["air", "fryer", "steamer", "grill"]),
    ("noise cancelling gear for travelers", ["headphone", "earbud", "sony", "bose", "silence"]),
    ("device to turn tv into smart tv", ["fire", "stick", "chromecast", "box", "mi"]),
    ("ergonomic gear for office workers", ["chair", "mouse", "keyboard", "stand", "support"]),
]

def hit(name, kws):
    return any(kw in str(name).lower() for kw in kws)

def evaluate(fn):
    p, m = [], []
    for q, kws in TESTS:
        names = fn(q)["name"].tolist()
        p.append(sum(hit(n, kws) for n in names[:K]) / K)
        m.append(next((1 / i for i, n in enumerate(names, 1) if hit(n, kws)), 0.0))
    return float(np.mean(p)), float(np.mean(m))

results = {}
print(f"\n{'Method':<28}{'Precision@5':>12}{'MRR':>8}")
for name, fn in [("Keyword Search (baseline)", keyword), ("Semantic Search (FAISS)", semantic),
                 (f"Hybrid (w={HYBRID_WEIGHT})", hybrid)]:
    results[name] = evaluate(fn)
    print(f"{name:<28}{results[name][0]:>12.3f}{results[name][1]:>8.3f}")

# ---------------- latency benchmark on real Gold vectors ----------------
queries = np.vstack([encode(q) for q, _ in TESTS] * 10)          # 100 real queries
for v in queries[:5]:
    index.search(v.reshape(1, -1), 5)                              # warm-up
def bench(fn):
    t = []
    for v in queries:
        t0 = time.perf_counter(); fn(v.reshape(1, -1)); t.append((time.perf_counter() - t0) * 1000)
    return float(np.median(t))
bf = bench(lambda v: np.argsort(-(vecs @ v.T).ravel())[:5])
fa = bench(lambda v: index.search(v, 5))
print(f"\nSearch latency over {index.ntotal:,} real vectors (median of 100 queries): "
      f"NumPy brute force {bf:.2f} ms | FAISS IndexFlatIP {fa:.2f} ms")

json.dump({"gold_size": int(index.ntotal), "silver_size": int(len(silver)), "bronze_size": int(len(bronze)),
           "metrics": {k: {"precision@5": v[0], "mrr": v[1]} for k, v in results.items()},
           "latency_ms": {"numpy_bruteforce": bf, "faiss_flat_ip": fa}},
          open("local_eval_results.json", "w"), indent=2)
print("Saved local_eval_results.json")
