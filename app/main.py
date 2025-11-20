from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import DATABASE
from app.router import message
from app.router.admin.index import router as admin
from app.router.auth.index import router as auth
from app.router.group.index import router as group
from app.router.shift.index import router as shift
from app.router.task.index import router as task
from app.router.template.index import router as template
from app.router.user.index import router as user

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def handler(request: Request, exc: RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


origins = ["http://next:3000", DATABASE, "http://localhost:3000", "http://localhost:5432"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello Proletariat"}


app.include_router(auth, prefix="")
app.include_router(admin, prefix="/admin")
app.include_router(group, prefix="/groups")
app.include_router(user, prefix="/user")
app.include_router(shift, prefix="/shifts")
app.include_router(task, prefix="/tasks")
app.include_router(template, prefix="/templates")
app.include_router(message.router, prefix="/message")

