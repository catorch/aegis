from typing import Any, Dict, List, Optional, Union

import httpx

from src.types.clickup_types import (
    ClickUpApiResponse,
    CreateListRequest,
    CreateTaskRequest,
    CreateWorkspaceRequest,
    UpdateTaskRequest,
    UpdateWorkspaceRequest,
)


class ClickUpService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.clickup.com/api/v2"

    def _get_headers(self) -> dict:
        return {"Authorization": self.api_key, "Content-Type": "application/json"}

    async def get_workspaces(self) -> ClickUpApiResponse:
        """
        Get all workspaces
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/team", headers=self._get_headers()
                )
                response.raise_for_status()

                return ClickUpApiResponse(
                    data=response.json()["teams"], status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse(
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse(error=str(error), status=500)

    async def get_workspace(self, workspace_id: str) -> ClickUpApiResponse:
        """
        Get a specific workspace by ID
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/team/{workspace_id}", headers=self._get_headers()
                )
                response.raise_for_status()

                return ClickUpApiResponse(
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse(
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse(error=str(error), status=500)

    async def create_workspace(
        self, workspace: CreateWorkspaceRequest
    ) -> ClickUpApiResponse:
        """
        Create a new workspace
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/team",
                    json=workspace.dict(),
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse(
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse(
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse(error=str(error), status=500)

    async def update_workspace(
        self, workspace_id: str, updates: UpdateWorkspaceRequest
    ) -> ClickUpApiResponse:
        """
        Update an existing workspace
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{self.base_url}/team/{workspace_id}",
                    json=updates.dict(),
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse(
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse(
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse(error=str(error), status=500)

    async def delete_workspace(self, workspace_id: str) -> ClickUpApiResponse:
        """
        Delete a workspace
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.base_url}/team/{workspace_id}", headers=self._get_headers()
                )
                response.raise_for_status()

                return ClickUpApiResponse(status=response.status_code)
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse(
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse(error=str(error), status=500)

    # Task operations

    async def get_tasks(self, list_id: str) -> ClickUpApiResponse:
        """
        Get all tasks from a list
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/list/{list_id}/task", headers=self._get_headers()
                )
                response.raise_for_status()

                return ClickUpApiResponse(
                    data=response.json()["tasks"], status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse(
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse(error=str(error), status=500)

    async def get_task(self, task_id: str) -> ClickUpApiResponse:
        """
        Get a specific task by ID
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/task/{task_id}", headers=self._get_headers()
                )
                response.raise_for_status()

                return ClickUpApiResponse(
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse(
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse(error=str(error), status=500)

    async def create_task(
        self, list_id: str, task: CreateTaskRequest
    ) -> ClickUpApiResponse:
        """
        Create a new task in a list
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/list/{list_id}/task",
                    json=task.dict(),
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse(
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse(
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse(error=str(error), status=500)

    async def update_task(
        self, task_id: str, updates: UpdateTaskRequest
    ) -> ClickUpApiResponse:
        """
        Update an existing task
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{self.base_url}/task/{task_id}",
                    json=updates.dict(exclude_unset=True),
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse(
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse(
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse(error=str(error), status=500)

    async def delete_task(self, task_id: str) -> ClickUpApiResponse:
        """
        Delete a task
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.base_url}/task/{task_id}", headers=self._get_headers()
                )
                response.raise_for_status()

                return ClickUpApiResponse(status=response.status_code)
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse(
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse(error=str(error), status=500)
