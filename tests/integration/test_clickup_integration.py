import os
from typing import Dict, List, Optional

import pytest
from dotenv import load_dotenv

from src.services.clickup_service import ClickUpService
from src.types.clickup_types import CreateSpaceRequest, UpdateSpaceRequest

# Load environment variables
load_dotenv()

# This is an integration test suite that will make actual API calls to ClickUp
# It should only be run manually and with valid API credentials
# To run: pytest -xvs tests/integration/test_clickup_integration.py

pytestmark = pytest.mark.asyncio


@pytest.mark.skipif(
    not os.getenv("CLICKUP_API_KEY"), reason="No ClickUp API key provided"
)
class TestClickUpIntegration:
    """
    Integration tests for the ClickUp API.

    These tests make actual API calls and require a valid API key.
    They should be run manually and not in CI/CD pipelines without proper setup.
    """

    service: Optional[ClickUpService] = None
    workspace_id: Optional[str] = None
    created_resources: Dict[str, List[str]] = {"spaces": []}

    @pytest.fixture(autouse=True, scope="class")
    async def setup_class(self, request):
        """Set up the test class with API credentials."""
        api_key = os.getenv("CLICKUP_API_KEY")
        if not api_key:
            pytest.skip("ClickUp API key not provided")

        self.__class__.service = ClickUpService(api_key=api_key)
        self.__class__.created_resources = {"spaces": []}

        # We need a workspace ID for space operations
        self.__class__.workspace_id = os.getenv("CLICKUP_WORKSPACE_ID")
        if not self.__class__.workspace_id:
            # Try to get the first workspace
            response = await self.__class__.service.get_workspaces()
            if response is None or response.error or not response.data:
                pytest.skip("No workspace ID provided and couldn't retrieve workspaces")
            self.__class__.workspace_id = response.data[0].id
            print(f"Using workspace ID: {self.__class__.workspace_id}")

        yield

        # Cleanup after all tests
        for space_id in self.__class__.created_resources["spaces"]:
            try:
                await self.__class__.service.delete_space(space_id)
                print(f"Cleaned up space: {space_id}")
            except Exception as e:
                print(f"Failed to clean up space {space_id}: {e}")

    @pytest.mark.asyncio
    async def test_1_get_workspaces(self):
        """Test listing workspaces."""
        if not self.service:
            pytest.fail("Service not initialized")

        response = await self.service.get_workspaces()

        assert response.error is None
        assert response.status == 200
        assert isinstance(response.data, list)

        # Print workspaces for debugging
        print(f"Found {len(response.data)} workspaces:")
        for workspace in response.data:
            print(f"  - {workspace.name} (ID: {workspace.id})")

    @pytest.mark.asyncio
    async def test_2_get_workspace(self):
        """Test getting a single workspace."""
        if not self.service:
            pytest.fail("Service not initialized")

        # Skip if no workspace ID
        if not self.workspace_id:
            pytest.skip("No workspace ID available")

        response = await self.service.get_workspace(self.workspace_id)

        if response is None:
            pytest.fail("Failed to get workspace")

        # Debug the response structure
        print(f"Response data structure: {response.data}")

        assert response.error is None
        assert response.status == 200
        assert response.data is not None, "Response data is None"

        # The workspace data is nested under 'team' key
        assert hasattr(
            response.data, "team"
        ), "Expected 'team' attribute in response data"
        team = response.data.team

        # Verify the workspace ID
        assert (
            team.id == self.workspace_id
        ), f"Workspace ID mismatch. Expected {self.workspace_id}, got {team.id}"

        # Print workspace details
        print(f"Workspace details: {team.name} (ID: {team.id})")

    @pytest.mark.asyncio
    async def test_3_get_spaces(self):
        """Test getting spaces in a workspace."""
        if not self.service:
            pytest.fail("Service not initialized")

        # Skip if no workspace ID
        if not self.workspace_id:
            pytest.skip("No workspace ID available")

        response = await self.service.get_spaces(self.workspace_id)

        if response is None:
            pytest.fail("Failed to get spaces")

        assert response.error is None
        assert response.status == 200
        assert isinstance(response.data, list)

        # Print spaces for debugging
        print(f"Found {len(response.data)} spaces:")
        for space in response.data:
            print(f"  - {space.name} (ID: {space.id})")

    @pytest.mark.asyncio
    async def test_4_create_space(self):
        """Test creating a space in a workspace."""
        if not self.service:
            pytest.fail("Service not initialized")

        # Skip if no workspace ID
        if not self.workspace_id:
            pytest.skip("No workspace ID available")

        # Use a unique name with timestamp to avoid conflicts
        import time

        timestamp = int(time.time())
        space_name = f"Test Space API {timestamp}"
        create_request = CreateSpaceRequest(name=space_name, multiple_assignees=True)

        # Ensure workspace_id is not None
        assert self.workspace_id is not None, "Workspace ID cannot be None"

        response = await self.service.create_space(self.workspace_id, create_request)

        if response is None:
            pytest.fail("Failed to create space")

        # Debug the response structure
        print(f"Create space response: {response.data}")

        assert response.error is None, f"Error creating space: {response.error}"
        assert response.status == 200

        # Check if the response has the expected structure
        assert response.data is not None, "Response data is None"

        # Get the space ID safely
        space_id = response.data.id
        assert space_id is not None, "Space ID not found in response"

        # Verify the space name
        assert (
            response.data.name == space_name
        ), f"Space name mismatch. Expected {space_name}, got {response.data.name}"

        # Store for cleanup
        self.__class__.created_resources["spaces"].append(space_id)

        print(f"Created space: {space_name} (ID: {space_id})")

    @pytest.mark.asyncio
    async def test_5_get_space(self):
        """Test getting a single space."""
        if not self.service:
            pytest.fail("Service not initialized")

        # Skip if no spaces were created
        if not self.__class__.created_resources["spaces"]:
            pytest.skip("No spaces available to test")

        space_id = self.__class__.created_resources["spaces"][0]
        response = await self.service.get_space(space_id)

        if response is None:
            pytest.fail("Failed to get space")

        # Debug the response structure
        print(f"Get space response: {response.data}")

        assert response.error is None
        assert response.status == 200

        # Check if the response has the expected structure
        assert response.data is not None, "Response data is None"

        # Verify the space ID
        assert (
            response.data.id == space_id
        ), f"Space ID mismatch. Expected {space_id}, got {response.data.id}"

        # Print space details
        print(f"Space details: {response.data.name} (ID: {response.data.id})")

    @pytest.mark.asyncio
    async def test_6_update_space(self):
        """Test updating a space."""
        if not self.service:
            pytest.fail("Service not initialized")

        # Skip if no spaces were created
        if not self.__class__.created_resources["spaces"]:
            pytest.skip("No spaces available to update")

        space_id = self.__class__.created_resources["spaces"][0]
        import time

        timestamp = int(time.time())
        new_name = f"Updated Test Space {timestamp}"
        update_request = UpdateSpaceRequest(name=new_name, multiple_assignees=False)

        response = await self.service.update_space(space_id, update_request)

        if response is None:
            pytest.fail("Failed to update space")

        # Debug the response structure
        print(f"Update space response: {response.data}")

        assert response.error is None, f"Error updating space: {response.error}"
        assert response.status == 200

        # Verify the update
        get_response = await self.service.get_space(space_id)
        if get_response is None:
            pytest.fail("Failed to get updated space")

        # Debug the get response structure
        print(f"Get updated space response: {get_response.data}")

        # Check if the response has the expected structure
        assert get_response.data is not None, "Response data is None"

        # Verify the space name was updated
        assert (
            get_response.data.name == new_name
        ), f"Space name mismatch. Expected {new_name}, got {get_response.data.name}"

        # Verify multiple_assignees setting
        assert (
            get_response.data.multiple_assignees is False
        ), "multiple_assignees should be False"

        print(f"Updated space to: {new_name} (ID: {space_id})")

    @pytest.mark.asyncio
    async def test_7_delete_space(self):
        """Test deleting a space."""
        if not self.service:
            pytest.fail("Service not initialized")

        # Skip if no spaces were created
        if not self.__class__.created_resources["spaces"]:
            pytest.skip("No spaces available to delete")

        # Create an additional space specifically for deletion
        import time

        timestamp = int(time.time())
        space_name = f"Test Space for Deletion {timestamp}"
        create_request = CreateSpaceRequest(name=space_name)

        # Ensure workspace_id is not None
        assert self.workspace_id is not None, "Workspace ID cannot be None"

        create_response = await self.service.create_space(
            self.workspace_id, create_request
        )

        if create_response is None:
            pytest.fail("Failed to create space for deletion")

        # Debug the response structure
        print(f"Create space for deletion response: {create_response.data}")

        assert (
            create_response.error is None
        ), f"Error creating space: {create_response.error}"
        assert create_response.data is not None, "Response data is None"

        # Get the space ID safely
        space_id = create_response.data.id
        assert space_id is not None, "Space ID not found in response"

        # Delete the space
        delete_response = await self.service.delete_space(space_id)

        if delete_response is None:
            pytest.fail("Failed to delete space")

        # Debug the delete response structure
        print(f"Delete space response: {delete_response.data}")

        assert (
            delete_response.error is None
        ), f"Error deleting space: {delete_response.error}"
        assert delete_response.status == 200

        print(f"Deleted space: {space_name} (ID: {space_id})")

        # Try to get the space - should fail
        get_response = await self.service.get_space(space_id)

        # Debug the get response structure
        response_data = None
        if get_response is not None:
            response_data = get_response.data
        print(f"Get deleted space response: {response_data}")

        # Check if the space was actually deleted
        # The API might return a 404 error or an empty response
        if get_response and not get_response.error and get_response.data:
            pytest.fail("Space was not deleted")

        # Remove from cleanup list since we've already deleted it
        if space_id in self.__class__.created_resources["spaces"]:
            self.__class__.created_resources["spaces"].remove(space_id)

    @pytest.mark.asyncio
    async def test_8_get_tasks(self):
        """Test getting tasks from a list."""
        if not self.service:
            pytest.fail("Service not initialized")

        # This test requires an existing list ID
        list_id = os.getenv("CLICKUP_TEST_LIST_ID")
        if not list_id:
            pytest.skip("No test list ID provided")

        response = await self.service.get_tasks(list_id)

        if response is None:
            pytest.fail("Failed to get tasks")

        # Debug the response structure
        print(f"Get tasks response structure: {response.data}")

        assert response.error is None
        assert response.status == 200
        assert isinstance(response.data, list)

        # Print tasks for debugging
        print(f"Found {len(response.data)} tasks:")
        for task in response.data[:5]:  # Only show first 5 to prevent verbose output
            print(f"  - {task.name} (ID: {task.id})")
