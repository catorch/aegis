from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel


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


class ClickUpFolder(BaseModel):
    id: str
    name: str
    orderindex: Optional[int] = None
    override_statuses: Optional[bool] = None
    hidden: Optional[bool] = None
    space: Optional[Dict[str, Any]] = None
    task_count: Optional[str] = None
    archived: Optional[bool] = None
    statuses: Optional[List[Dict[str, Any]]] = None
    lists: Optional[List[Dict[str, Any]]] = None


class CreateFolderRequest(BaseModel):
    name: str
    hidden: Optional[bool] = None


class UpdateFolderRequest(BaseModel):
    name: Optional[str] = None
    hidden: Optional[bool] = None


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


class UpdateListRequest(BaseModel):
    """
    Request model for updating a ClickUp list.

    Attributes:
        name: The new name for the list.
        content: The new content (description) for the list.
        due_date: The due date as a UNIX timestamp in milliseconds.
        due_date_time: Whether the due date includes a time component.
        priority: The priority level (1-4, where 1 is urgent).
        assignee: User ID to assign as the default assignee.
        unset_status: Whether to unset the default status.
        status: The new default status.
    """

    name: Optional[str] = None
    content: Optional[str] = None
    due_date: Optional[int] = None
    due_date_time: Optional[bool] = None
    priority: Optional[int] = None
    assignee: Optional[int] = None
    unset_status: Optional[bool] = None
    status: Optional[str] = None


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


# Generic response type for API responses
T = TypeVar("T")


class ClickUpApiResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    error: Optional[str] = None
    status: int
