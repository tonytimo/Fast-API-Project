from fastapi import FastAPI
from router import get_router

app = FastAPI()

# Include the router from router.py
app.include_router(get_router())


def get_app() -> FastAPI:
    return app


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to the FastAPI app!"}
