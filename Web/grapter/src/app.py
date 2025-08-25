from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter

from .schema import schema
from .db import Base, engine


# Ensure tables exist
Base.metadata.create_all(bind=engine)

def get_context(request: Request):
    return {"request": request}

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)

app = FastAPI(title="Grapter CTF GraphQL API")

app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def root():
    return {"message": "Grapter CTF GraphQL running. Visit /graphql"}


