"""Teendőlista mini alkalmazás – Flask REST API + egyszerű webes felület."""
import os

from flask import Flask, jsonify, render_template, request

from .service import TodoNotFound, TodoService


def create_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False
    version = os.environ.get("APP_VERSION", "dev")
    service = TodoService()
    app.config["TODO_SERVICE"] = service

    @app.errorhandler(ValueError)
    def bad_request(err):
        return jsonify(error=str(err)), 400

    @app.errorhandler(TodoNotFound)
    def not_found(err):
        return jsonify(error=f"Nincs ilyen teendő: {err.args[0]}"), 404

    @app.get("/health")
    def health():
        return jsonify(status="ok", version=version)

    @app.get("/")
    def index():
        return render_template("index.html", version=version)

    @app.get("/api/todos")
    def list_todos():
        return jsonify(service.list(request.args.get("status")))

    @app.post("/api/todos")
    def create_todo():
        data = request.get_json(silent=True) or {}
        todo = service.add(data.get("title"), data.get("priority", "normal"))
        return jsonify(todo), 201

    @app.get("/api/todos/<int:todo_id>")
    def get_todo(todo_id):
        return jsonify(service.get(todo_id))

    @app.patch("/api/todos/<int:todo_id>")
    def update_todo(todo_id):
        data = request.get_json(silent=True) or {}
        todo = service.update(
            todo_id,
            title=data.get("title"),
            priority=data.get("priority"),
            done=data.get("done"),
        )
        return jsonify(todo)

    @app.delete("/api/todos/<int:todo_id>")
    def delete_todo(todo_id):
        service.delete(todo_id)
        return "", 204

    @app.get("/api/stats")
    def stats():
        return jsonify(service.stats())

    return app
