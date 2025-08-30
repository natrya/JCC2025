import random
import string
import uuid
from typing import List

from .db import SessionLocal, engine
from .models import User, Note, Base


def random_string(n: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits + " ", k=n)).strip()


def seed():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        # Clear existing data
        db.query(Note).delete()
        db.query(User).delete()
        db.commit()

        # Admin with flag as raw password
        flag = "JCC25{graphQL_iNj3c7i0n_&_ID0R_fun}"
        admin = User(username="admin", password=flag, role="admin")
        db.add(admin)
        db.commit()
        db.refresh(admin)

        # 19 regular users
        users: List[User] = [admin]
        for i in range(1, 20):
            u = User(username=f"user{i}", password=random_string(10), role="user")
            db.add(u)
            db.commit()
            db.refresh(u)
            users.append(u)

        # 100 notes distributed across users
        for i in range(100):
            owner = random.choice(users)
            note = Note(
                id=str(uuid.uuid4()),
                title=f"Note {i} of {owner.username}",
                content=random_string(60),
                owner_id=owner.id,
            )
            db.add(note)
        db.commit()


if __name__ == "__main__":
    seed()


