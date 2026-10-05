# app/services/task_service.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task_schema import Task, TaskUpdate
from app.models.task_model import TaskModel


# Every query is filtered by user_id, so a user can only see and change their own tasks.
class TaskService:
    @staticmethod
    async def create_task(task: Task, user_id: int, db: AsyncSession):
        task_model = TaskModel(
            title=task.title,
            description=task.description,
            user_id=user_id,
        )
        db.add(task_model)
        await db.commit()
        await db.refresh(task_model)
        return task_model


    @staticmethod
    async def get_one(task_id: int, user_id: int, db: AsyncSession):
        result = await db.execute(
            select(TaskModel)
            .where(TaskModel.id == task_id, TaskModel.user_id == user_id)
        )
        return result.scalar_one_or_none()


    @staticmethod
    async def get_all(user_id: int, db: AsyncSession):
        result = await db.execute(
            select(TaskModel)
            .where(TaskModel.user_id == user_id)
            .order_by(TaskModel.id)
        )
        return result.scalars().all()


    @staticmethod
    async def update_task(task_id: int, data: TaskUpdate, user_id: int, db: AsyncSession):
        task_model = await TaskService.get_one(task_id, user_id, db)
        if task_model is None:
            return None

        update_data = data.model_dump(exclude_unset=True)
        # Keep status and completed in sync, whichever one the client sent
        if update_data.get("status") is not None:
            update_data["completed"] = update_data["status"] == "completed"
        elif update_data.get("completed") is not None:
            update_data["status"] = "completed" if update_data["completed"] else "pending"

        for field, value in update_data.items():
            setattr(task_model, field, value)

        await db.commit()
        await db.refresh(task_model)
        return task_model


    @staticmethod
    async def delete_task(task_id: int, user_id: int, db: AsyncSession):
        task_model = await TaskService.get_one(task_id, user_id, db)
        if task_model is None:
            return False

        await db.delete(task_model)
        await db.commit()
        return True
