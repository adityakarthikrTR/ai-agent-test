"""Tests for the Calculator REST API."""

import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


# =============================================================================
# Level 1: Unit Tests — Each endpoint returns correct results
# =============================================================================


class TestHealthEndpoint:
    """Tests for the GET /health endpoint."""

    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_healthy(self, client):
        response = client.get("/health")
        assert response.json() == {"status": "healthy"}


class TestAddEndpoint:
    """Tests for POST /calculate with operation=add."""

    def test_add_positive_numbers(self, client):
        response = client.post(
            "/calculate", json={"operation": "add", "a": 10, "b": 5}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 15.0
        assert data["operation"] == "add"

    def test_add_negative_numbers(self, client):
        response = client.post(
            "/calculate", json={"operation": "add", "a": -3, "b": -7}
        )
        assert response.json()["result"] == -10.0

    def test_add_floats(self, client):
        response = client.post(
            "/calculate", json={"operation": "add", "a": 1.5, "b": 2.5}
        )
        assert response.json()["result"] == 4.0


class TestSubtractEndpoint:
    """Tests for POST /calculate with operation=subtract."""

    def test_subtract_positive_numbers(self, client):
        response = client.post(
            "/calculate", json={"operation": "subtract", "a": 10, "b": 3}
        )
        assert response.status_code == 200
        assert response.json()["result"] == 7.0

    def test_subtract_negative_result(self, client):
        response = client.post(
            "/calculate", json={"operation": "subtract", "a": 3, "b": 10}
        )
        assert response.json()["result"] == -7.0


class TestMultiplyEndpoint:
    """Tests for POST /calculate with operation=multiply."""

    def test_multiply_positive_numbers(self, client):
        response = client.post(
            "/calculate", json={"operation": "multiply", "a": 4, "b": 5}
        )
        assert response.status_code == 200
        assert response.json()["result"] == 20.0

    def test_multiply_by_zero(self, client):
        response = client.post(
            "/calculate", json={"operation": "multiply", "a": 99, "b": 0}
        )
        assert response.json()["result"] == 0.0


class TestDivideEndpoint:
    """Tests for POST /calculate with operation=divide."""

    def test_divide_positive_numbers(self, client):
        response = client.post(
            "/calculate", json={"operation": "divide", "a": 20, "b": 4}
        )
        assert response.status_code == 200
        assert response.json()["result"] == 5.0

    def test_divide_returns_float(self, client):
        response = client.post(
            "/calculate", json={"operation": "divide", "a": 7, "b": 2}
        )
        assert response.json()["result"] == 3.5


# =============================================================================
# Level 2: Integration Tests — API → calculator module integration
# =============================================================================


class TestResponseFormat:
    """Verify the response payload structure matches the contract."""

    def test_response_contains_all_fields(self, client):
        response = client.post(
            "/calculate", json={"operation": "add", "a": 1, "b": 2}
        )
        data = response.json()
        assert "operation" in data
        assert "a" in data
        assert "b" in data
        assert "result" in data

    def test_response_echoes_operands(self, client):
        response = client.post(
            "/calculate", json={"operation": "multiply", "a": 6, "b": 7}
        )
        data = response.json()
        assert data["a"] == 6.0
        assert data["b"] == 7.0
        assert data["operation"] == "multiply"


# =============================================================================
# Level 3: Functional Tests — Realistic workflows via the API
# =============================================================================


class TestCalculatorWorkflows:
    """Test multi-step calculations through the API."""

    def test_percentage_calculation(self, client):
        """Calculate 20% of 150: multiply(150, 20) then divide by 100."""
        step1 = client.post(
            "/calculate", json={"operation": "multiply", "a": 150, "b": 20}
        )
        intermediate = step1.json()["result"]

        step2 = client.post(
            "/calculate", json={"operation": "divide", "a": intermediate, "b": 100}
        )
        assert step2.json()["result"] == 30.0

    def test_average_of_three_numbers(self, client):
        """Average of 10, 20, 30 via API: add them then divide by 3."""
        step1 = client.post(
            "/calculate", json={"operation": "add", "a": 10, "b": 20}
        )
        step2 = client.post(
            "/calculate",
            json={"operation": "add", "a": step1.json()["result"], "b": 30},
        )
        step3 = client.post(
            "/calculate",
            json={"operation": "divide", "a": step2.json()["result"], "b": 3},
        )
        assert step3.json()["result"] == 20.0


# =============================================================================
# Level 4: Edge & Security Tests — Error handling and invalid inputs
# =============================================================================


class TestDivisionByZero:
    """Test division by zero returns a proper 400 error."""

    def test_divide_by_zero_returns_400(self, client):
        response = client.post(
            "/calculate", json={"operation": "divide", "a": 10, "b": 0}
        )
        assert response.status_code == 400

    def test_divide_by_zero_error_body(self, client):
        response = client.post(
            "/calculate", json={"operation": "divide", "a": 10, "b": 0}
        )
        data = response.json()["detail"]
        assert data["error"] == "division_by_zero"


class TestInvalidRequests:
    """Test that malformed requests are rejected with 422."""

    def test_missing_operation(self, client):
        response = client.post("/calculate", json={"a": 1, "b": 2})
        assert response.status_code == 422

    def test_missing_operand_a(self, client):
        response = client.post(
            "/calculate", json={"operation": "add", "b": 2}
        )
        assert response.status_code == 422

    def test_missing_operand_b(self, client):
        response = client.post(
            "/calculate", json={"operation": "add", "a": 1}
        )
        assert response.status_code == 422

    def test_invalid_operation(self, client):
        response = client.post(
            "/calculate", json={"operation": "power", "a": 2, "b": 3}
        )
        assert response.status_code == 422

    def test_string_operand(self, client):
        response = client.post(
            "/calculate", json={"operation": "add", "a": "abc", "b": 1}
        )
        assert response.status_code == 422

    def test_empty_body(self, client):
        response = client.post("/calculate", content=b"{}")
        assert response.status_code == 422

    def test_no_body(self, client):
        response = client.post("/calculate")
        assert response.status_code == 422
