# 🚀 Semantic Search for E-commerce using Data Lakehouse Architecture

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Databricks](https://img.shields.io/badge/Platform-Databricks-orange.svg)](https://databricks.com/)
[![Apache Spark](https://img.shields.io/badge/Engine-Apache_Spark-red.svg)](https://spark.apache.org/)
[![FAISS](https://img.shields.io/badge/Library-FAISS-green.svg)](https://github.com/facebookresearch/faiss)

## 📌 Overview
This project proposes an end-to-end **Semantic Search system for E-commerce** built on top of a modern **Data Lakehouse Architecture**.

Unlike traditional **Keyword Search**, the system leverages:
- Vector Embeddings
- Semantic Retrieval
- Metadata-aware Ranking
- FAISS Vector Indexing

to better understand user intent in natural language queries.

The entire pipeline is implemented using:
- Apache Spark
- Delta Lake
- Sentence-BERT
- FAISS
- Databricks

---

## 🏗 Architecture

```text
Raw Data
   ↓
Bronze Layer
   ↓
Silver Layer
(Data Cleaning & Standardization)
   ↓
Gold Layer
(Embedding + Semantic Enrichment)
   ↓
FAISS Vector Index
   ↓
Semantic Retrieval
   ↓
Hybrid Ranking
   ↓
Search Results
```

---

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| Data Processing | Apache Spark |
| Data Platform | Databricks |
| Storage Layer | Delta Lake |
| Language | Python |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Search | FAISS |
| UI | ipywidgets |

---

## 🚀 Installation

### Install dependencies

```bash
pip install sentence-transformers faiss-cpu pyspark delta-spark ipywidgets
```

### Initialize Spark Session

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SemanticSearchLakehouse") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()
```

### Initialize FAISS Index

```python
import faiss

index = faiss.IndexFlatIP(384)
index.add(embeddings)
```

### Example Query

```python
results = search_engine.search(
    query="affordable gaming laptop",
    top_k=5
)
```

---

## 🔍 System Workflow

### 1. Data Ingestion
- Raw Amazon product data is ingested into Bronze Layer.

### 2. Data Cleaning
Silver Layer performs:
- Regex cleaning
- Missing value handling
- Rating normalization
- Price normalization
- Deduplication

### 3. Semantic Enrichment
Gold Layer performs:
- Combined text generation
- Sentence-BERT embeddings
- Metadata enrichment
- Vector indexing

### 4. Semantic Retrieval
FAISS is used for:
- Nearest Neighbor Search
- Fast vector similarity retrieval

### 5. Hybrid Ranking
Final ranking combines:
- Semantic similarity
- Product ratings
- Price/value signals

---

## 📊 Experimental Results

| Metric | Semantic Search | Keyword Search |
|---|---|---|
| Average Precision@5 | **0.820** | 0.500 |
| Average MRR | **0.825** | 0.631 |
| Average Latency | **1.88 ms** | 14.24 ms |
| Speed Improvement | **7.6x faster** | Baseline |

### Win/Loss Summary

| Metric | Semantic Wins | Keyword Wins |
|---|---|---|
| Precision@5 | 7/10 | 3/10 |
| MRR | 6/10 | 4/10 |

---

## 💡 Key Contributions

- End-to-end Semantic Search pipeline
- Data Lakehouse-based architecture
- Metadata-aware ranking
- FAISS latency optimization
- Scalable Medallion Architecture

---

## ⚠ Limitations

- No domain-specific fine-tuning
- English-only queries
- No advanced ANN indexing
- No user feedback loop

---

## 🔮 Future Work

- Hybrid Search
- Personalized Search
- Real-time streaming pipeline
- LLM-based Conversational Search
- Vector Databases (Milvus, Pinecone)

---

## 👨‍💻 Nhóm sinh viên thực hiện: Nhóm 3

| Họ và tên | Student ID |
|---|---|
| Nguyễn Vũ Thanh Giang| 31231026898 |
| Nguyễn Vĩnh Hoàng | 31231024973 |
| Hoàng Hữu Hưng | 31231027485 |
| Nguyễn Đình Gia Huy | 31231026899 |
| Nguyễn Thành Huy | 31231025985 |
---

## 👨‍🏫 Giảng viên hướng dẫn

- TS. Nguyễn An Tế

---

## 📚 References

- Sentence-BERT (Reimers & Gurevych, 2019)
- FAISS (Johnson et al., 2017)
- Data Lakehouse (Armbrust et al., 2020)
- Manning et al. — Information Retrieval
