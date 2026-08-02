from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    DatabaseConnectionError,
    WorkspaceNotFoundError,
)
from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreate


class WorkspaceService:

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[Workspace]:

        result = await db.execute(
            select(Workspace)
        )

        return result.scalars().all()

    @staticmethod
    async def create(
        db: AsyncSession,
        data: WorkspaceCreate,
    ) -> Workspace:

        workspace = Workspace(
            title=data.title,
            description=data.description,
        )

        db.add(workspace)

        try:

            await db.commit()

        except Exception as e:

            await db.rollback()

            raise DatabaseConnectionError(
                technical=str(e),
            )

        await db.refresh(workspace)

        return workspace

    @staticmethod
    async def delete(
        db: AsyncSession,
        workspace_id: int,
    ):

        workspace = await db.get(
            Workspace,
            workspace_id,
        )

        if workspace is None:

            raise WorkspaceNotFoundError()

        await db.delete(workspace)

        try:

            await db.commit()

        except Exception as e:

            await db.rollback()

            raise DatabaseConnectionError(
                technical=str(e),
            )

        return {
            "success": True,
            "message": "Workspace deleted successfully.",
        }