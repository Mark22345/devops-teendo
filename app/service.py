"""Üzleti logika: teendők kezelése (memóriában tárolva)."""
import threading
from datetime import datetime, timezone

PRIORITIES = ("low", "normal", "high")
MAX_TITLE_LENGTH = 200


class TodoNotFound(KeyError):
    """A kért teendő nem létezik."""


class TodoService:
    def __init__(self):
        self._items = {}
        self._next_id = 1
        self._lock = threading.Lock()

    @staticmethod
    def _validate_title(title):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("A 'title' mező kötelező.")
        title = title.strip()
        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError(f"A cím legfeljebb {MAX_TITLE_LENGTH} karakter lehet.")
        return title

    @staticmethod
    def _validate_priority(priority):
        if priority not in PRIORITIES:
            raise ValueError(f"A prioritás csak ezek egyike lehet: {', '.join(PRIORITIES)}.")
        return priority

    def add(self, title, priority="normal"):
        title = self._validate_title(title)
        priority = self._validate_priority(priority)
        with self._lock:
            todo = {
                "id": self._next_id,
                "title": title,
                "priority": priority,
                "done": False,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            self._items[todo["id"]] = todo
            self._next_id += 1
            return dict(todo)

    def list(self, status=None):
        with self._lock:
            items = [dict(t) for t in self._items.values()]
        if status == "open":
            items = [t for t in items if not t["done"]]
        elif status == "done":
            items = [t for t in items if t["done"]]
        elif status is not None:
            raise ValueError("A status szűrő értéke 'open' vagy 'done' lehet.")
        order = {p: i for i, p in enumerate(reversed(PRIORITIES))}
        return sorted(items, key=lambda t: (t["done"], order[t["priority"]], t["id"]))

    def get(self, todo_id):
        with self._lock:
            if todo_id not in self._items:
                raise TodoNotFound(todo_id)
            return dict(self._items[todo_id])

    def update(self, todo_id, title=None, priority=None, done=None):
        if title is not None:
            title = self._validate_title(title)
        if priority is not None:
            priority = self._validate_priority(priority)
        if done is not None and not isinstance(done, bool):
            raise ValueError("A 'done' mező logikai érték (true/false) kell legyen.")
        with self._lock:
            if todo_id not in self._items:
                raise TodoNotFound(todo_id)
            todo = self._items[todo_id]
            if title is not None:
                todo["title"] = title
            if priority is not None:
                todo["priority"] = priority
            if done is not None:
                todo["done"] = done
            return dict(todo)

    def delete(self, todo_id):
        with self._lock:
            if todo_id not in self._items:
                raise TodoNotFound(todo_id)
            del self._items[todo_id]

    def stats(self):
        with self._lock:
            total = len(self._items)
            done = sum(1 for t in self._items.values() if t["done"])
        return {
            "total": total,
            "done": done,
            "open": total - done,
            "completion_percent": round(done / total * 100, 1) if total else 0.0,
        }
