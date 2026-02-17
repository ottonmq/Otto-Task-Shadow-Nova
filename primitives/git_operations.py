"""Git operation primitives for agents."""

import subprocess
from typing import Optional, List


def run_git_command(command: List[str]) -> tuple[bool, str]:
    """
    Execute a git command and return success status and output.
    
    Args:
        command: Git command as list of strings
    
    Returns:
        Tuple of (success, output/error message)
    """
    try:
        result = subprocess.run(
            ["git"] + command,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout or result.stderr
    except Exception as e:
        return False, str(e)


def create_commit(message: str, files: Optional[List[str]] = None) -> bool:
    """
    Create a git commit with the given message.
    
    Args:
        message: Commit message
        files: List of files to stage (None = all changes)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if files:
            for file in files:
                success, _ = run_git_command(["add", file])
                if not success:
                    return False
        else:
            success, _ = run_git_command(["add", "."])
            if not success:
                return False
        
        success, _ = run_git_command(["commit", "-m", message])
        return success
    except Exception as e:
        print(f"Error creating commit: {e}")
        return False


def push_branch(branch: Optional[str] = None, force: bool = False) -> bool:
    """
    Push changes to remote branch.
    
    Args:
        branch: Branch name (None = current branch)
        force: Whether to force push
    
    Returns:
        True if successful, False otherwise
    """
    try:
        cmd = ["push"]
        if force:
            cmd.append("-f")
        if branch:
            cmd.extend(["origin", branch])
        else:
            cmd.append("origin")
        
        success, _ = run_git_command(cmd)
        return success
    except Exception as e:
        print(f"Error pushing branch: {e}")
        return False


def create_branch(branch_name: str, start_point: Optional[str] = None) -> bool:
    """
    Create a new git branch.
    
    Args:
        branch_name: Name of the new branch
        start_point: Starting point (commit/branch)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        cmd = ["checkout", "-b", branch_name]
        if start_point:
            cmd.append(start_point)
        
        success, _ = run_git_command(cmd)
        return success
    except Exception as e:
        print(f"Error creating branch: {e}")
        return False


def delete_branch(branch_name: str, force: bool = False) -> bool:
    """
    Delete a git branch.
    
    Args:
        branch_name: Name of the branch to delete
        force: Whether to force delete
    
    Returns:
        True if successful, False otherwise
    """
    try:
        cmd = ["branch", "-D" if force else "-d", branch_name]
        success, _ = run_git_command(cmd)
        return success
    except Exception as e:
        print(f"Error deleting branch: {e}")
        return False


def get_current_branch() -> Optional[str]:
    """
    Get the current git branch name.
    
    Returns:
        Branch name or None if error
    """
    try:
        success, output = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
        if success:
            return output.strip()
        return None
    except Exception as e:
        print(f"Error getting current branch: {e}")
        return None
