from fastapi import APIRouter
from app.schemas.task_schema import TaskResponse
from app.handlers.task_handler import create_task, get_one, get_all, update_task, delete_task
router = APIRouter(prefix="/tasks", tags=["Tasks"])


router.post("/", response_model=TaskResponse, status_code=201)(create_task)
router.get("/{id}", response_model=TaskResponse)(get_one)
router.get("/", response_model=list[TaskResponse])(get_all)
router.put("/{id}", response_model=TaskResponse)(update_task)
router.delete("/{id}")(delete_task)
