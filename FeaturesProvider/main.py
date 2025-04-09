from ai import request_model
from fastapi import FastAPI, HTTPException, status

app = FastAPI()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello"}


@app.post("/greet", status_code=status.HTTP_200_OK)
def greet(payload: dict[str, str]) -> dict[str, str]:
    name = payload.get("name")
    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required"
        )

    greeting = request_model(name)
    if greeting is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is currently unavailable",
        )
    return {"message": greeting}
