import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_health_endpoint(client):
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "message" in data
    assert "version" in data


def test_main_app_imports():
    """Test that main app can be imported without errors."""
    from src.main import app
    assert app is not None


def test_models_import():
    """Test that models can be imported without errors."""
    from src.models.knowledge_doc import KnowledgeDoc
    from src.models.vector_chunk import VectorChunk
    from src.models.audit_log import AuditLog

    assert KnowledgeDoc is not None
    assert VectorChunk is not None
    assert AuditLog is not None


def test_services_import():
    """Test that services can be imported without errors."""
    from src.services.knowledge_service import knowledge_doc_service
    from src.services.vector_service import vector_chunk_service
    from src.services.audit_service import audit_service
    from src.services.embedding_service import embedding_service

    assert knowledge_doc_service is not None
    assert vector_chunk_service is not None
    assert audit_service is not None
    assert embedding_service is not None