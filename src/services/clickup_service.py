from typing import Any, Dict, List, Optional, Union

import httpx

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
    UpdateFolderRequest,
    UpdateListRequest,
    UpdateSpaceRequest,
)


class ClickUpService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.clickup.com/api/v2"

    def _get_headers(self) -> dict:
        return {"Authorization": self.api_key, "Content-Type": "application/json"}

    # Workspace operations (read-only)

    async def get_workspaces(self) -> ClickUpApiResponse[List[ClickUpWorkspace]]:
        """
        Get all workspaces
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/team", headers=self._get_headers()
                )
                response.raise_for_status()

                return ClickUpApiResponse[List[ClickUpWorkspace]](
                    data=response.json()["teams"], status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[List[ClickUpWorkspace]](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[List[ClickUpWorkspace]](
                error=str(error), status=500
            )

    async def get_workspace(
        self, workspace_id: str
    ) -> ClickUpApiResponse[ClickUpWorkspaceResponse]:
        """
        Get a specific workspace by ID
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/team/{workspace_id}", headers=self._get_headers()
                )
                response.raise_for_status()

                return ClickUpApiResponse[ClickUpWorkspaceResponse](
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[ClickUpWorkspaceResponse](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[ClickUpWorkspaceResponse](
                error=str(error), status=500
            )

    # Space operations (full CRUD)

    async def get_spaces(
        self, workspace_id: str
    ) -> ClickUpApiResponse[List[ClickUpSpace]]:
        """
        Get all spaces in a workspace
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/team/{workspace_id}/space",
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[List[ClickUpSpace]](
                    data=response.json()["spaces"], status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[List[ClickUpSpace]](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[List[ClickUpSpace]](error=str(error), status=500)

    async def get_space(self, space_id: str) -> ClickUpApiResponse[ClickUpSpace]:
        """
        Get a specific space by ID
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/space/{space_id}", headers=self._get_headers()
                )
                response.raise_for_status()

                return ClickUpApiResponse[ClickUpSpace](
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[ClickUpSpace](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[ClickUpSpace](error=str(error), status=500)

    async def create_space(
        self, workspace_id: str, space: CreateSpaceRequest
    ) -> ClickUpApiResponse[ClickUpSpace]:
        """
        Create a new space in a workspace
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/team/{workspace_id}/space",
                    json=space.model_dump(),
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[ClickUpSpace](
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[ClickUpSpace](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[ClickUpSpace](error=str(error), status=500)

    async def update_space(
        self, space_id: str, updates: UpdateSpaceRequest
    ) -> ClickUpApiResponse[ClickUpSpace]:
        """
        Update an existing space
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{self.base_url}/space/{space_id}",
                    json=updates.model_dump(exclude_unset=True),
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[ClickUpSpace](
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[ClickUpSpace](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[ClickUpSpace](error=str(error), status=500)

    async def delete_space(self, space_id: str) -> ClickUpApiResponse[None]:
        """
        Delete a space
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.base_url}/space/{space_id}",
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[None](status=response.status_code)
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[None](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[None](error=str(error), status=500)

    # Folder operations (full CRUD)

    async def get_folders(
        self, space_id: str
    ) -> ClickUpApiResponse[List[ClickUpFolder]]:
        """
        Get all folders in a space
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/space/{space_id}/folder",
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[List[ClickUpFolder]](
                    data=response.json()["folders"], status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[List[ClickUpFolder]](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[List[ClickUpFolder]](error=str(error), status=500)

    async def get_folder(self, folder_id: str) -> ClickUpApiResponse[ClickUpFolder]:
        """
        Get a specific folder by ID
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/folder/{folder_id}", headers=self._get_headers()
                )
                response.raise_for_status()

                return ClickUpApiResponse[ClickUpFolder](
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[ClickUpFolder](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[ClickUpFolder](error=str(error), status=500)

    async def create_folder(
        self, space_id: str, folder: CreateFolderRequest
    ) -> ClickUpApiResponse[ClickUpFolder]:
        """
        Create a new folder in a space
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/space/{space_id}/folder",
                    json=folder.model_dump(),
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[ClickUpFolder](
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[ClickUpFolder](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[ClickUpFolder](error=str(error), status=500)

    async def update_folder(
        self, folder_id: str, updates: UpdateFolderRequest
    ) -> ClickUpApiResponse[ClickUpFolder]:
        """
        Update an existing folder
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{self.base_url}/folder/{folder_id}",
                    json=updates.model_dump(exclude_unset=True),
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[ClickUpFolder](
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[ClickUpFolder](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[ClickUpFolder](error=str(error), status=500)

    async def delete_folder(self, folder_id: str) -> ClickUpApiResponse[None]:
        """
        Delete a folder
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.base_url}/folder/{folder_id}",
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[None](status=response.status_code)
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[None](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[None](error=str(error), status=500)

    # List operations (full CRUD)

    async def get_lists(self, folder_id: str) -> ClickUpApiResponse[List[ClickUpList]]:
        """
        Get all lists in a folder
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/folder/{folder_id}/list",
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[List[ClickUpList]](
                    data=response.json()["lists"], status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[List[ClickUpList]](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[List[ClickUpList]](error=str(error), status=500)

    async def get_lists_in_space(
        self, space_id: str
    ) -> ClickUpApiResponse[List[ClickUpList]]:
        """
        Get all lists in a space (folderless lists)
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/space/{space_id}/list",
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[List[ClickUpList]](
                    data=response.json()["lists"], status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[List[ClickUpList]](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[List[ClickUpList]](error=str(error), status=500)

    async def get_list(self, list_id: str) -> ClickUpApiResponse[ClickUpList]:
        """
        Get a specific list by ID
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/list/{list_id}", headers=self._get_headers()
                )
                response.raise_for_status()

                return ClickUpApiResponse[ClickUpList](
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[ClickUpList](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[ClickUpList](error=str(error), status=500)

    async def create_list_in_folder(
        self, folder_id: str, list_data: CreateListRequest
    ) -> ClickUpApiResponse[ClickUpList]:
        """
        Create a new list in a folder
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/folder/{folder_id}/list",
                    json=list_data.model_dump(),
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[ClickUpList](
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[ClickUpList](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[ClickUpList](error=str(error), status=500)

    async def create_list_in_space(
        self, space_id: str, list_data: CreateListRequest
    ) -> ClickUpApiResponse[ClickUpList]:
        """
        Create a new list in a space (folderless)
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/space/{space_id}/list",
                    json=list_data.model_dump(),
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[ClickUpList](
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[ClickUpList](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[ClickUpList](error=str(error), status=500)

    async def update_list(
        self, list_id: str, updates: UpdateListRequest
    ) -> ClickUpApiResponse[ClickUpList]:
        """
        Update an existing list
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{self.base_url}/list/{list_id}",
                    json=updates.model_dump(exclude_unset=True),
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[ClickUpList](
                    data=response.json(), status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[ClickUpList](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[ClickUpList](error=str(error), status=500)

    async def delete_list(self, list_id: str) -> ClickUpApiResponse[None]:
        """
        Delete a list
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self.base_url}/list/{list_id}",
                    headers=self._get_headers(),
                )
                response.raise_for_status()

                return ClickUpApiResponse[None](status=response.status_code)
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[None](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[None](error=str(error), status=500)

    # Task operations

    async def get_tasks(self, list_id: str) -> ClickUpApiResponse[List[ClickUpTask]]:
        """
        Get all tasks from a list
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/list/{list_id}/task", headers=self._get_headers()
                )
                response.raise_for_status()

                return ClickUpApiResponse[List[ClickUpTask]](
                    data=response.json()["tasks"], status=response.status_code
                )
        except httpx.HTTPStatusError as error:
            return ClickUpApiResponse[List[ClickUpTask]](
                error=(
                    error.response.json().get("err") if error.response else str(error)
                ),
                status=error.response.status_code if error.response else 500,
            )
        except httpx.RequestError as error:
            return ClickUpApiResponse[List[ClickUpTask]](error=str(error), status=500)
