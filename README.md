# 🚀 E-Commerce Semantic Search Engine with Data Lakehouse Architecture

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
   pip install sentence-transformers faiss-cpu
