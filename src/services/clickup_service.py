from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    TypeVar,
    Union,
)

import httpx
from pydantic import BaseModel

from src.types.clickup_types import (
    ClickUpApiResponse,
    ClickUpFolder,
    ClickUpList,
    ClickUpSpace,
    ClickUpTask,
    ClickUpWorkspace,
    ClickUpWorkspaceResponse,
    CreateFolderRequest,
    CreateListRequest,
    CreateSpaceRequest,
    CreateTaskRequest,
    GetListsResponse,
    GetTasksResponse,
    UpdateFolderRequest,
    UpdateListRequest,
    UpdateSpaceRequest,
    UpdateTaskRequest,
)

T = TypeVar("T")


class ClickUpService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.clickup.com/api/v2"

    def _get_headers(self) -> dict:
        return {"Authorization": self.api_key, "Content-Type": "application/json"}

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        response_type: type[T],
        data_key: Optional[str] = None,
        **kwargs,
    ) -> ClickUpApiResponse[T]:
        """
        Makes a request to the ClickUp API with common error handling.

        Args:
            method: The HTTP method to use (get, post, put, delete)
            endpoint: The API endpoint to call
            response_type: The type to cast the response data to
            data_key: Optional key to extract data from the response (e.g. 'teams', 'spaces')
            **kwargs: Additional arguments to pass to the httpx request method

        Returns:
            A ClickUpApiResponse containing the response data or error
        """
        url = f"{self.base_url}/{endpoint}"

        if "headers" not in kwargs:
            kwargs["headers"] = self._get_headers()

        try:
            async with httpx.AsyncClient() as client:
                request_method = getattr(client, method.lower())
                response = await request_method(url, **kwargs)
                response.raise_for_status()

                if method.lower() == "delete":
                    # Delete operations typically don't return data
                    return ClickUpApiResponse[response_type](
                        status=response.status_code
                    )

                data = response.json()
                if data_key:
                    data = data[data_key]

                return ClickUpApiResponse[response_type](
                    data=data, status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[response_type](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[response_type](error=str(error), status=500)

    # Workspace operations (read-only)

    async def get_workspaces(self) -> ClickUpApiResponse[List[ClickUpWorkspace]]:
        """Get all workspaces"""
        return await self._make_request(
            "get", "team", List[ClickUpWorkspace], data_key="teams"
        )

    async def get_workspace(
        self, workspace_id: str
    ) -> ClickUpApiResponse[ClickUpWorkspaceResponse]:
        """Get a specific workspace by ID"""
        return await self._make_request(
            "get", f"team/{workspace_id}", ClickUpWorkspaceResponse
        )

    # Space operations (full CRUD)

    async def get_spaces(
        self, workspace_id: str
    ) -> ClickUpApiResponse[List[ClickUpSpace]]:
        """Get all spaces in a workspace"""
        return await self._make_request(
            "get", f"team/{workspace_id}/space", List[ClickUpSpace], data_key="spaces"
        )

    async def get_space(self, space_id: str) -> ClickUpApiResponse[ClickUpSpace]:
        """Get a specific space by ID"""
        return await self._make_request("get", f"space/{space_id}", ClickUpSpace)

    async def create_space(
        self, workspace_id: str, space: CreateSpaceRequest
    ) -> ClickUpApiResponse[ClickUpSpace]:
        """Create a new space in a workspace"""
        return await self._make_request(
            "post", f"team/{workspace_id}/space", ClickUpSpace, json=space.model_dump()
        )

    async def update_space(
        self, space_id: str, updates: UpdateSpaceRequest
    ) -> ClickUpApiResponse[ClickUpSpace]:
        """Update an existing space"""
        return await self._make_request(
            "put",
            f"space/{space_id}",
            ClickUpSpace,
            json=updates.model_dump(exclude_unset=True),
        )

    async def delete_space(self, space_id: str) -> ClickUpApiResponse[None]:
        """Delete a space"""
        return await self._make_request("delete", f"space/{space_id}", type(None))

    # Folder operations (full CRUD)

    async def get_folders(
        self, space_id: str
    ) -> ClickUpApiResponse[List[ClickUpFolder]]:
        """Get all folders in a space"""
        return await self._make_request(
            "get", f"space/{space_id}/folder", List[ClickUpFolder], data_key="folders"
        )

    async def get_folder(self, folder_id: str) -> ClickUpApiResponse[ClickUpFolder]:
        """Get a specific folder by ID"""
        return await self._make_request("get", f"folder/{folder_id}", ClickUpFolder)

    async def create_folder(
        self, space_id: str, folder: CreateFolderRequest
    ) -> ClickUpApiResponse[ClickUpFolder]:
        """Create a new folder in a space"""
        return await self._make_request(
            "post", f"space/{space_id}/folder", ClickUpFolder, json=folder.model_dump()
        )

    async def update_folder(
        self, folder_id: str, updates: UpdateFolderRequest
    ) -> ClickUpApiResponse[ClickUpFolder]:
        """Update an existing folder"""
        return await self._make_request(
            "put",
            f"folder/{folder_id}",
            ClickUpFolder,
            json=updates.model_dump(exclude_unset=True),
        )

    async def delete_folder(self, folder_id: str) -> ClickUpApiResponse[None]:
        """Delete a folder"""
        return await self._make_request("delete", f"folder/{folder_id}", type(None))

    # List operations (full CRUD)

    async def get_lists(self, folder_id: str) -> ClickUpApiResponse[GetListsResponse]:
        """Get all lists in a folder.

        Args:
            folder_id: The ID of the folder to get lists from.

        Returns:
            ClickUpApiResponse containing a GetListsResponse with the lists or error details.
        """
        return await self._make_request(
            "get", f"folder/{folder_id}/list", GetListsResponse
        )

    async def get_lists_in_space(
        self, space_id: str
    ) -> ClickUpApiResponse[GetListsResponse]:
        """Get all lists in a space (folderless lists).

        Args:
            space_id: The ID of the space to get lists from.

        Returns:
            ClickUpApiResponse containing a GetListsResponse with the lists or error details.
        """
        return await self._make_request(
            "get", f"space/{space_id}/list", GetListsResponse
        )

    async def get_list(self, list_id: str) -> ClickUpApiResponse[ClickUpList]:
        """Get a specific list by ID.

        Args:
            list_id: The ID of the list to retrieve.

        Returns:
            ClickUpApiResponse containing the list details or error details.
        """
        return await self._make_request("get", f"list/{list_id}", ClickUpList)

    async def create_list_in_folder(
        self, folder_id: str, list_data: CreateListRequest
    ) -> ClickUpApiResponse[ClickUpList]:
        """Create a new list in a folder.

        Args:
            folder_id: The ID of the folder to create the list in.
            list_data: CreateListRequest object containing the list details.
                Required fields:
                - name: List name
                Optional fields:
                - content: List description
                - due_date: Due date timestamp
                - priority: Priority level
                - assignee: Default assignee ID
                - status: Default status

        Returns:
            ClickUpApiResponse containing the created list or error details.
        """
        return await self._make_request(
            "post", f"folder/{folder_id}/list", ClickUpList, json=list_data.model_dump()
        )

    async def create_list_in_space(
        self, space_id: str, list_data: CreateListRequest
    ) -> ClickUpApiResponse[ClickUpList]:
        """Create a new list in a space (folderless).

        Args:
            space_id: The ID of the space to create the list in.
            list_data: CreateListRequest object containing the list details.
                Required fields:
                - name: List name
                Optional fields:
                - content: List description
                - due_date: Due date timestamp
                - priority: Priority level
                - assignee: Default assignee ID
                - status: Default status

        Returns:
            ClickUpApiResponse containing the created list or error details.
        """
        return await self._make_request(
            "post", f"space/{space_id}/list", ClickUpList, json=list_data.model_dump()
        )

    async def update_list(
        self, list_id: str, updates: UpdateListRequest
    ) -> ClickUpApiResponse[ClickUpList]:
        """Update an existing list"""
        return await self._make_request(
            "put",
            f"list/{list_id}",
            ClickUpList,
            json=updates.model_dump(exclude_unset=True),
        )

    async def delete_list(self, list_id: str) -> ClickUpApiResponse[None]:
        """Delete a list"""
        return await self._make_request("delete", f"list/{list_id}", type(None))

    # Task operations (full CRUD)

    async def get_tasks(
        self,
        list_id: str,
        archived: bool = False,
        page: int = 0,
        subtasks: bool = False,
    ) -> ClickUpApiResponse[GetTasksResponse]:
        """Get all tasks from a list.

        Args:
            list_id: The ID of the list to get tasks from.
            archived: Whether to include archived tasks.
            page: Page number for pagination (0-based).
            subtasks: Whether to include subtasks.

        Returns:
            ClickUpApiResponse containing a GetTasksResponse with tasks and pagination info.
        """
        params = {
            "archived": str(archived).lower(),
            "page": page,
            "subtasks": str(subtasks).lower(),
        }
        return await self._make_request(
            "get",
            f"list/{list_id}/task",
            GetTasksResponse,
            params=params,
        )

    async def get_task(self, task_id: str) -> ClickUpApiResponse[ClickUpTask]:
        """Get a specific task by ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            ClickUpApiResponse containing the task details or error details.
        """
        return await self._make_request("get", f"task/{task_id}", ClickUpTask)

    async def create_task(
        self, list_id: str, task: CreateTaskRequest
    ) -> ClickUpApiResponse[ClickUpTask]:
        """Create a new task in a list.

        Args:
            list_id: The ID of the list to create the task in.
            task: CreateTaskRequest object containing the task details.
                Required fields:
                - name: Task name/title
                Optional fields:
                - description: Task description
                - assignees: List of user IDs
                - status: Task status
                - priority: 1 (urgent) to 4 (low)
                - due_date: Unix timestamp in milliseconds
                - tags: List of tag names
                And more (see CreateTaskRequest for full list)

        Returns:
            ClickUpApiResponse containing the created task or error details.
        """
        return await self._make_request(
            "post",
            f"list/{list_id}/task",
            ClickUpTask,
            json=task.model_dump(exclude_unset=True),
        )

    async def update_task(
        self, task_id: str, updates: UpdateTaskRequest
    ) -> ClickUpApiResponse[ClickUpTask]:
        """Update an existing task.

        Args:
            task_id: The ID of the task to update.
            updates: UpdateTaskRequest object containing the fields to update.
                All fields are optional:
                - name: New task name
                - description: New description
                - status: New status
                - priority: New priority (1-4)
                - assignees: New complete list of assignees
                - add_assignees: List of assignees to add
                - remove_assignees: List of assignees to remove

        Returns:
            ClickUpApiResponse containing the updated task or error details.
        """
        return await self._make_request(
            "put",
            f"task/{task_id}",
            ClickUpTask,
            json=updates.model_dump(exclude_unset=True),
        )

    async def delete_task(self, task_id: str) -> ClickUpApiResponse[None]:
        """Delete a task.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            ClickUpApiResponse containing the deletion status or error details.
        """
        return await self._make_request("delete", f"task/{task_id}", type(None))

    async def add_task_comment(
        self, task_id: str, comment_text: str
    ) -> ClickUpApiResponse[Dict[str, Any]]:
        """Add a comment to a task.

        Args:
            task_id: The ID of the task to comment on.
            comment_text: The text content of the comment.
                Supports markdown formatting.

        Returns:
            ClickUpApiResponse containing the created comment details or error details.
        """
        return await self._make_request(
            "post",
            f"task/{task_id}/comment",
            Dict[str, Any],
            json={"comment_text": comment_text},
        )

    async def get_task_comments(
        self, task_id: str
    ) -> ClickUpApiResponse[List[Dict[str, Any]]]:
        """Get comments for a task.

        Args:
            task_id: The ID of the task to get comments from.

        Returns:
            ClickUpApiResponse containing a list of comments or error details.
            Each comment is a dictionary with fields like:
            - id: Comment ID
            - comment_text: The text content
            - user: User who created the comment
            - date: Creation timestamp
        """
        return await self._make_request(
            "get", f"task/{task_id}/comment", List[Dict[str, Any]], data_key="comments"
        )

    async def set_task_dependencies(
        self,
        task_id: str,
        depends_on: Optional[List[str]] = None,
        dependency_of: Optional[List[str]] = None,
    ) -> ClickUpApiResponse[Dict[str, Any]]:
        """Set task dependencies.

        Args:
            task_id: The ID of the task to set dependencies for.
            depends_on: List of task IDs that this task depends on.
            dependency_of: List of task IDs that depend on this task.

        Returns:
            ClickUpApiResponse containing the updated dependency details or error details.
        """
        data = {}
        if depends_on:
            data["depends_on"] = depends_on
        if dependency_of:
            data["dependency_of"] = dependency_of

        return await self._make_request(
            "post", f"task/{task_id}/dependency", Dict[str, Any], json=data
        )
