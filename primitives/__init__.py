"""Unit primitives for agent operations."""

from .file_operations import (
    create_file,
    edit_file,
    delete_file,
    read_file,
)
from .git_operations import (
    create_commit,
    push_branch,
    create_branch,
    delete_branch,
    get_current_branch,
)
from .merge_request_operations import (
    create_merge_request,
    update_merge_request,
    merge_merge_request,
    close_merge_request,
)

__all__ = [
    "create_file",
    "edit_file",
    "delete_file",
    "read_file",
    "create_commit",
    "push_branch",
    "create_branch",
    "delete_branch",
    "get_current_branch",
    "create_merge_request",
    "update_merge_request",
    "merge_merge_request",
    "close_merge_request",
]
