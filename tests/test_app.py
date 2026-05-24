import pytest
from src.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """Test that the index home page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Skillyfy" in response.data


def test_api_calculate_add(client):
    """Test standard addition via API."""
    response = client.post("/api/calculate", json={
        "operation": "add",
        "a": 10,
        "b": 5
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["result"] == 15


def test_api_calculate_divide(client):
    """Test standard division via API."""
    response = client.post("/api/calculate", json={
        "operation": "divide",
        "a": 10,
        "b": 4
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["result"] == 2.5


def test_api_calculate_divide_by_zero(client):
    """Test division by zero error handling."""
    response = client.post("/api/calculate", json={
        "operation": "divide",
        "a": 10,
        "b": 0
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Cannot divide by zero." in data["error"]


def test_api_calculate_square_root(client):
    """Test square root API operation."""
    response = client.post("/api/calculate", json={
        "operation": "square_root",
        "a": 16
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["result"] == 4.0


def test_api_calculate_square_root_negative(client):
    """Test square root with negative value error handling."""
    response = client.post("/api/calculate", json={
        "operation": "square_root",
        "a": -9
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    msg = "Cannot calculate square root of a negative number."
    assert msg in data["error"]


def test_api_calculate_missing_params(client):
    """Test API request validation when parameters are missing."""
    response = client.post("/api/calculate", json={
        "operation": "add",
        "a": 10
        # missing "b"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Missing parameter" in data["error"]


def test_api_calculate_invalid_operation(client):
    """Test behavior when operation is unsupported."""
    response = client.post("/api/calculate", json={
        "operation": "integrate",
        "a": 1,
        "b": 2
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Invalid operation" in data["error"]


def test_api_calculate_invalid_payload(client):
    """Test POST request with non-JSON payload."""
    response = client.post("/api/calculate", data="not json string")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Request body must be valid JSON." in data["error"]
