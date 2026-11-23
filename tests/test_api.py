import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_index_page(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "Teendőlista" in res.get_data(as_text=True)


def test_create_and_list(client):
    res = client.post("/api/todos", json={"title": "Beadandó", "priority": "high"})
    assert res.status_code == 201
    todo = res.get_json()
    assert todo["title"] == "Beadandó"
    assert client.get("/api/todos").get_json() == [todo]


def test_create_without_title_returns_400(client):
    res = client.post("/api/todos", json={})
    assert res.status_code == 400
    assert "title" in res.get_json()["error"]


def test_create_with_invalid_json_returns_400(client):
    res = client.post("/api/todos", data="nem json", content_type="application/json")
    assert res.status_code == 400


def test_get_update_delete(client):
    todo_id = client.post("/api/todos", json={"title": "x"}).get_json()["id"]

    assert client.get(f"/api/todos/{todo_id}").status_code == 200

    res = client.patch(f"/api/todos/{todo_id}", json={"done": True})
    assert res.status_code == 200
    assert res.get_json()["done"] is True

    assert client.delete(f"/api/todos/{todo_id}").status_code == 204
    assert client.get(f"/api/todos/{todo_id}").status_code == 404


def test_unknown_todo_returns_404(client):
    assert client.patch("/api/todos/999", json={"done": True}).status_code == 404
    assert client.delete("/api/todos/999").status_code == 404


def test_status_filter(client):
    a = client.post("/api/todos", json={"title": "a"}).get_json()["id"]
    client.post("/api/todos", json={"title": "b"})
    client.patch(f"/api/todos/{a}", json={"done": True})
    assert [t["title"] for t in client.get("/api/todos?status=open").get_json()] == ["b"]
    assert client.get("/api/todos?status=rossz").status_code == 400


def test_stats_endpoint(client):
    client.post("/api/todos", json={"title": "a"})
    stats = client.get("/api/stats").get_json()
    assert stats["total"] == 1 and stats["open"] == 1
