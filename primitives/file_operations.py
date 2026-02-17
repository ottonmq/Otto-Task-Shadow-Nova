"""File operation primitives for agents."""

import os
from pathlib import Path
from typing import Optional


def create_file(file_path: str, content: str, overwrite: bool = False) -> bool:
    """
    Create a new file with the given content.
    
    Args:
        file_path: Path to the file to create
        content: Content to write to the file
        overwrite: Whether to overwrite if file exists
    
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)
        
        if path.exists() and not overwrite:
            return False
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error creating file {file_path}: {e}")
        return False


def edit_file(file_path: str, content: str) -> bool:
    """
    Edit an existing file with new content.
    
    Args:
        file_path: Path to the file to edit
        content: New content to write
    
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)
        
        if not path.exists():
            return False
        
        path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error editing file {file_path}: {e}")
        return False


def delete_file(file_path: str) -> bool:
    """
    Delete a file.
    
    Args:
        file_path: Path to the file to delete
    
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)
        
        if not path.exists():
            return False
        
        path.unlink()
        return True
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False


def read_file(file_path: str) -> Optional[str]:
    """
    Read the content of a file.
    
    Args:
        file_path: Path to the file to read
    
    Returns:
        File content as string, or None if error
    """
    try:
        path = Path(file_path)
        
        if not path.exists():
            return None
        
        return path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
