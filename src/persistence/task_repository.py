"""Task Repository - Persistence Layer for Otto-task.

Developed by: Otto Napoleón Mendoza Quant
Signature: — OTTONQQ —
Version: 1.0.0
"""

from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from datetime import datetime
import json
import logging
from pathlib import Path

from src.models.task_state import OttoTask, TaskState, TaskAuditLog


logger = logging.getLogger(__name__)


class TaskRepository(ABC):
  """Abstract base class for task persistence."""
  
  @abstractmethod
  async def create(self, task: OttoTask) -> bool:
    """Create new task."""
    pass
  
  @abstractmethod
  async def read(self, task_id: str) -> Optional[OttoTask]:
    """Read task by ID."""
    pass
  
  @abstractmethod
  async def update(self, task: OttoTask) -> bool:
    """Update existing task."""
    pass
  
  @abstractmethod
  async def delete(self, task_id: str) -> bool:
    """Delete task."""
    pass
  
  @abstractmethod
  async def list_by_state(self, state: TaskState) -> List[OttoTask]:
    """List tasks by state."""
    pass
  
  @abstractmethod
  async def get_audit_log(self, task_id: str) -> List[TaskAuditLog]:
    """Get audit log for task."""
    pass


class FileSystemRepository(TaskRepository):
  """File system-based task repository (development)."""
  
  def __init__(self, storage_path: str = "./data/tasks"):
    """Initialize file system repository.
    
    Args:
      storage_path: Path to store task files
    """
    self.storage_path = Path(storage_path)
    self.storage_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"FileSystemRepository initialized at {self.storage_path}")
  
  def _get_task_file(self, task_id: str) -> Path:
    """Get file path for task."""
    return self.storage_path / f"{task_id}.json"
  
  async def create(self, task: OttoTask) -> bool:
    """Create new task file."""
    try:
      file_path = self._get_task_file(task.id)
      
      if file_path.exists():
        logger.warning(f"Task {task.id} already exists")
        return False
      
      with open(file_path, 'w') as f:
        f.write(task.to_json())
      
      logger.info(f"Task {task.id} created successfully")
      return True
    except Exception as e:
      logger.error(f"Error creating task: {e}")
      return False
  
  async def read(self, task_id: str) -> Optional[OttoTask]:
    """Read task from file."""
    try:
      file_path = self._get_task_file(task_id)
      
      if not file_path.exists():
        logger.warning(f"Task {task_id} not found")
        return None
      
      with open(file_path, 'r') as f:
        data = json.load(f)
      
      return OttoTask.from_dict(data)
    except Exception as e:
      logger.error(f"Error reading task: {e}")
      return None
  
  async def update(self, task: OttoTask) -> bool:
    """Update task file."""
    try:
      file_path = self._get_task_file(task.id)
      
      if not file_path.exists():
        logger.warning(f"Task {task.id} not found for update")
        return False
      
      task.version += 1
      with open(file_path, 'w') as f:
        f.write(task.to_json())
      
      logger.info(f"Task {task.id} updated to version {task.version}")
      return True
    except Exception as e:
      logger.error(f"Error updating task: {e}")
      return False
  
  async def delete(self, task_id: str) -> bool:
    """Delete task file."""
    try:
      file_path = self._get_task_file(task_id)
      
      if not file_path.exists():
        logger.warning(f"Task {task_id} not found for deletion")
        return False
      
      file_path.unlink()
      logger.info(f"Task {task_id} deleted")
      return True
    except Exception as e:
      logger.error(f"Error deleting task: {e}")
      return False
  
  async def list_by_state(self, state: TaskState) -> List[OttoTask]:
    """List all tasks with given state."""
    try:
      tasks = []
      for file_path in self.storage_path.glob("*.json"):
        with open(file_path, 'r') as f:
          data = json.load(f)
        
        if data.get("state") == state.value:
          tasks.append(OttoTask.from_dict(data))
      
      logger.info(f"Found {len(tasks)} tasks in state {state.value}")
      return tasks
    except Exception as e:
      logger.error(f"Error listing tasks: {e}")
      return []
  
  async def get_audit_log(self, task_id: str) -> List[TaskAuditLog]:
    """Get audit log for task."""
    try:
      task = await self.read(task_id)
      if not task:
        return []
      return task.audit_log
    except Exception as e:
      logger.error(f"Error getting audit log: {e}")
      return []


class TaskRepositoryFactory:
  """Factory for creating task repositories."""
  
  @staticmethod
  def create_repository(repo_type: str = "filesystem", **kwargs) -> TaskRepository:
    """Create repository instance.
    
    Args:
      repo_type: Repository type (filesystem, database, etc.)
      **kwargs: Additional arguments for repository
    
    Returns:
      TaskRepository instance
    """
    if repo_type == "filesystem":
      return FileSystemRepository(**kwargs)
    else:
      raise ValueError(f"Unknown repository type: {repo_type}")
