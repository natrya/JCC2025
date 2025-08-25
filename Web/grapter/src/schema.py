import uuid
from typing import List, Optional

import strawberry
from strawberry.schema.config import StrawberryConfig
from sqlalchemy import text
from sqlalchemy.orm import Session

from .db import SessionLocal, engine
from .models import User, Note


def get_db() -> Session:
    return SessionLocal()


def get_current_user_from_context(info) -> Optional[User]:
    request = info.context.get("request")
    username_token: Optional[str] = None
    if request is not None:
        # Accept either Authorization: Bearer <username> or X-Token: <username>
        auth = request.headers.get("Authorization")
        if auth and auth.lower().startswith("bearer "):
            username_token = auth.split(" ", 1)[1].strip()
        if username_token is None:
            username_token = request.headers.get("X-Token")

    if not username_token:
        return None

    with get_db() as db:
        return db.query(User).filter(User.username == username_token).first()


@strawberry.type
class UserType:
    id: int
    username: str
    role: str


@strawberry.type
class NoteType:
    id: str
    title: str
    content: str
    owner_id: int


@strawberry.type
class AuthPayload:
    token: str
    user: UserType


@strawberry.type
class Query:
    @strawberry.field
    def me(self, info) -> Optional[UserType]:
        user = get_current_user_from_context(info)
        if not user:
            return None
        return UserType(id=user.id, username=user.username, role=user.role)

    @strawberry.field
    def note_by_id(self, info, id: str) -> Optional[NoteType]:
        # IDOR: no ownership check; any authenticated user can fetch any note by UUID
        with get_db() as db:
            note = db.query(Note).filter(Note.id == id).first()
            if not note:
                return None
            return NoteType(
                id=note.id,
                title=note.title,
                content=note.content,
                owner_id=note.owner_id,
            )

    @strawberry.field
    def my_notes(self, info, owner_id: Optional[int] = None) -> List[NoteType]:
        # Insecure: allows specifying arbitrary owner_id to escalate
        with get_db() as db:
            if owner_id is None:
                user = get_current_user_from_context(info)
                if not user:
                    return []
                owner_id = user.id
            notes = db.query(Note).filter(Note.owner_id == owner_id).all()
            return [
                NoteType(id=n.id, title=n.title, content=n.content, owner_id=n.owner_id)
                for n in notes
            ]

    @strawberry.field
    def search_notes(self, info, text_query: str) -> List[NoteType]:
        # INTENTIONAL SQL INJECTION VULNERABILITY
        # This uses raw, concatenated SQL without parameters.
        insecure_sql = (
            "SELECT id, title, content, owner_id FROM notes "
            f"WHERE title LIKE '%{text_query}%' OR content LIKE '%{text_query}%'"
        )
        results: List[NoteType] = []
        with engine.connect() as conn:
            rows = conn.exec_driver_sql(insecure_sql).fetchall()
            for row in rows:
                # row order matches SELECT columns
                results.append(
                    NoteType(id=str(row[0]), title=str(row[1]), content=str(row[2]), owner_id=int(row[3]))
                )
        return results


@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(self, info, username: str, password: str, role: str = "user") -> AuthPayload:
        # Raw password storage on purpose for CTF
        with get_db() as db:
            existing = db.query(User).filter(User.username == username).first()
            if existing:
                # For simplicity, treat as login
                token = username
                return AuthPayload(token=token, user=UserType(id=existing.id, username=existing.username, role=existing.role))
            user = User(username=username, password=password, role=role)
            db.add(user)
            db.commit()
            db.refresh(user)
            token = username
            return AuthPayload(token=token, user=UserType(id=user.id, username=user.username, role=user.role))

    @strawberry.mutation
    def login(self, info, username: str, password: str) -> Optional[AuthPayload]:
        with get_db() as db:
            user = db.query(User).filter(User.username == username, User.password == password).first()
            if not user:
                return None
            token = username  # token is just the username for simplicity
            return AuthPayload(token=token, user=UserType(id=user.id, username=user.username, role=user.role))

    @strawberry.mutation
    def create_note(self, info, title: str, content: str) -> Optional[NoteType]:
        user = get_current_user_from_context(info)
        if not user:
            return None
        note_id = str(uuid.uuid4())
        with get_db() as db:
            note = Note(id=note_id, title=title, content=content, owner_id=user.id)
            db.add(note)
            db.commit()
            db.refresh(note)
            return NoteType(id=note.id, title=note.title, content=note.content, owner_id=note.owner_id)


schema = strawberry.Schema(query=Query, mutation=Mutation, config=StrawberryConfig(auto_camel_case=False))


