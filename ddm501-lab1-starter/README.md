# Lab 1: First ML Product - Movie Rating Prediction API

## 👥 Team Members 
- **Duong Binh AN**
- **Le Quang TUYEN**
- **Nguyen Thi Hong NHI**

## Overview

Build your first ML product - a Movie Rating Prediction API using collaborative filtering, REST API, and Docker containerization.

## 🎯 Completion Status

✅ **PROJECT COMPLETE - ALL COMPONENTS FUNCTIONAL**

### Implementation Summary
- **Model Training**: SVD Collaborative Filtering model trained and saved
- **API Implementation**: Full REST API with health check, prediction, and batch endpoints
- **Test Suite**: 10/10 unit tests passing
- **Documentation**: Complete API documentation with Swagger UI

### Metrics
- **Model Performance**: 
  - Cross-Validation RMSE: 0.9370
  - Cross-Validation MAE: 0.7386
  - Test Sample Prediction: User 196 → Movie 242 = 3.68 rating
- **Test Results**: 10/10 tests passed ✅
- **API Status**: All endpoints functional and validated

## Project Structure

```
ddm501-lab1-starter/
├── app/
│   ├── __init__.py
│   ├── main.py           # ✅ FastAPI application - COMPLETE
│   ├── model.py          # ✅ ML model loading & prediction - COMPLETE
│   ├── schemas.py        # ✅ Pydantic models - COMPLETE
│   └── config.py         # Configuration
├── models/               
│   └── svd_model.pkl     # ✅ Trained SVD model
├── tests/
│   ├── __init__.py
│   └── test_api.py       # ✅ Unit tests (10/10 passing) - COMPLETE
├── scripts/
│   └── train_model.py    # ✅ Model training script - COMPLETE
├── Dockerfile            # Docker containerization
├── docker-compose.yml    # Multi-container orchestration
├── requirements.txt      # Python dependencies
└── README.md
```

## Prerequisites

- Python 3.10+ (tested with 3.12.10)
- Docker & Docker Compose
- Git
- Virtual environment (venv/conda)

## Quick Start

### 1. Setup Environment

```bash
cd ddm501-lab1-starter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Train the Model

The model file is pre-trained and included. To retrain:

```bash
python scripts/train_model.py
```

**Training Output** (from latest run):
```
[1/4] Loading MovieLens 100K dataset...
      Dataset loaded successfully!
      - This dataset contains 100,000 ratings
      - From 943 users on 1,682 movies

[2/4] Performing cross-validation...
      Cross-validation results:
      - Mean RMSE: 0.9370
      - Mean MAE:  0.7386

[3/4] Training on full dataset...
      Training completed!

[4/4] Saving model to models/svd_model.pkl...
      Model saved successfully!

Sample prediction:
  User ID:           196
  Movie ID:          242
  Predicted Rating:  3.68
```

### 3. Run the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test the API

#### Manual Tests (cURL):
```bash
# Health check
curl http://localhost:8000/health

# Single Prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "196", "movie_id": "242"}'

# Batch Predictions
curl -X POST "http://localhost:8000/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{"predictions": [{"user_id": "196", "movie_id": "242"}, {"user_id": "1", "movie_id": "100"}]}'
```

#### Unit Tests:
```bash
pytest tests/test_api.py -v

# Test Results
# tests/test_api.py::TestHealthEndpoint::test_health_check_returns_200 PASSED
# tests/test_api.py::TestHealthEndpoint::test_health_check_response_format PASSED
# tests/test_api.py::TestRootEndpoint::test_root_returns_200 PASSED
# tests/test_api.py::TestPredictEndpoint::test_predict_valid_input PASSED
# tests/test_api.py::TestPredictEndpoint::test_predict_missing_field PASSED
# tests/test_api.py::TestPredictEndpoint::test_predict_empty_payload PASSED
# tests/test_api.py::TestModelInfoEndpoint::test_model_info_returns_200 PASSED
# tests/test_api.py::TestModelInfoEndpoint::test_model_info_contains_version PASSED
# tests/test_api.py::TestBatchPredictEndpoint::test_batch_predict_multiple_items PASSED
# tests/test_api.py::TestBatchPredictEndpoint::test_batch_predict_empty_list PASSED
# ======================= 10 passed ==========================
```

### 5. Run with Docker

```bash
docker-compose build
docker-compose up -d

# Access API
curl http://localhost:8000/health
```

## API Endpoints

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/` | API info and routes | ✅ |
| GET | `/health` | Health check | ✅ |
| POST | `/predict` | Single rating prediction | ✅ |
| POST | `/predict/batch` | Batch predictions | ✅ |
| GET | `/model/info` | Model information | ✅ |
| GET | `/docs` | Swagger documentation | ✅ |

## API Documentation

FastAPI automatically generates interactive Swagger documentation. When running the API locally:

**Access Swagger UI**: `http://localhost:8000/docs`  
**Access ReDoc**: `http://localhost:8000/redoc`

### Example Requests & Responses

#### Health Check
```bash
GET /health
```
**Response (200)**:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

#### Single Prediction
```bash
POST /predict
Content-Type: application/json

{
  "user_id": "196",
  "movie_id": "242"
}
```
**Response (200)**:
```json
{
  "user_id": "196",
  "movie_id": "242",
  "predicted_rating": 3.68,
  "model_version": "1.0.0"
}
```

#### Batch Predictions
```bash
POST /predict/batch
Content-Type: application/json

{
  "predictions": [
    {"user_id": "196", "movie_id": "242"},
    {"user_id": "1", "movie_id": "100"}
  ]
}
```
**Response (200)**:
```json
{
  "predictions": [
    {
      "user_id": "196",
      "movie_id": "242",
      "predicted_rating": 3.68,
      "model_version": "1.0.0"
    },
    {
      "user_id": "1",
      "movie_id": "100",
      "predicted_rating": 4.15,
      "model_version": "1.0.0"
    }
  ],
  "total_count": 2
}
```

#### Model Info
```bash
GET /model/info
```
**Response (200)**:
```json
{
  "model_version": "1.0.0",
  "model_type": "SVD (Collaborative Filtering)",
  "is_loaded": true
}
```

## Implementation Details

### ML Model
- **Algorithm**: Singular Value Decomposition (SVD)
- **Framework**: scikit-surprise
- **Dataset**: MovieLens 100K
- **Training Parameters**:
  - n_factors: 100 (latent factors)
  - n_epochs: 20 (training iterations)
  - lr_all: 0.005 (learning rate)
  - reg_all: 0.02 (regularization)

### Model Wrapper (`app/model.py`)
- `_load_model()`: Loads pickled SVD model from disk
- `predict(user_id, movie_id)`: Single prediction with rounding to 2 decimals
- `predict_batch(pairs)`: Batch predictions using list comprehension
- `is_loaded()`: Status check

### API Framework (FastAPI)
- **Async Endpoints**: All endpoints are async for scalability
- **CORS Enabled**: Cross-Origin Resource Sharing configured
- **Request Validation**: Pydantic models validate all inputs
- **Error Handling**: HTTP exceptions with proper status codes
- **Logging**: Structured logging for debugging

## Dependencies

```
fastapi           # Web framework
uvicorn           # ASGI server
pandas            # Data processing
numpy<2.0.0       # Numerical computing
scikit-learn      # Machine learning
scikit-surprise   # Collaborative filtering
pydantic          # Data validation
python-dotenv     # Environment configuration
pytest            # Testing
pytest-cov        # Code coverage
httpx             # HTTP client for tests
```

## Testing

### Test Suite Overview
- **Total Tests**: 10
- **Passed**: 10 ✅
- **Failed**: 0
- **Coverage**: Health checks, predictions, validation, batch operations

### Running Tests
```bash
# Run all tests with verbose output
pytest tests/test_api.py -v

# Run specific test class
pytest tests/test_api.py::TestPredictEndpoint -v

# Run with coverage
pytest tests/test_api.py --cov=app
```

## Troubleshooting

### Model Not Loading
- Verify `models/svd_model.pkl` exists in the project root
- Check file permissions
- Ensure scikit-surprise is installed: `pip install scikit-surprise`

### Port Already in Use
```bash
# Change port number
uvicorn app.main:app --port 8001

# On Windows, find process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Import Errors
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

## Performance Considerations

- **Prediction Latency**: ~5-10ms per request (model loaded in memory)
- **Batch Efficiency**: Linear O(n) for n predictions
- **Memory Usage**: ~10-15MB for loaded model
- **Concurrency**: FastAPI handles multiple concurrent requests via async

## Future Enhancements

- [ ] Add user/item information endpoints
- [ ] Implement caching for frequent predictions
- [ ] Add model versioning and A/B testing
- [ ] Implement rate limiting and authentication
- [ ] Add monitoring and metrics endpoints
- [ ] Deploy to Kubernetes for production
- [ ] Add database persistence for prediction logs

## References

- [MovieLens Dataset](https://grouplens.org/datasets/movielens/)
- [scikit-surprise Documentation](https://surprise.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Collaborative Filtering](https://en.wikipedia.org/wiki/Collaborative_filtering)

## Team

**Lab 1 - ML Product Development**  
Course: DDM501  
Weight: 5%

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
3. Push to your GitHub repository: [RocketUp-Team/Lab01.1_MLOPs_Team1](https://github.com/RocketUp-Team/Lab01.1_MLOPs_Team1)
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