from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from routes import events, users, tickets, auth
import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.exception_handler(Exception)
def handle_exception(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "message": f"Failed to process request: {request.method} {request.url}. Details: {exc}"
        },
    )


app.include_router(auth.router)
app.include_router(events.router)
app.include_router(users.router)
app.include_router(tickets.router)


@app.get("/")
def index():
    return {"message": "Hello world"}


# @app.get("/bookings")
# def get_bookings(token: str = Depends(oauth2_scheme)):
#     return {"token": token}

# @app.get("/users")
# async def get_users(user: get_current_user = Depends()):
#     return {"user": user}
