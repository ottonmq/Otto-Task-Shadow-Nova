"""Merge request operation primitives for agents."""

from typing import Optional, Dict, Any
import subprocess
import json


def run_gitlab_api_command(endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> tuple[bool, Any]:
    """
    Execute a GitLab API command using glab CLI.
    
    Args:
        endpoint: API endpoint path
        method: HTTP method (GET, POST, PUT, DELETE)
        data: Request data for POST/PUT
    
    Returns:
        Tuple of (success, response data)
    """
    try:
        cmd = ["glab", "api", endpoint]
        
        if method != "GET":
            cmd.extend(["-X", method])
        
        if data:
            cmd.extend(["-f", json.dumps(data)])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            try:
                return True, json.loads(result.stdout)
            except:
                return True, result.stdout
        return False, result.stderr
    except Exception as e:
        return False, str(e)


def create_merge_request(
    source_branch: str,
    target_branch: str,
    title: str,
    description: Optional[str] = None,
    assignee_ids: Optional[list] = None,
    reviewer_ids: Optional[list] = None,
    labels: Optional[list] = None
) -> tuple[bool, Optional[int]]:
    """
    Create a new merge request.
    
    Args:
        source_branch: Source branch name
        target_branch: Target branch name
        title: MR title
        description: MR description
        assignee_ids: List of assignee user IDs
        reviewer_ids: List of reviewer user IDs
        labels: List of label names
    
    Returns:
        Tuple of (success, MR IID or None)
    """
    try:
        data = {
            "source_branch": source_branch,
            "target_branch": target_branch,
            "title": title,
        }
        
        if description:
            data["description"] = description
        if assignee_ids:
            data["assignee_ids"] = assignee_ids
        if reviewer_ids:
            data["reviewer_ids"] = reviewer_ids
        if labels:
            data["labels"] = ",".join(labels)
        
        success, response = run_gitlab_api_command("projects/:id/merge_requests", "POST", data)
        
        if success and isinstance(response, dict):
            return True, response.get("iid")
        return False, None
    except Exception as e:
        print(f"Error creating merge request: {e}")
        return False, None


def update_merge_request(
    mr_iid: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    target_branch: Optional[str] = None,
    assignee_ids: Optional[list] = None,
    reviewer_ids: Optional[list] = None,
    labels: Optional[list] = None
) -> bool:
    """
    Update an existing merge request.
    
    Args:
        mr_iid: Merge request IID
        title: New title
        description: New description
        target_branch: New target branch
        assignee_ids: New assignee IDs
        reviewer_ids: New reviewer IDs
        labels: New labels
    
    Returns:
        True if successful, False otherwise
    """
    try:
        data = {}
        
        if title:
            data["title"] = title
        if description:
            data["description"] = description
        if target_branch:
            data["target_branch"] = target_branch
        if assignee_ids:
            data["assignee_ids"] = assignee_ids
        if reviewer_ids:
            data["reviewer_ids"] = reviewer_ids
        if labels:
            data["labels"] = ",".join(labels)
        
        success, _ = run_gitlab_api_command(
            f"projects/:id/merge_requests/{mr_iid}",
            "PUT",
            data
        )
        return success
    except Exception as e:
        print(f"Error updating merge request: {e}")
        return False


def merge_merge_request(mr_iid: int, squash: bool = False) -> bool:
    """
    Merge a merge request.
    
    Args:
        mr_iid: Merge request IID
        squash: Whether to squash commits
    
    Returns:
        True if successful, False otherwise
    """
    try:
        data = {}
        if squash:
            data["squash"] = True
        
        success, _ = run_gitlab_api_command(
            f"projects/:id/merge_requests/{mr_iid}/merge",
            "PUT",
            data
        )
        return success
    except Exception as e:
        print(f"Error merging merge request: {e}")
        return False


def close_merge_request(mr_iid: int) -> bool:
    """
    Close a merge request.
    
    Args:
        mr_iid: Merge request IID
    
    Returns:
        True if successful, False otherwise
    """
    try:
        data = {"state_event": "close"}
        success, _ = run_gitlab_api_command(
            f"projects/:id/merge_requests/{mr_iid}",
            "PUT",
            data
        )
        return success
    except Exception as e:
        print(f"Error closing merge request: {e}")
        return False
