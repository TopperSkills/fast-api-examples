from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db import get_db
from app.services.task_service import TaskService
from app.schemas.task_schema import Task, TaskUpdate
from app.models.user_model import UserModel
# All task routes are protected: they need "Authorization: Bearer <token>",
# and current_user decides whose tasks are read or changed.
from app.core.deps import get_current_user


async def create_task(task: Task, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return await TaskService.create_task(task, current_user.id, db)


async def get_one(id: int, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    task = await TaskService.get_one(id, current_user.id, db)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def get_all(db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return await TaskService.get_all(current_user.id, db)


async def update_task(id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    updated_task = await TaskService.update_task(id, task, current_user.id, db)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


async def delete_task(id: int, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    deleted = await TaskService.delete_task(id, current_user.id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task Deleted"}
