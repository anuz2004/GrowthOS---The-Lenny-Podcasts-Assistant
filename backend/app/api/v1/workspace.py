from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse,
)
from app.services.workspace_service import WorkspaceService

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)


@router.get(
    "/",
    response_model=list[WorkspaceResponse],
    summary="Get all workspaces",
)
async def get_workspaces(
    db: AsyncSession = Depends(get_db),
):
    return await WorkspaceService.get_all(db)


@router.post(
    "/",
    response_model=WorkspaceResponse,
    summary="Create a new workspace",
)
async def create_workspace(
    workspace: WorkspaceCreate,
    db: AsyncSession = Depends(get_db),
):
    return await WorkspaceService.create(db, workspace)


@router.delete(
    "/{workspace_id}",
    summary="Delete a workspace",
)
async def delete_workspace(
    workspace_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await WorkspaceService.delete(
        db,
        workspace_id,
    )