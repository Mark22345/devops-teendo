import pytest

from app.service import TodoNotFound, TodoService


@pytest.fixture
def service():
    return TodoService()


def test_add_creates_open_todo_with_incrementing_id(service):
    first = service.add("Bevásárlás")
    second = service.add("Mosogatás", "high")
    assert first["id"] == 1 and second["id"] == 2
    assert first["done"] is False
    assert first["priority"] == "normal"
    assert second["priority"] == "high"


def test_add_trims_title(service):
    assert service.add("  Futás  ")["title"] == "Futás"


@pytest.mark.parametrize("title", ["", "   ", None, 123, "x" * 201])
def test_add_rejects_invalid_title(service, title):
    with pytest.raises(ValueError):
        service.add(title)


def test_add_rejects_invalid_priority(service):
    with pytest.raises(ValueError):
        service.add("Valami", "urgent")


def test_list_orders_open_first_then_by_priority(service):
    low = service.add("alacsony", "low")
    high = service.add("magas", "high")
    normal = service.add("normál", "normal")
    service.update(high["id"], done=True)
    ids = [t["id"] for t in service.list()]
    assert ids == [normal["id"], low["id"], high["id"]]


def test_list_filters_by_status(service):
    a = service.add("a")
    service.add("b")
    service.update(a["id"], done=True)
    assert [t["title"] for t in service.list("done")] == ["a"]
    assert [t["title"] for t in service.list("open")] == ["b"]
    with pytest.raises(ValueError):
        service.list("mind")


def test_update_changes_fields(service):
    todo = service.add("régi")
    updated = service.update(todo["id"], title="új", priority="low", done=True)
    assert updated["title"] == "új"
    assert updated["priority"] == "low"
    assert updated["done"] is True


def test_update_rejects_non_bool_done(service):
    todo = service.add("x")
    with pytest.raises(ValueError):
        service.update(todo["id"], done="igen")


def test_missing_todo_raises(service):
    with pytest.raises(TodoNotFound):
        service.get(42)
    with pytest.raises(TodoNotFound):
        service.update(42, done=True)
    with pytest.raises(TodoNotFound):
        service.delete(42)


def test_delete_removes_todo(service):
    todo = service.add("x")
    service.delete(todo["id"])
    assert service.list() == []


def test_returned_dict_is_a_copy(service):
    todo = service.add("x")
    todo["title"] = "módosított"
    assert service.get(todo["id"])["title"] == "x"


def test_stats(service):
    assert service.stats() == {"total": 0, "done": 0, "open": 0, "completion_percent": 0.0}
    a = service.add("a")
    service.add("b")
    service.add("c")
    service.update(a["id"], done=True)
    assert service.stats() == {"total": 3, "done": 1, "open": 2, "completion_percent": 33.3}
