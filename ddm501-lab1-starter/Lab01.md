
# LAB 1 FIRST ML PRODUCT

**Course** | DDM501  
**Weight** | 5%  
**Format** | Team Lab (3-4 members per team)

## 1. OVERVIEW

### 1.1. Introduction

The purpose of this lab is to build the first complete ML product - a Movie Rating Prediction system. This lab simulates the real-world process when an ML Engineer receives a trained model and needs to bring it to production: from wrapping the model in an API, containerizing the application, to writing tests and documentation.

### 1.2. Scenario: Movie Rating Prediction System

You are an ML Engineer at a company. The Data Science team has trained a collaborative filtering model to predict the rating a user would give to a movie. Your task is to:

- Wrap the model in a REST API so other services can call it
- Ensure the API can handle requests with low latency
- Containerize for easy deployment across different environments
- Write tests and documentation for the DevOps team

## 2. BACKGROUND

### 2.1. REST API

REST API is the most common way to expose ML models for other applications to use. A typical ML API has the following endpoints:

```
POST /predict: Receives input data, returns predictions
GET /health: Health check endpoint for monitoring
GET /model/info: Information about model version, metrics
```

### 2.2. Docker

- **Dockerfile**: Blueprint to build Docker image
- **Docker Image**: Snapshot of application + dependencies
- **Docker Container**: Running instance of an image
- **docker-compose.yml**: Defines multi-container application

### 2.3. Collaborative Filtering Basics

Collaborative Filtering (CF) is a recommendation technique based on the behavior of similar users. There are 2 main types:

- **User-based CF**: Find users with similar preferences, recommend items they liked
- **Item-based CF**: Find items similar to those the user has liked

In this lab, we use Matrix Factorization (SVD) - a popular model-based CF approach.

## 3. HANDS-ON GUIDES

### Task 1: Setup Development Environment

1. Create project structure
2. Setup Python virtual environment
3. Install dependencies

### Task 2: Implement ML Model

#### 2.1. Prepare data

Use MovieLens 100K dataset - a standard dataset for recommendation systems with 100,000 ratings from 943 users for 1,682 movies.

#### 2.2. Train and save model

Create `train_model.py` script to train and save the model.

#### 2.3. Implement prediction function

In `app/model.py`, implement a class to load model and predict.

### Task 3: Build REST API

1. Define Pydantic schemas
2. Implement FastAPI application
3. Run and test API locally

Access Swagger UI at: `http://localhost:8000/docs`

### Task 4: Containerization with Docker

1. Write Dockerfile
2. Write docker-compose.yml
3. Build and run

### Task 5: Testing

1. Write unit tests
2. Run tests

### Task 6: Documentation

#### 6.1. Write README.md

README should include:

- Project description and features
- Prerequisites (Python, Docker)
- Installation steps
- API usage examples
- Running tests
- Project structure

#### 6.2. API Documentation

FastAPI automatically generates Swagger documentation at `/docs`. Ensure all endpoints have complete docstrings and examples in Pydantic models.

## 4. STARTER CODE TEMPLATE

Unzip starter code: `unzip ddm501-lab1-starter.zip`

The repository already has the folder structure and placeholder files. Students need to complete the sections marked TODO in the code.

Files to complete:

| File          | TODO Items |
|---------------|------------|
| app/model.py  | Implement load_model(), predict(), predict_batch() |
| app/main.py   | Implement /predict endpoint, error handling |
| app/schemas.py| Define request/response Pydantic models |
| Dockerfile    | Complete Dockerfile with health check |
| tests/test_api.py | Add test cases for edge cases |

## 5. DELIVERABLES & GRADING

### 5.1. Deliverables

Submit GitHub repository link containing:

- Working ML Model: Trained model file (.pkl) + loading code
- REST API: FastAPI application with /health and /predict endpoints
- Docker Setup: Working Dockerfile + docker-compose.yml
- Test Suite: Unit tests with pytest
- Documentation: README.md + API docs (Swagger)

### 5.2. Grading Rubric

| Criteria      | Weight | Detailed Description |
|---------------|--------|----------------------|
| Working ML Model | 25% | Model loads successfully (10%)<br>Valid predictions 1-5 (10%)<br>Error handling (5%) |
| REST API      | 25% | /health endpoint (5%)<br>/predict endpoint correct (10%)<br>Input validation (5%)<br>Proper error responses (5%) |
| Docker Setup  | 20% | Dockerfile builds (8%)<br>docker-compose works (7%)<br>Health check configured (5%) |
| Test Cases    | 20% | Happy path tests (8%)<br>Edge case tests (7%)<br>Tests pass (5%) |
| Documentation | 10% | Complete README (5%)<br>API docs (Swagger) (5%) |

### 5.3. Submission

- **Deadline**: 1 week after the lab session
- **Format**: GitHub repository link
