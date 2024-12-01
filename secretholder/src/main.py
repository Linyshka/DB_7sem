from uvicorn import run

from settings import settings

if __name__ == "__main__":
    run(
        "app:app",
        host=settings.PWD_MANAGER_HOST,
        port=settings.PWD_MANAGER_PORT,
    )
