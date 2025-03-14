from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, Field


class ClickUpWorkspace(BaseModel):
    id: str
    name: str
    color: Optional[str] = None
    avatar: Optional[str] = None
    members: Optional[List[Dict[str, Any]]] = None


class ClickUpTeam(BaseModel):
    """Team represents a workspace in ClickUp API."""

    id: str
    name: str
    color: Optional[str] = None
    avatar: Optional[str] = None
    members: Optional[List[Dict[str, Any]]] = None
    roles: Optional[List[Dict[str, Any]]] = None


class ClickUpWorkspaceResponse(BaseModel):
    """Response structure for a single workspace."""

    team: ClickUpTeam


class ClickUpSpace(BaseModel):
    id: str
    name: str
    private: Optional[bool] = None
    statuses: Optional[List[Dict[str, Any]]] = None
    multiple_assignees: Optional[bool] = None
    features: Optional[Dict[str, Any]] = None
    archived: Optional[bool] = None


class CreateSpaceRequest(BaseModel):
    name: str
    multiple_assignees: Optional[bool] = None


class UpdateSpaceRequest(BaseModel):
    name: Optional[str] = None
    multiple_assignees: Optional[bool] = None


# Generic response type for API responses
T = TypeVar("T")


class ClickUpApiResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    error: Optional[str] = None
    status: int


class ClickUpTask(BaseModel):
    id: str
    name: str
    status: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    tags: Optional[List[str]] = None
    priority: Optional[str] = None
    assignees: Optional[List[Dict[str, Any]]] = None


class CreateTaskRequest(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    due_date: Optional[str] = None
    time_estimate: Optional[int] = None
    assignees: Optional[List[int]] = None
    tags: Optional[List[str]] = None


class UpdateTaskRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    due_date: Optional[str] = None
    time_estimate: Optional[int] = None
    assignees: Optional[List[int]] = None
    add_assignees: Optional[List[int]] = None
    remove_assignees: Optional[List[int]] = None


class ClickUpList(BaseModel):
    id: str
    name: str
    content: Optional[str] = None
    status: Optional[Dict[str, Any]] = None
    priority: Optional[Dict[str, Any]] = None
    assignee: Optional[Dict[str, Any]] = None
    task_count: Optional[int] = None
    due_date: Optional[str] = None
    start_date: Optional[str] = None
    folder: Optional[Dict[str, Any]] = None
    space: Optional[Dict[str, Any]] = None
    archived: Optional[bool] = None


class CreateListRequest(BaseModel):
    name: str
    content: Optional[str] = None
    due_date: Optional[int] = None
    priority: Optional[int] = None
    assignee: Optional[int] = None
    status: Optional[str] = None
