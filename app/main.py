from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import DATABASE
from app.router import admin, auth, groups, message, role, task, user
from app.router.task import slot
from app.router.template.index import router as template

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
    return {"message": "Hello World"}


app.include_router(auth.router, prefix="")
app.include_router(admin.router, prefix="/admin")
app.include_router(groups.router, prefix="/groups")
app.include_router(slot.router, prefix="/{group_id}/slots")
app.include_router(task.router, prefix="/{group_id}/tasks")
app.include_router(template, prefix="/{group_id}/templates")
app.include_router(user.router, prefix="/{group_id}/users")
app.include_router(role.router, prefix="/{group_id}/roles")
app.include_router(message.router, prefix="/{group_id}/message")
