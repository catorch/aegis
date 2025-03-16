from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel


class ClickUpWorkspace(BaseModel):
    """Represents a ClickUp workspace.

    Attributes:
        id: Unique identifier for the workspace.
        name: Name of the workspace.
        color: Color code associated with the workspace.
        avatar: URL to the workspace's avatar image.
        members: List of members in the workspace with their details.
    """

    id: str
    name: str
    color: Optional[str] = None
    avatar: Optional[str] = None
    members: Optional[List[Dict[str, Any]]] = None


class ClickUpTeam(BaseModel):
    """Team represents a workspace in ClickUp API.

    Attributes:
        id: Unique identifier for the team.
        name: Name of the team.
        color: Color code associated with the team.
        avatar: URL to the team's avatar image.
        members: List of team members with their details.
        roles: List of roles defined in the team.
    """

    id: str
    name: str
    color: Optional[str] = None
    avatar: Optional[str] = None
    members: Optional[List[Dict[str, Any]]] = None
    roles: Optional[List[Dict[str, Any]]] = None


class ClickUpWorkspaceResponse(BaseModel):
    """Response structure for a single workspace.

    Attributes:
        team: The team/workspace details returned by the API.
    """

    team: ClickUpTeam


class ClickUpSpace(BaseModel):
    """Represents a space within a ClickUp workspace.

    Attributes:
        id: Unique identifier for the space.
        name: Name of the space.
        private: Whether the space is private.
        statuses: List of available statuses in the space.
        multiple_assignees: Whether tasks can have multiple assignees.
        features: Dictionary of enabled features.
        archived: Whether the space is archived.
    """

    id: str
    name: str
    private: Optional[bool] = None
    statuses: Optional[List[Dict[str, Any]]] = None
    multiple_assignees: Optional[bool] = None
    features: Optional[Dict[str, Any]] = None
    archived: Optional[bool] = None


class CreateSpaceRequest(BaseModel):
    """Request model for creating a ClickUp space.

    Attributes:
        name: The name of the space (required).
        multiple_assignees: Whether to allow multiple assignees on tasks.
    """

    name: str
    multiple_assignees: Optional[bool] = None


class UpdateSpaceRequest(BaseModel):
    """Request model for updating a ClickUp space.

    Attributes:
        name: New name for the space.
        multiple_assignees: Whether to allow multiple assignees on tasks.
    """

    name: Optional[str] = None
    multiple_assignees: Optional[bool] = None


class ClickUpFolder(BaseModel):
    """Represents a folder within a ClickUp space.

    Attributes:
        id: Unique identifier for the folder.
        name: Name of the folder.
        orderindex: Position of the folder in the space.
        override_statuses: Whether the folder has custom statuses.
        hidden: Whether the folder is hidden.
        space: Details of the parent space.
        task_count: Number of tasks in the folder.
        archived: Whether the folder is archived.
        statuses: List of available statuses.
        lists: List of lists within the folder.
    """

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
    """Request model for creating a ClickUp folder.

    Attributes:
        name: The name of the folder (required).
        hidden: Whether the folder should be hidden.
    """

    name: str
    hidden: Optional[bool] = None


class UpdateFolderRequest(BaseModel):
    """Request model for updating a ClickUp folder.

    Attributes:
        name: New name for the folder.
        hidden: Whether the folder should be hidden.
    """

    name: Optional[str] = None
    hidden: Optional[bool] = None


class ClickUpListLocation(BaseModel):
    """Represents a location reference (folder/space) in a ClickUp list.

    Attributes:
        id: Unique identifier for the location.
        name: Name of the location.
        hidden: Whether the location is hidden (folders only).
        access: Whether the user has access to this location.
    """

    id: str
    name: str
    hidden: Optional[bool] = None
    access: bool


class ClickUpList(BaseModel):
    """Represents a list within a ClickUp folder or space.

    Attributes:
        id: Unique identifier for the list.
        name: Name of the list.
        orderindex: Position of the list in the folder/space.
        status: Default status configuration.
        priority: Default priority configuration.
        assignee: Default assignee configuration.
        task_count: Number of tasks in the list.
        due_date: Default due date for tasks.
        start_date: Default start date for tasks.
        folder: Parent folder details.
        space: Parent space details.
        archived: Whether the list is archived.
        override_statuses: Custom status configuration.
        permission_level: User's permission level for the list.
    """

    id: str
    name: str
    orderindex: int
    status: Optional[Dict[str, Any]] = None
    priority: Optional[Dict[str, Any]] = None
    assignee: Optional[Dict[str, Any]] = None
    task_count: int = 0
    due_date: Optional[str] = None
    start_date: Optional[str] = None
    folder: ClickUpListLocation
    space: ClickUpListLocation
    archived: bool = False
    override_statuses: Optional[Dict[str, Any]] = None
    permission_level: str


class CreateListRequest(BaseModel):
    """Request model for creating a new ClickUp list.

    Attributes:
        name: Name of the list (required).
        content: Description or content of the list.
        due_date: Default due date for tasks as UNIX timestamp in milliseconds.
        priority: Default priority level (1-4, where 1 is urgent).
        assignee: User ID to set as the default assignee.
        status: Default status for new tasks in this list.
    """

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


class ClickUpTaskStatus(BaseModel):
    """Represents the status of a ClickUp task.

    Attributes:
        status: The status name (e.g., "to do").
        id: Unique identifier for the status.
        color: Color code associated with the status.
        type: Type of status (e.g., "open").
        orderindex: Position of the status in the workflow.
    """

    status: str
    id: str
    color: str
    type: str
    orderindex: int


class ClickUpUser(BaseModel):
    """Represents a user in ClickUp.

    Attributes:
        id: Unique identifier for the user.
        username: Display name of the user.
        color: Color code associated with the user.
        email: Email address of the user.
        profilePicture: URL to the user's profile picture.
        initials: User's initials (optional).
    """

    id: int
    username: str
    color: str
    email: str
    profilePicture: Optional[str] = None
    initials: Optional[str] = None


class ClickUpTaskSharing(BaseModel):
    """Represents sharing settings for a ClickUp task.

    Attributes:
        public: Whether the task is publicly accessible.
        public_share_expires_on: Expiration date for public sharing.
        public_fields: List of fields visible in public sharing.
        token: Sharing token.
        seo_optimized: Whether SEO optimization is enabled.
    """

    public: bool
    public_share_expires_on: Optional[str] = None
    public_fields: List[str]
    token: Optional[str] = None
    seo_optimized: bool


class ClickUpTaskLocation(BaseModel):
    """Represents a location reference in a ClickUp task.

    Attributes:
        id: Unique identifier for the location.
        name: Name of the location.
        access: Whether the user has access to this location.
        hidden: Whether the location is hidden (folders/projects only).
    """

    id: str
    name: Optional[str] = None
    access: Optional[bool] = None
    hidden: Optional[bool] = None


class ClickUpTask(BaseModel):
    """Represents a task within a ClickUp list.

    Attributes:
        id: Unique identifier for the task.
        custom_id: Custom identifier for the task.
        custom_item_id: Custom item identifier.
        name: Name/title of the task.
        text_content: Plain text content of the task.
        description: Detailed description of the task.
        status: Current status configuration of the task.
        orderindex: Position of the task in the list.
        date_created: Creation timestamp in milliseconds.
        date_updated: Last update timestamp in milliseconds.
        date_closed: Closure timestamp in milliseconds.
        date_done: Completion timestamp in milliseconds.
        archived: Whether the task is archived.
        creator: User who created the task.
        assignees: List of users assigned to the task.
        group_assignees: List of groups assigned to the task.
        watchers: List of users watching the task.
        checklists: List of checklists in the task.
        tags: List of tags associated with the task.
        parent: Parent task ID for subtasks.
        top_level_parent: Top-most parent task ID.
        priority: Priority level of the task.
        due_date: Due date timestamp in milliseconds.
        start_date: Start date timestamp in milliseconds.
        points: Story points or effort estimation.
        time_estimate: Estimated time in minutes.
        time_spent: Time spent on the task in minutes.
        custom_fields: List of custom field values.
        dependencies: List of dependent task IDs.
        linked_tasks: List of linked task IDs.
        locations: List of location references.
        team_id: ID of the team owning the task.
        url: Web URL to access the task.
        sharing: Sharing configuration for the task.
        permission_level: User's permission level for the task.
        list: Associated list information.
        project: Associated project information.
        folder: Associated folder information.
        space: Associated space information.
        attachments: List of attachments on the task.
    """

    id: str
    custom_id: Optional[str] = None
    custom_item_id: int = 0
    name: str
    text_content: str = ""
    description: str = ""
    status: ClickUpTaskStatus
    orderindex: str
    date_created: str
    date_updated: str
    date_closed: Optional[str] = None
    date_done: Optional[str] = None
    archived: bool = False
    creator: ClickUpUser
    assignees: List[ClickUpUser] = []
    group_assignees: List[Dict[str, Any]] = []
    watchers: List[ClickUpUser] = []
    checklists: List[Dict[str, Any]] = []
    tags: List[str] = []
    parent: Optional[str] = None
    top_level_parent: Optional[str] = None
    priority: Optional[Dict[str, Any]] = None
    due_date: Optional[str] = None
    start_date: Optional[str] = None
    points: Optional[float] = None
    time_estimate: Optional[int] = None
    time_spent: int = 0
    custom_fields: List[Dict[str, Any]] = []
    dependencies: List[str] = []
    linked_tasks: List[str] = []
    locations: List[Dict[str, Any]] = []
    team_id: str
    url: str
    sharing: ClickUpTaskSharing
    permission_level: str
    list: ClickUpTaskLocation
    project: ClickUpTaskLocation
    folder: ClickUpTaskLocation
    space: ClickUpTaskLocation
    attachments: List[Dict[str, Any]] = []


class CreateTaskRequest(BaseModel):
    """Request model for creating a new ClickUp task.

    Attributes:
        name: Name/title of the task (required).
        description: Detailed description of the task.
        assignees: List of user IDs to assign to the task.
        archived: Whether the task should be created as archived.
        group_assignees: List of group IDs to assign to the task.
        tags: List of tags to apply to the task.
        status: Initial status of the task.
        priority: Priority level (1-4, where 1 is urgent).
        due_date: Due date as UNIX timestamp in milliseconds.
        due_date_time: Whether the due date includes a time component.
        time_estimate: Estimated time in minutes.
        start_date: Start date as UNIX timestamp in milliseconds.
        start_date_time: Whether the start date includes a time component.
        points: Story points or effort estimation.
        notify_all: Whether to notify all assignees.
        parent: Parent task ID for subtasks.
        markdown_content: Task description in markdown format.
        links_to: Task ID to link this task to.
        check_required_custom_fields: Whether to validate required custom fields.
        custom_fields: List of custom field values.
        custom_item_id: Custom identifier for the task.
    """

    name: str
    description: Optional[str] = None
    assignees: Optional[List[int]] = None
    archived: Optional[bool] = None
    group_assignees: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    due_date: Optional[int] = None
    due_date_time: Optional[bool] = None
    time_estimate: Optional[int] = None
    start_date: Optional[int] = None
    start_date_time: Optional[bool] = None
    points: Optional[float] = None
    notify_all: Optional[bool] = None
    parent: Optional[str] = None
    markdown_content: Optional[str] = None
    links_to: Optional[str] = None
    check_required_custom_fields: Optional[bool] = None
    custom_fields: Optional[List[Dict[str, Any]]] = None
    custom_item_id: Optional[int] = None


class UpdateTaskRequest(BaseModel):
    """Request model for updating an existing ClickUp task.

    Attributes:
        name: New name/title for the task.
        description: New description for the task.
        status: New status for the task.
        priority: New priority level (1-4, where 1 is urgent).
        due_date: New due date for the task.
        time_estimate: New time estimate in minutes.
        assignees: Complete list of user IDs to assign (replaces existing).
        add_assignees: List of user IDs to add to existing assignees.
        remove_assignees: List of user IDs to remove from existing assignees.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    due_date: Optional[str] = None
    time_estimate: Optional[int] = None
    assignees: Optional[List[int]] = None
    add_assignees: Optional[List[int]] = None
    remove_assignees: Optional[List[int]] = None


class GetListsResponse(BaseModel):
    """Response model for the get_lists endpoint.

    Attributes:
        lists: Array of ClickUp lists returned by the API.
    """

    lists: List[ClickUpList]


class GetTasksResponse(BaseModel):
    """Response model for the get_tasks endpoint.

    Attributes:
        tasks: Array of ClickUp tasks returned by the API.
        last_page: Whether this is the last page of results.
    """

    tasks: List[ClickUpTask]
    last_page: bool


# Generic response type for API responses
T = TypeVar("T")


class ClickUpApiResponse(BaseModel, Generic[T]):
    """Generic response wrapper for ClickUp API responses.

    Attributes:
        data: The response data of type T.
        error: Error message if the request failed.
        status: HTTP status code of the response.
    """

    data: Optional[T] = None
    error: Optional[str] = None
    status: int
