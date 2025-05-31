from dotenv import load_dotenv
from fastapi import FastAPI
from uvicorn import run
from core.config import settings
from starlette.middleware.sessions import SessionMiddleware

from api.v1.user import google_auth
from api.v1.user import user_routes
from api.v1.doc_management import doc_management_routes
from api.v1.generate_resume_text import generate_ai_text_route
from api.v1.history import history_routes
from api.v1.payment import payment_routes
load_dotenv()


app = FastAPI(title="RefineCV")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=settings.GOOGLE_CLIENT_SECRET)

app.include_router(google_auth.router, prefix="/v1/user", tags=["User"])

app.include_router(user_routes.router, prefix="/v1/user/profile", tags=["User Profile"])

app.include_router(doc_management_routes.router, prefix="/v1/doc", tags=["User Document Management"])

app.include_router(generate_ai_text_route.router, prefix="/v1/resume", tags=["Resume Management"])

app.include_router(history_routes.router, prefix="/v1/history", tags=["History"])


app.include_router(payment_routes.router, prefix="/v1/payment", tags=["Payment"])


@app.get('/')
def root():
    return {"message":f"Status: OK ✅"}



if __name__ == "__main__":
    run("main:app", host="localhost", port=8000, reload=True)