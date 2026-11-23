# Teendőlista – DevOps CI/CD projekt

Egyszerű teendőkezelő webalkalmazás (Python / Flask) teljes, end-to-end CI/CD pipeline-nal
GitHub Actions + Docker + Kubernetes (kind) sandbox környezetben.

A részletes leírás a [DOKUMENTACIO.md](DOKUMENTACIO.md) fájlban, az elevator pitch vázlata
az [ELEVATOR_PITCH.md](ELEVATOR_PITCH.md) fájlban található.

## Pipeline röviden

```
git push (main) ──► [test] flake8 + pytest ──► [build] Docker image + konténer füstteszt
                                                  │   └─► GHCR (ghcr.io/<owner>/teendo-app)
                                                  ▼
                       [deploy] kind Kubernetes cluster ──► rollout ──► füstteszt (DoD)
```

## Projekt struktúra

| Útvonal | Tartalom |
|---|---|
| `app/service.py` | Üzleti logika (teendők, validáció, statisztika) |
| `app/__init__.py` | Flask REST API |
| `app/templates/index.html` | Webes felület |
| `tests/` | Unit és API tesztek (pytest) |
| `Dockerfile` | Konténer image leírás |
| `k8s/` | Kubernetes manifestek és a kind sandbox cluster konfigja |
| `scripts/smoke_test.sh` | Telepítés utáni füstteszt |
| `.github/workflows/ci-cd.yml` | A CI/CD pipeline definíció |

## Feltöltés GitHubra (első alkalommal)

1. Telepítsd a Gitet: https://git-scm.com/download/win
2. Hozz létre egy új, üres repositoryt a GitHubon (pl. `devops-teendo`), README nélkül.
3. A projekt mappájában:

```powershell
git init -b main
git add .
git commit -m "feat: teendőlista alkalmazás CI/CD pipeline-nal"
git remote add origin https://github.com/<felhasznalonev>/devops-teendo.git
git push -u origin main
```

4. A GitHubon az **Actions** fülön elindul a pipeline; zölden végződő `deploy` job = kész.

## Lokális futtatás (opcionális)

```powershell
python -m venv .venv; .venv\Scripts\activate; pip install -r requirements-dev.txt
pytest
flask --app app run --port 8080
```

Dockerrel: `docker build -t teendo-app .` majd `docker run -p 8080:8080 teendo-app`,
ezután: http://localhost:8080

## API

| Metódus | Útvonal | Leírás |
|---|---|---|
| GET | `/health` | Állapot és verzió |
| GET | `/api/todos?status=open\|done` | Teendők listája (szűrhető) |
| POST | `/api/todos` | Új teendő: `{"title": "...", "priority": "low\|normal\|high"}` |
| GET | `/api/todos/<id>` | Egy teendő |
| PATCH | `/api/todos/<id>` | Módosítás: `title`, `priority`, `done` |
| DELETE | `/api/todos/<id>` | Törlés |
| GET | `/api/stats` | Összes / kész / nyitott / készültség % |
