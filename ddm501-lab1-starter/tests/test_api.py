"""
Unit tests for Movie Rating Prediction API.
Fully implemented by Senior QA.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
import app.main as main_module

# Create test client
client = TestClient(app)

# Fixture to ensure model is loaded before tests
@pytest.fixture(scope="session", autouse=True)
def load_model():
    """Ensure model is loaded for all tests."""
    import asyncio
    asyncio.run(main_module.startup_event())
    yield

# =============================================================================
# Health Check & Root Tests
# =============================================================================
class TestHealthEndpoint:
    def test_health_check_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_response_format(self):
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
        assert isinstance(data["status"], str)
        assert isinstance(data["model_loaded"], bool)

class TestRootEndpoint:
    def test_root_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data

# =============================================================================
# Prediction Endpoint Tests (IMPLEMENTED)
# =============================================================================
class TestPredictEndpoint:
    
    @patch("app.model.MovieRatingModel.predict")
    def test_predict_valid_input(self, mock_predict):
        """TC_03: Test prediction with valid inputs (Happy Path) using Mock."""
        # Giả lập model luôn trả về 4.5 để không phụ thuộc file .pkl
        mock_predict.return_value = 4.5
        
        payload = {"user_id": "196", "movie_id": "242"}
        response = client.post("/predict", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "196"
        assert data["movie_id"] == "242"
        assert data["predicted_rating"] == 4.5
        assert "model_version" in data
    
    def test_predict_missing_field(self):
        """TC_04: Test validation error when field is missing."""
        payload = {"user_id": "196"} # Thiếu movie_id
        response = client.post("/predict", json=payload)
        
        assert response.status_code == 422
        data = response.json()
        # Đảm bảo lỗi báo đúng vị trí thiếu data
        assert data["detail"][0]["loc"] == ["body", "movie_id"]
        assert data["detail"][0]["type"] == "missing"

    def test_predict_empty_payload(self):
        """TC_05: Test validation error with empty JSON."""
        response = client.post("/predict", json={})
        assert response.status_code == 422

# =============================================================================
# Model Info Endpoint Tests (IMPLEMENTED)
# =============================================================================
class TestModelInfoEndpoint:
    
    def test_model_info_returns_200(self):
        response = client.get("/model/info")
        assert response.status_code == 200
    
    def test_model_info_contains_version(self):
        """TC_06: Test model info payload structure."""
        response = client.get("/model/info")
        data = response.json()
        
        assert "model_version" in data
        assert "model_type" in data
        assert "is_loaded" in data
        assert isinstance(data["model_version"], str)
        assert isinstance(data["is_loaded"], bool)

# =============================================================================
# Batch Prediction Tests (BONUS - IMPLEMENTED)
# =============================================================================
class TestBatchPredictEndpoint:
    
    @patch("app.main.model")
    def test_batch_predict_multiple_items(self, mock_model):
        """TC_07: Test batch prediction with multiple valid items."""
        # Mock the model's predict method
        mock_instance = mock_model
        mock_instance.is_loaded.return_value = True
        # Return different predictions for each call
        mock_instance.predict.side_effect = [3.5, 4.0]
        
        payload = {
            "predictions": [
                {"user_id": "1", "movie_id": "100"},
                {"user_id": "2", "movie_id": "200"}
            ]
        }
        response = client.post("/predict/batch", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 2
        assert len(data["predictions"]) == 2
        assert data["predictions"][0]["predicted_rating"] == 3.5
        assert data["predictions"][1]["predicted_rating"] == 4.0
    
    def test_batch_predict_empty_list(self):
        """TC_08: Test batch prediction with an empty list."""
        payload = {"predictions": []}
        response = client.post("/predict/batch", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 0
        assert len(data["predictions"]) == 0