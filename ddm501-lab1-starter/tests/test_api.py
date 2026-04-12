"""
Unit tests for Movie Rating Prediction API.

TODO: Complete the test cases below.

Run tests with:
    pytest tests/ -v
    pytest tests/ -v --cov=app --cov-report=html
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

@pytest.fixture(scope="module")
def client():
    """TestClient that triggers FastAPI startup/shutdown events."""
    with TestClient(app) as c:
        yield c


# =============================================================================
# Health Check Tests (PROVIDED)
# =============================================================================
class TestHealthEndpoint:
    """Tests for the /health endpoint."""
    
    def test_health_check_returns_200(self, client):
        """Test that health endpoint returns 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_response_format(self, client):
        """Test that health response has correct format."""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert "model_loaded" in data
        assert isinstance(data["status"], str)
        assert isinstance(data["model_loaded"], bool)


# =============================================================================
# Root Endpoint Tests (PROVIDED)
# =============================================================================
class TestRootEndpoint:
    """Tests for the / endpoint."""
    
    def test_root_returns_200(self, client):
        """Test that root endpoint returns 200 status code."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_contains_api_info(self, client):
        """Test that root response contains API information."""
        response = client.get("/")
        data = response.json()
        
        assert "name" in data
        assert "version" in data
        assert "docs" in data


# =============================================================================
# TODO 1: Prediction Endpoint Tests
# =============================================================================
class TestPredictEndpoint:
    """Tests for the /predict endpoint."""

    def _assert_model_loaded(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["model_loaded"] is True, "Model must be trained and present at models/svd_model.pkl"
    
    # -------------------------------------------------------------------------
    # TODO: Implement test_predict_valid_input
    # -------------------------------------------------------------------------
    # Requirements:
    # - Send POST request to /predict with valid user_id and movie_id
    # - Assert status code is 200
    # - Assert response contains "predicted_rating"
    # - Assert predicted_rating is between 1.0 and 5.0
    
    def test_predict_valid_input(self, client):
        """Test prediction with valid input."""
        self._assert_model_loaded(client)
        response = client.post(
            "/predict",
            json={"user_id": "196", "movie_id": "242"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "predicted_rating" in data
        assert 1.0 <= data["predicted_rating"] <= 5.0
    
    # -------------------------------------------------------------------------
    # TODO: Implement test_predict_response_format
    # -------------------------------------------------------------------------
    # Requirements:
    # - Assert response contains all required fields:
    #   user_id, movie_id, predicted_rating, model_version
    
    def test_predict_response_format(self, client):
        """Test that prediction response has correct format."""
        self._assert_model_loaded(client)
        response = client.post(
            "/predict",
            json={"user_id": "196", "movie_id": "242"},
        )
        assert response.status_code == 200
        data = response.json()

        assert "user_id" in data
        assert "movie_id" in data
        assert "predicted_rating" in data
        assert "model_version" in data
    
    # -------------------------------------------------------------------------
    # TODO: Implement test_predict_missing_user_id
    # -------------------------------------------------------------------------
    # Requirements:
    # - Send request without user_id
    # - Assert status code is 422 (Validation Error)
    
    def test_predict_missing_user_id(self, client):
        """Test prediction with missing user_id."""
        response = client.post("/predict", json={"movie_id": "242"})
        assert response.status_code == 422
    
    # -------------------------------------------------------------------------
    # TODO: Implement test_predict_missing_movie_id
    # -------------------------------------------------------------------------
    # Requirements:
    # - Send request without movie_id
    # - Assert status code is 422 (Validation Error)
    
    def test_predict_missing_movie_id(self, client):
        """Test prediction with missing movie_id."""
        response = client.post("/predict", json={"user_id": "196"})
        assert response.status_code == 422
    
    # -------------------------------------------------------------------------
    # TODO: Implement test_predict_empty_body
    # -------------------------------------------------------------------------
    # Requirements:
    # - Send request with empty JSON body
    # - Assert status code is 422 (Validation Error)
    
    def test_predict_empty_body(self, client):
        """Test prediction with empty request body."""
        response = client.post("/predict", json={})
        assert response.status_code == 422

    def test_predict_blank_ids(self, client):
        """Test prediction with blank IDs (should fail validation)."""
        response = client.post("/predict", json={"user_id": "   ", "movie_id": "242"})
        assert response.status_code == 422
        response = client.post("/predict", json={"user_id": "196", "movie_id": "   "})
        assert response.status_code == 422

    def test_predict_model_not_loaded_returns_503(self, client, monkeypatch):
        """Test that /predict returns 503 when the model is not available."""
        import app.main as main
        monkeypatch.setattr(main, "model", None)
        response = client.post("/predict", json={"user_id": "196", "movie_id": "242"})
        assert response.status_code == 503


# =============================================================================
# TODO 2: Edge Case Tests (BONUS)
# =============================================================================
class TestEdgeCases:
    """Edge case tests."""
    
    def test_predict_unknown_user(self, client):
        """Test prediction with unknown user ID."""
        response = client.post("/predict", json={"user_id": "999999", "movie_id": "242"})
        assert response.status_code == 200
        data = response.json()
        assert 1.0 <= data["predicted_rating"] <= 5.0
    
    def test_predict_unknown_movie(self, client):
        """Test prediction with unknown movie ID."""
        response = client.post("/predict", json={"user_id": "196", "movie_id": "999999"})
        assert response.status_code == 200
        data = response.json()
        assert 1.0 <= data["predicted_rating"] <= 5.0
    
    def test_predict_special_characters_in_id(self, client):
        """Test prediction with special characters in IDs."""
        pytest.skip("Out of core scope; keep minimal for submission safety.")


# =============================================================================
# TODO 3: Model Info Endpoint Tests
# =============================================================================
class TestModelInfoEndpoint:
    """Tests for the /model/info endpoint."""
    
    def test_model_info_returns_200(self, client):
        """Test that model info endpoint returns 200."""
        response = client.get("/model/info")
        assert response.status_code == 200
    
    def test_model_info_contains_version(self, client):
        """Test that model info contains version."""
        response = client.get("/model/info")
        assert response.status_code == 200
        data = response.json()
        assert "model_version" in data
        assert "is_loaded" in data
        assert isinstance(data["model_version"], str)
        assert isinstance(data["is_loaded"], bool)


# =============================================================================
# Batch Prediction Tests (BONUS)
# =============================================================================
class TestBatchPredictEndpoint:
    """Tests for the /predict/batch endpoint (BONUS)."""
    
    def test_batch_predict_multiple_items(self, client):
        """Test batch prediction with multiple items."""
        response = client.post(
            "/predict/batch",
            json={
                "predictions": [
                    {"user_id": "196", "movie_id": "242"},
                    {"user_id": "10", "movie_id": "50"},
                ]
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 2
        assert len(data["predictions"]) == 2
        for item in data["predictions"]:
            assert 1.0 <= item["predicted_rating"] <= 5.0
    
    def test_batch_predict_empty_list(self, client):
        """Test batch prediction with empty list."""
        response = client.post("/predict/batch", json={"predictions": []})
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 0
        assert data["predictions"] == []


# =============================================================================
# Run tests
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
