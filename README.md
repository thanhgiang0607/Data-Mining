# 🚀 Nâng cao hiệu quả tìm kiếm thương mại điện tử bằng truy xuất ngữ nghĩa: Thiết kế hệ thống dựa trên kiến trúc Data Lakehouse và đánh giá thực nghiệm

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Databricks](https://img.shields.io/badge/Platform-Databricks-orange.svg)](https://databricks.com/)
[![Apache Spark](https://img.shields.io/badge/Engine-Apache_Spark-red.svg)](https://spark.apache.org/)
[![FAISS](https://img.shields.io/badge/Library-FAISS-green.svg)](https://github.com/facebookresearch/faiss)

---

## 📌 Tổng quan dự án

Dự án tập trung xây dựng hệ thống **Semantic Search cho thương mại điện tử** nhằm khắc phục hạn chế của phương pháp **Keyword Search** truyền thống.

Hệ thống sử dụng:
- Vector Embedding
- Semantic Retrieval
- Metadata-aware Ranking
- FAISS Vector Index

để cải thiện khả năng hiểu ý định người dùng thông qua truy vấn ngôn ngữ tự nhiên.

Toàn bộ pipeline được triển khai trên kiến trúc **Data Lakehouse** với:
- Apache Spark
- Delta Lake
- Databricks
- Sentence-BERT
- FAISS

---

## 🏗 Kiến trúc hệ thống

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

| Thành phần | Công nghệ |
|---|---|
| Data Processing | Apache Spark |
| Data Platform | Databricks |
| Storage Layer | Delta Lake |
| Ngôn ngữ lập trình | Python |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Search | FAISS |
| Frontend UI | ipywidgets |

---

## 🚀 Hướng dẫn cài đặt

### Cài đặt thư viện

```bash
pip install sentence-transformers faiss-cpu pyspark delta-spark ipywidgets
```

### Khởi tạo Spark Session

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SemanticSearchLakehouse") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()
```

### Khởi tạo FAISS Index

```python
import faiss

index = faiss.IndexFlatIP(384)
index.add(embeddings)
```

### Ví dụ truy vấn

```python
results = search_engine.search(
    query="affordable gaming laptop",
    top_k=5
)
```

---

## 🔍 Quy trình hoạt động

### 1. Data Ingestion
Dữ liệu sản phẩm Amazon được ingest vào tầng Bronze dưới dạng dữ liệu thô.

### 2. Data Cleaning
Tầng Silver thực hiện:
- Chuẩn hóa giá và ratings
- Xử lý dữ liệu thiếu
- Regex cleaning
- Deduplication

### 3. Semantic Enrichment
Tầng Gold thực hiện:
- Kết hợp metadata vào văn bản
- Sinh vector embedding bằng Sentence-BERT
- Semantic enrichment
- Tạo vector index

### 4. Semantic Retrieval
FAISS được sử dụng để:
- Index vector embeddings
- Tìm nearest neighbors
- Tăng tốc truy vấn semantic similarity

### 5. Hybrid Ranking
Kết quả cuối cùng được xếp hạng dựa trên:
- Semantic similarity
- Ratings
- Price/value signals

---

## 📊 Kết quả thực nghiệm

| Metric | Semantic Search | Keyword Search |
|---|---|---|
| Average Precision@5 | **0.540** | 0.240 |
| Average MRR | **0.695** | 0.370 |



---

## 💡 Đóng góp chính

- Xây dựng end-to-end Semantic Search pipeline
- Ứng dụng Data Lakehouse trong E-commerce Search
- Tích hợp Metadata-aware Ranking
- Tối ưu latency bằng FAISS
- Thiết kế pipeline scalable theo Medallion Architecture

---

## ⚠ Hạn chế

- Chưa fine-tune theo domain E-commerce
- Chưa hỗ trợ multilingual search
- Chưa triển khai ANN index nâng cao
- Chưa tích hợp user feedback loop

---

## 🔮 Hướng phát triển

- Hybrid Search
- Personalized Search
- Real-time Streaming Pipeline
- Conversational Search với LLMs
- Vector Database (Milvus, Pinecone)



---


