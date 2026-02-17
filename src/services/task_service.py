"""Task Service - Business Logic Layer for Otto-task.

Developed by: Otto Napoleón Mendoza Quant
Signature: — OTTONQQ —
Version: 1.0.0
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging

from src.models.task_state import OttoTask, TaskState, TaskPriority, SecurityLevel
from src.persistence.task_repository import TaskRepository


logger = logging.getLogger(__name__)


class TaskService:
  """Service layer for task management."""
  
  def __init__(self, repository: TaskRepository):
    """Initialize task service.
    
    Args:
      repository: Task repository instance
    """
    self.repository = repository
  
  async def create_task(
    self,
    title: str,
    description: str,
    priority: TaskPriority = TaskPriority.MEDIUM,
    security_level: SecurityLevel = SecurityLevel.MEDIUM,
    assigned_to: Optional[str] = None,
    due_date: Optional[datetime] = None,
    created_by: str = "system",
  ) -> Optional[OttoTask]:
    """Create new task.
    
    Args:
      title: Task title
      description: Task description
      priority: Task priority
      security_level: Security classification
      assigned_to: Assigned user
      due_date: Due date
      created_by: Creator identifier
    
    Returns:
      Created task or None if failed
    """
    try:
      task = OttoTask(
        title=title,
        description=description,
        priority=priority,
        security_level=security_level,
        assigned_to=assigned_to,
        due_date=due_date,
      )
      task.metadata.created_by = created_by
      
      success = await self.repository.create(task)
      if success:
        logger.info(f"Task {task.id} created by {created_by}")
        return task
      return None
    except Exception as e:
      logger.error(f"Error creating task: {e}")
      return None
  
  async def get_task(self, task_id: str) -> Optional[OttoTask]:
    """Get task by ID."""
    return await self.repository.read(task_id)
  
  async def transition_task(
    self,
    task_id: str,
    new_state: TaskState,
    actor: str,
    details: Optional[Dict] = None,
  ) -> bool:
    """Transition task to new state.
    
    Args:
      task_id: Task ID
      new_state: Target state
      actor: User/agent performing transition
      details: Additional details
    
    Returns:
      True if successful, False otherwise
    """
    try:
      task = await self.repository.read(task_id)
      if not task:
        logger.warning(f"Task {task_id} not found")
        return False
      
      success = task.transition_to(new_state, actor, details)
      if success:
        await self.repository.update(task)
        logger.info(f"Task {task_id} transitioned to {new_state.value} by {actor}")
        return True
      return False
    except Exception as e:
      logger.error(f"Error transitioning task: {e}")
      return False
  
  async def get_pending_tasks(self) -> List[OttoTask]:
    """Get all pending tasks."""
    return await self.repository.list_by_state(TaskState.PENDING)
  
  async def get_in_progress_tasks(self) -> List[OttoTask]:
    """Get all in-progress tasks."""
    return await self.repository.list_by_state(TaskState.IN_PROGRESS)
  
  async def get_secured_tasks(self) -> List[OttoTask]:
    """Get all secured tasks."""
    return await self.repository.list_by_state(TaskState.SECURED)
  
  async def get_overdue_tasks(self) -> List[OttoTask]:
    """Get tasks past due date."""
    try:
      pending = await self.repository.list_by_state(TaskState.PENDING)
      in_progress = await self.repository.list_by_state(TaskState.IN_PROGRESS)
      
      overdue = []
      now = datetime.utcnow()
      
      for task in pending + in_progress:
        if task.due_date and task.due_date < now:
          overdue.append(task)
      
      return overdue
    except Exception as e:
      logger.error(f"Error getting overdue tasks: {e}")
      return []
  
  async def get_task_statistics(self) -> Dict[str, Any]:
    """Get task statistics."""
    try:
      pending = await self.repository.list_by_state(TaskState.PENDING)
      in_progress = await self.repository.list_by_state(TaskState.IN_PROGRESS)
      secured = await self.repository.list_by_state(TaskState.SECURED)
      
      return {
        "total_tasks": len(pending) + len(in_progress) + len(secured),
        "pending": len(pending),
        "in_progress": len(in_progress),
        "secured": len(secured),
        "completion_rate": (
          len(secured) / (len(pending) + len(in_progress) + len(secured))
          if (len(pending) + len(in_progress) + len(secured)) > 0
          else 0
        ),
      }
    except Exception as e:
      logger.error(f"Error getting statistics: {e}")
      return {}
  
  async def get_task_audit_log(self, task_id: str) -> List[Dict[str, Any]]:
    """Get audit log for task."""
    try:
      audit_log = await self.repository.get_audit_log(task_id)
      return [log.to_dict() for log in audit_log]
    except Exception as e:
      logger.error(f"Error getting audit log: {e}")
      return []
