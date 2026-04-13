# Lab 1: First ML Product - Movie Rating Prediction API

## Overview

Build your first ML product - a Movie Rating Prediction API using collaborative filtering, REST API, and Docker containerization.

## Project Structure

```
ddm501-lab1-starter/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application (TODO)
│   ├── model.py          # ML model loading & prediction (TODO)
│   ├── schemas.py        # Pydantic models (TODO)
│   └── config.py         # Configuration
├── models/               # Saved ML models
├── tests/
│   ├── __init__.py
│   └── test_api.py       # Unit tests (TODO)
├── scripts/
│   └── train_model.py    # Model training script
├── Dockerfile            # (TODO)
├── docker-compose.yml    # (TODO)
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Git

## Quick Start

### 1. Clone and Setup

```bash
unzip ddm501-lab1-starter.zip
cd ddm501-lab1-starter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Train the Model

```bash
python scripts/train_model.py
```

This will download MovieLens 100K dataset and train an SVD model.

### 3. Run the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Predict
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "196", "movie_id": "242"}'
```

### 5. Run with Docker

```bash
docker-compose build
docker-compose up -d
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/predict` | Get rating prediction |
| GET | `/docs` | Swagger documentation |

## API Documentation

FastAPI automatically generates interactive Swagger documentation at `/docs`. You can access it at `http://localhost:8000/docs` when the API is running.

All endpoints include complete docstrings and the Pydantic models provide examples for request/response validation.

### Endpoints

#### Health Check
- **GET /health**
  
  Returns the health status of the API and whether the model is loaded.
  
  **Response Example:**
  ```json
  {
    "status": "healthy",
    "model_loaded": true
  }
  ```

#### Prediction
- **POST /predict**
  
  Predicts the movie rating for a single user-movie pair.
  
  **Request Body:**
  ```json
  {
    "user_id": "196",
    "movie_id": "242"
  }
  ```
  
  **Response Example:**
  ```json
  {
    "user_id": "196",
    "movie_id": "242",
    "predicted_rating": 4.2,
    "model_version": "1.0.0"
  }
  ```

#### Batch Prediction (Bonus)
- **POST /predict/batch**
  
  Predicts ratings for multiple user-movie pairs in a single request.
  
  **Request Body:**
  ```json
  {
    "predictions": [
      {"user_id": "196", "movie_id": "242"},
      {"user_id": "186", "movie_id": "302"}
    ]
  }
  ```
  
  **Response Example:**
  ```json
  {
    "predictions": [
      {
        "user_id": "196",
        "movie_id": "242",
        "predicted_rating": 4.2,
        "model_version": "1.0.0"
      },
      {
        "user_id": "186",
        "movie_id": "302",
        "predicted_rating": 3.8,
        "model_version": "1.0.0"
      }
    ],
    "total_count": 2
  }
  ```

#### Root
- **GET /**
  
  Returns basic API information including title, version, description, and links to docs and health endpoints.

#### Model Info
- **GET /model/info**
  
  Returns information about the loaded model, including version, type, and loading status.

## TODO Tasks

Complete the following files:

- [ ] `app/model.py` - Implement `load_model()`, `predict()`, `predict_batch()`
- [ ] `app/schemas.py` - Define Pydantic request/response models
- [ ] `app/main.py` - Implement `/predict` endpoint with error handling
- [ ] `Dockerfile` - Complete with health check
- [ ] `docker-compose.yml` - Configure services
- [ ] `tests/test_api.py` - Add edge case tests

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html
```

## Grading Rubric

| Criteria | Weight |
|----------|--------|
| Working ML Model | 25% |
| REST API | 25% |
| Docker Setup | 20% |
| Test Cases | 20% |
| Documentation | 10% |

## Submission

1. Complete all TODO tasks
2. Ensure all tests pass
3. Push to your GitHub repository
4. Submit the repository link

## Movie Rating Prediction System (DDM501-Lab1)

Hệ thống dự đoán xếp hạng phim chuyên nghiệp dựa trên thuật toán Lọc cộng tác (Collaborative Filtering), cung cấp API hiệu suất cao để tích hợp vào các nền tảng gợi ý (Recommendation Engines).

### Mô tả dự án

Dự án này triển khai thuật toán SVD (Singular Value Decomposition) trên tập dữ liệu MovieLens 100k để dự đoán mức độ yêu thích của người dùng đối với một bộ phim cụ thể. Hệ thống được thiết kế theo tư duy MLOps, tách biệt hoàn toàn giữa luồng huấn luyện (Offline Training) và luồng phục vụ (Online Serving).

### Tính năng chính

- **Cơ chế Singleton Model**: Tối ưu hóa bộ nhớ bằng cách chỉ load mô hình một lần duy nhất khi khởi chạy API.
- **Validation chặt chẽ**: Sử dụng Pydantic Schemas để đảm bảo dữ liệu đầu vào và đầu ra luôn chính xác.
- **Auto-Documentation**: Tự động sinh tài liệu API (Swagger UI) thông qua FastAPI.
- **Containerization**: Đóng gói toàn bộ môi trường với Docker, đảm bảo tính nhất quán giữa môi trường Dev và Prod.

### Kiến trúc hệ thống

```
┌─────────────────┐      ┌────────────────────┐      ┌─────────────────┐
│  Training Data  │ ───> │ scripts/train.py   │ ───> │ models/svd.pkl  │
│ (MovieLens 100k)│      │ (SVD + Cross-Val)  │      │ (Model Artifact)│
└─────────────────┘      └────────────────────┘      └────────┬────────┘
                                                              │
┌─────────────────┐      ┌────────────────────┐               │
│     Client      │ <──> │    FastAPI App     │ <─────────────┘
│ (REST Request)  │      │ (Uvicorn Worker)   │ (Load once into RAM)
└─────────────────┘      └────────────────────┘
```

### Tech Stack

- **Ngôn ngữ**: Python 3.10+
- **ML Framework**: Surprise (Scikit-learn compatible)
- **Web Framework**: FastAPI
- **Validation**: Pydantic v2
- **Deployment**: Docker, Docker Compose
- **Server**: Uvicorn

## 🚀 Cài đặt

### 1. Sử dụng Local Environment

```bash
# Clone dự án
git clone <your-repo-url>
cd ddm501-lab1-starter

# Tạo môi trường ảo
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate

# Cài đặt thư viện
pip install -r requirements.txt
```

### 2. Sử dụng Docker (Khuyến nghị)

```bash
# Build và chạy container
docker-compose up --build
```

## Cách sử dụng

### Bước 1: Huấn luyện mô hình (Offline)

Trước khi chạy API, bạn cần tạo artifact cho mô hình:

```bash
python scripts/train_model.py
```

Script này sẽ tải dữ liệu, thực hiện Cross-validation và lưu file `models/svd_model.pkl`.

### Bước 2: Khởi chạy API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Bước 3: Truy cập API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Dự đoán mẫu (cURL):

```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 196,
  "movie_id": 242
}'
```

## Cấu trúc thư mục

```
.
├── app/
│   ├── main.py          # Entry point của FastAPI
│   ├── model.py         # Wrapper quản lý model và logic dự đoán
│   ├── schemas.py       # Định nghĩa Pydantic models (Input/Output)
│   └── config.py        # Quản lý biến môi trường và thiết lập
├── models/              # Lưu trữ artifacts (.pkl)
├── scripts/
│   └── train_model.py   # Pipeline huấn luyện và đánh giá
├── tests/               # Unit tests và Integration tests
├── Dockerfile           # Cấu hình đóng gói ứng dụng
├── docker-compose.yml   # Orchestration cho local deployment
└── requirements.txt     # Danh sách thư viện phụ thuộc
```

## ML Pipeline

- **Data Ingestion**: Tự động fetch dữ liệu MovieLens thông qua surprise.dataset.
- **Preprocessing**: Chuyển đổi dữ liệu thô sang TrainSet object.
- **Training**: Thuật toán SVD với n_factors=100, n_epochs=20.
- **Evaluation**: Đánh giá thông qua RMSE (Root Mean Square Error) và MAE.
- **Serialization**: Xuất mô hình sang định dạng Pickle để phục vụ inference.

## Deployment

Ứng dụng được thiết kế để triển khai dễ dàng trên các nền tảng đám mây (AWS, GCP, Azure) thông qua Docker.

- **Cổng mặc định**: 8000
- **Log level**: info
- **Workers**: Có thể điều chỉnh qua biến môi trường để tối ưu hóa CPU.

## API Documentation

Once the server is running, you can access interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example Prediction Request

```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "196",
  "movie_id": "242"
}'
```

## Testing

The project uses pytest for automated quality assurance.

### Run all tests:

```bash
pytest tests/ -v
```

### Run with Coverage Report:

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

## 👥 Team Members

- **Duong Binh AN**
- **Le Quang TUYEN**
- **Nguyen Thi Hong NHI**