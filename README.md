# 🚀 Nâng cao hiệu quả tìm kiếm thương mại điện tử bằng truy xuất ngữ nghĩa: Thiết kế hệ thống dựa trên kiến trúc Data Lakehouse và đánh giá thực nghiệm 

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Databricks](https://img.shields.io/badge/Platform-Databricks-orange.svg)](https://databricks.com/)
[![Apache Spark](https://img.shields.io/badge/Engine-Apache_Spark-red.svg)](https://spark.apache.org/)
[![FAISS](https://img.shields.io/badge/Library-FAISS-green.svg)](https://github.com/facebookresearch/faiss)

## 📌 Tổng quan dự án (Project Overview)
Dự án này tập trung vào việc xây dựng một hệ thống tìm kiếm sản phẩm thông minh, vượt xa giới hạn của phương pháp khớp từ khóa (**Keyword Search**) truyền thống. Bằng cách ứng dụng **Truy xuất ngữ nghĩa (Semantic Search)**, hệ thống có khả năng thấu hiểu ý định người dùng thông qua ngôn ngữ tự nhiên.

Hệ thống được triển khai trên nền tảng **Data Lakehouse** hiện đại, kết hợp sức mạnh xử lý dữ liệu lớn của Spark và khả năng tìm kiếm vector hiệu năng cao của FAISS.

## 🏗 Kiến trúc dữ liệu (Medallion Architecture)
Dữ liệu được tổ chức theo tiêu chuẩn **Medallion Architecture** trên Delta Lake:
- **Bronze Layer:** Lưu trữ dữ liệu thô (Raw Data) được Ingest từ các nguồn tập tin.
- **Silver Layer:** Quy trình làm sạch, khử nhiễu và chuẩn hóa thuộc tính sản phẩm.
- **Gold Layer:** Tầng "giàu ngữ nghĩa" (Semantic Enrichment) nơi thực hiện tạo Vector Embeddings và lưu trữ chỉ mục (Index) phục vụ truy xuất.

## 🛠 Công nghệ cốt lõi (Tech Stack)
- **Data Engineering:** Apache Spark, Delta Lake, Databricks.
- **Machine Learning:** `Sentence-Transformers` (Model: `all-MiniLM-L6-v2`).
- **Vector Search:** `FAISS` (Facebook AI Research).
- **Frontend UI:** `ipywidgets` phục vụ tương tác trực tiếp trên Notebook.

## 📊 Chỉ số ấn tượng (Experimental Results)
Hệ thống đã đạt được các kết quả thực nghiệm vượt trội:
* **Hiệu năng:** Độ trễ truy vấn trung bình chỉ ~**2.18ms** (nhanh gấp 6.2 lần so với tìm kiếm tuyến tính).
* **Độ chính xác:** Chỉ số **Precision@5** đạt 80% trong các kịch bản thử nghiệm phức tạp.
* **Scalability:** Duy trì độ trễ < 10ms ngay cả khi quy mô dữ liệu đạt **100,000 sản phẩm**.

## 🚀 Hướng dẫn cài đặt (Setup Instruction)

1. **Chuẩn bị môi trường:** Triển khai trên Databricks Community hoặc Local Spark.
2. **Cài đặt thư viện:**
   ```bash
      pip install sentence-transformers faiss-cpu pyspark delta-spark ipywidgets
   ```

3. **Khởi tạo Spark Session với Delta Lake**
   ```python
   from pyspark.sql import SparkSession

   spark = SparkSession.builder \
       .appName("SemanticSearchLakehouse") \
       .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
       .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
       .getOrCreate()
   ```

4. **Chạy Pipeline xử lý dữ liệu**
   - Bronze → Silver → Gold
   - Cleaning → Embedding → Indexing

5. **Khởi tạo Vector Index**
   ```python
   import faiss

   index = faiss.IndexFlatIP(384)
   index.add(embeddings)
   ```

6. **Thực hiện truy vấn**
   ```python
   results = search_engine.search(
       query="affordable gaming laptop",
       top_k=5
   )
   ```

---

## 🔍 Cơ chế hoạt động của hệ thống (How It Works)

### 1️⃣ Data Ingestion
Dữ liệu sản phẩm Amazon được ingest vào tầng Bronze dưới dạng dữ liệu thô nhằm đảm bảo khả năng truy xuất nguồn gốc và tái xử lý.

### 2️⃣ Data Cleaning & Standardization
Pipeline tại tầng Silver thực hiện:
- Chuẩn hóa giá và ratings
- Xử lý dữ liệu thiếu
- Regex cleaning
- Deduplication bằng Window Functions

### 3️⃣ Semantic Enrichment
Tại tầng Gold:
- Product title + metadata được kết hợp thành `combined_text`
- Văn bản được chuyển thành vector embedding 384 chiều bằng Sentence-BERT
- Metadata như:
  - price tier
  - rating tier
  - category
  được enrich trực tiếp vào biểu diễn ngữ nghĩa

### 4️⃣ Vector Retrieval
FAISS được sử dụng để:
- Index vector embeddings
- Thực hiện nearest neighbor search
- Tăng tốc truy vấn semantic similarity

### 5️⃣ Hybrid Ranking
Kết quả cuối cùng được xếp hạng dựa trên:
- Semantic similarity
- Product ratings
- Price/value signals

Trong trường hợp metadata thiếu hoặc không hợp lệ, hệ thống áp dụng cơ chế fallback giá nhằm đảm bảo tính ổn định của pipeline xếp hạng.

---

## 📈 Các chỉ số đánh giá (Evaluation Metrics)

### Precision@K
Đo lường tỷ lệ kết quả liên quan trong top-K sản phẩm đầu tiên.

:contentReference[oaicite:0]{index=0}

### Mean Reciprocal Rank (MRR)
Đánh giá vị trí xuất hiện của kết quả đúng đầu tiên.

:contentReference[oaicite:1]{index=1}

---

## 🧪 Kết quả thực nghiệm (Benchmarking)

| Metric | Semantic Search | Keyword Search |
|---|---|---|
| Average Precision@5 | **0.820** | 0.500 |
| Average MRR | **0.825** | 0.631 |
| Avg Latency | **2.18ms** | 13.62ms |
| Scalability | Stable <10ms | Linear slowdown |

### Một số truy vấn tiêu biểu:
| Query | Semantic Search | Keyword Search |
|---|---|---|
| portable computer for gaming | ✅ Hiểu là gaming laptop | ❌ Match từ khóa rời rạc |
| affordable wireless audio | ✅ Ưu tiên wireless headphones | ⚠ Kết quả thiếu ngữ cảnh |
| cordless pointing device | ⚠ Semantic drift | ✅ Match keyword “device” |

---

## 💡 Đóng góp chính của dự án (Key Contributions)

### ✅ Về học thuật
- Kết hợp Information Retrieval + Machine Learning + Data Engineering trong một pipeline thống nhất.
- Chứng minh hiệu quả của Semantic Search trong môi trường E-commerce thực tế.
- Phân tích trade-off giữa Keyword Search và Semantic Search.

### ✅ Về kỹ thuật
- Xây dựng end-to-end Semantic Search pipeline trên Data Lakehouse.
- Tích hợp metadata-aware ranking.
- Tối ưu latency bằng FAISS Index.
- Thiết kế pipeline scalable theo Medallion Architecture.

### ✅ Về ứng dụng thực tiễn
- Cải thiện trải nghiệm tìm kiếm sản phẩm.
- Hỗ trợ truy vấn ngôn ngữ tự nhiên.
- Tăng khả năng hiểu user intent trong E-commerce systems.

---

## ⚠ Hạn chế hiện tại (Limitations)

- Chưa fine-tune embedding model theo domain thương mại điện tử.
- Chưa triển khai ANN index nâng cao như IVF/PQ/HNSW.
- Truy vấn hiện tại chủ yếu bằng tiếng Anh.
- Chưa tích hợp feedback loop từ hành vi người dùng.

---

## 🔮 Hướng phát triển tương lai (Future Work)

Trong tương lai, hệ thống có thể được mở rộng theo các hướng:
- Hybrid Search (Keyword + Semantic).
- Fine-tuning embedding model theo domain E-commerce.
- Personalized Search dựa trên user behavior.
- Real-time streaming pipeline.
- Triển khai Vector Database chuyên dụng như Milvus hoặc Pinecone.
- Tích hợp Large Language Models (LLMs) cho Conversational Search.

---

## 👨‍💻 Authors
Nhóm thực hiện:
- [Tên thành viên 1]
- [Tên thành viên 2]
- [Tên thành viên 3]

Giảng viên hướng dẫn:
- [Tên GVHD]

---

## 📚 References
- Reimers & Gurevych (2019) — Sentence-BERT
- Armbrust et al. (2020) — Data Lakehouse
- Johnson et al. (2017) — FAISS
- Manning et al. (2008) — Information Retrieval
- Databricks Documentation
- Hugging Face Transformers

---

## ⭐ Project Highlights
✅ Semantic Search for E-commerce  
✅ Data Lakehouse Architecture  
✅ Vector Embeddings + FAISS  
✅ Metadata-aware Ranking  
✅ Real-time Retrieval  
✅ Scalable Data Engineering Pipeline
