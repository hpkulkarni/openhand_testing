"""Configuration Admin Tool - FastAPI entry point."""
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Cookie, Depends, FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import auth
from app.db import connect, init_db
from app.schemas import ConfigIn, LoginIn, validate_value

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Configuration Admin Tool", lifespan=lifespan)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/auth/login")
def login(body: LoginIn, response: Response) -> dict:
    with connect() as conn:
        row = conn.execute(
            "SELECT id, username, role, password_hash FROM users WHERE username = ?",
            (body.username,),
        ).fetchone()
    if row is None or not auth.verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = auth.create_session(row["id"])
    response.set_cookie(auth.SESSION_COOKIE, token, httponly=True, samesite="lax")
    return {"username": row["username"], "role": row["role"]}


@app.post("/api/auth/logout")
def logout(response: Response, _: dict = Depends(auth.current_user),
           session: str | None = Cookie(default=None)) -> dict:
    if session:
        auth.delete_session(session)
    response.delete_cookie(auth.SESSION_COOKIE)
    return {"status": "logged out"}


@app.get("/api/auth/me")
def me(user: dict = Depends(auth.current_user)) -> dict:
    return {"username": user["username"], "role": user["role"]}


@app.get("/api/configs")
def list_configs(environment: str | None = None, q: str | None = None,
                 _: dict = Depends(auth.current_user)) -> list[dict]:
    sql, params = "SELECT * FROM configs WHERE 1=1", []
    if environment:
        sql += " AND environment = ?"
        params.append(environment)
    if q:
        sql += " AND key LIKE ?"
        params.append(f"%{q}%")
    sql += " ORDER BY key, environment"
    with connect() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]


@app.get("/api/configs/{config_id}")
def get_config(config_id: int, _: dict = Depends(auth.current_user)) -> dict:
    with connect() as conn:
        row = conn.execute("SELECT * FROM configs WHERE id = ?", (config_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Config not found")
    return dict(row)


def _check_value(body: ConfigIn) -> None:
    error = validate_value(body.value, body.value_type)
    if error:
        raise HTTPException(status_code=422, detail=error)


@app.post("/api/configs", status_code=201)
def create_config(body: ConfigIn, user: dict = Depends(auth.require_admin)) -> dict:
    _check_value(body)
    try:
        with connect() as conn:
            cur = conn.execute(
                "INSERT INTO configs (key, value, value_type, environment, description, updated_by) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (body.key, body.value, body.value_type, body.environment,
                 body.description, user["username"]),
            )
            row = conn.execute("SELECT * FROM configs WHERE id = ?", (cur.lastrowid,)).fetchone()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="key already exists for this environment")
    return dict(row)


@app.put("/api/configs/{config_id}")
def update_config(config_id: int, body: ConfigIn, user: dict = Depends(auth.require_admin)) -> dict:
    _check_value(body)
    try:
        with connect() as conn:
            cur = conn.execute(
                "UPDATE configs SET key=?, value=?, value_type=?, environment=?, description=?, "
                "updated_at=datetime('now'), updated_by=? WHERE id=?",
                (body.key, body.value, body.value_type, body.environment,
                 body.description, user["username"], config_id),
            )
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Config not found")
            row = conn.execute("SELECT * FROM configs WHERE id = ?", (config_id,)).fetchone()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="key already exists for this environment")
    return dict(row)


@app.delete("/api/configs/{config_id}", status_code=204)
def delete_config(config_id: int, _: dict = Depends(auth.require_admin)) -> Response:
    with connect() as conn:
        cur = conn.execute("DELETE FROM configs WHERE id = ?", (config_id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Config not found")
    return Response(status_code=204)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "login.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
