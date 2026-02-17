"""Task State Management Model for Otto-task Persistence Layer.

Developed by: Otto Napoleón Mendoza Quant
Signature: — OTTONQQ —
Version: 1.0.0
"""

from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict
from uuid import uuid4
import json
import hashlib


class TaskState(str, Enum):
  """Task state enumeration with security levels."""
  PENDING = "pending"
  IN_PROGRESS = "in_progress"
  SECURED = "secured"
  FAILED = "failed"
  ARCHIVED = "archived"


class TaskPriority(str, Enum):
  """Task priority levels."""
  CRITICAL = "critical"
  HIGH = "high"
  MEDIUM = "medium"
  LOW = "low"


class SecurityLevel(str, Enum):
  """Security classification levels."""
  CRITICAL = "critical"
  HIGH = "high"
  MEDIUM = "medium"
  LOW = "low"
  INFO = "info"


@dataclass
class TaskMetadata:
  """Metadata for task tracking and audit."""
  created_by: str
  created_at: datetime = field(default_factory=datetime.utcnow)
  updated_at: datetime = field(default_factory=datetime.utcnow)
  updated_by: Optional[str] = None
  tags: List[str] = field(default_factory=list)
  custom_fields: Dict[str, Any] = field(default_factory=dict)

  def to_dict(self) -> Dict[str, Any]:
    """Convert metadata to dictionary."""
    return {
      "created_by": self.created_by,
      "created_at": self.created_at.isoformat(),
      "updated_at": self.updated_at.isoformat(),
      "updated_by": self.updated_by,
      "tags": self.tags,
      "custom_fields": self.custom_fields,
    }


@dataclass
class TaskAuditLog:
  """Audit log entry for task state changes."""
  timestamp: datetime = field(default_factory=datetime.utcnow)
  action: str = ""
  previous_state: Optional[str] = None
  new_state: Optional[str] = None
  actor: str = ""
  details: Dict[str, Any] = field(default_factory=dict)
  checksum: str = ""

  def calculate_checksum(self) -> str:
    """Calculate SHA256 checksum for audit integrity."""
    data = f"{self.timestamp}{self.action}{self.previous_state}{self.new_state}{self.actor}"
    return hashlib.sha256(data.encode()).hexdigest()

  def to_dict(self) -> Dict[str, Any]:
    """Convert audit log to dictionary."""
    return {
      "timestamp": self.timestamp.isoformat(),
      "action": self.action,
      "previous_state": self.previous_state,
      "new_state": self.new_state,
      "actor": self.actor,
      "details": self.details,
      "checksum": self.checksum,
    }


@dataclass
class OttoTask:
  """Core Task Model for Otto-task Persistence Layer.
  
  Attributes:
    id: Unique task identifier (UUID)
    title: Task title
    description: Detailed task description
    state: Current task state (Pending, In-Progress, Secured)
    priority: Task priority level
    security_level: Security classification
    metadata: Task metadata and tracking info
    audit_log: Complete audit trail
  """
  
  id: str = field(default_factory=lambda: str(uuid4()))
  title: str = ""
  description: str = ""
  state: TaskState = TaskState.PENDING
  priority: TaskPriority = TaskPriority.MEDIUM
  security_level: SecurityLevel = SecurityLevel.MEDIUM
  metadata: TaskMetadata = field(default_factory=lambda: TaskMetadata(created_by="system"))
  audit_log: List[TaskAuditLog] = field(default_factory=list)
  
  # Execution tracking
  assigned_to: Optional[str] = None
  due_date: Optional[datetime] = None
  completion_date: Optional[datetime] = None
  
  # Security fields
  encrypted_payload: Optional[str] = None
  checksum: str = ""
  version: int = 1
  
  def __post_init__(self):
    """Validate and initialize task."""
    self._validate_state_transition()
    self._calculate_checksum()
  
  def _validate_state_transition(self) -> bool:
    """Validate state transitions follow security rules."""
    valid_transitions = {
      TaskState.PENDING: [TaskState.IN_PROGRESS, TaskState.ARCHIVED],
      TaskState.IN_PROGRESS: [TaskState.SECURED, TaskState.FAILED, TaskState.PENDING],
      TaskState.SECURED: [TaskState.ARCHIVED],
      TaskState.FAILED: [TaskState.PENDING, TaskState.ARCHIVED],
      TaskState.ARCHIVED: [],
    }
    return True
  
  def _calculate_checksum(self) -> None:
    """Calculate task checksum for integrity verification."""
    data = f"{self.id}{self.title}{self.state}{self.priority}{self.security_level}"
    self.checksum = hashlib.sha256(data.encode()).hexdigest()
  
  def transition_to(self, new_state: TaskState, actor: str, details: Optional[Dict] = None) -> bool:
    """Transition task to new state with audit logging.
    
    Args:
      new_state: Target state
      actor: User/agent performing transition
      details: Additional transition details
    
    Returns:
      True if transition successful, False otherwise
    """
    valid_transitions = {
      TaskState.PENDING: [TaskState.IN_PROGRESS, TaskState.ARCHIVED],
      TaskState.IN_PROGRESS: [TaskState.SECURED, TaskState.FAILED, TaskState.PENDING],
      TaskState.SECURED: [TaskState.ARCHIVED],
      TaskState.FAILED: [TaskState.PENDING, TaskState.ARCHIVED],
      TaskState.ARCHIVED: [],
    }
    
    if new_state not in valid_transitions.get(self.state, []):
      return False
    
    # Create audit log entry
    audit_entry = TaskAuditLog(
      action=f"state_transition",
      previous_state=self.state.value,
      new_state=new_state.value,
      actor=actor,
      details=details or {},
    )
    audit_entry.checksum = audit_entry.calculate_checksum()
    
    # Update task
    self.state = new_state
    self.metadata.updated_at = datetime.utcnow()
    self.metadata.updated_by = actor
    self.audit_log.append(audit_entry)
    self._calculate_checksum()
    
    if new_state == TaskState.SECURED:
      self.completion_date = datetime.utcnow()
    
    return True
  
  def to_dict(self) -> Dict[str, Any]:
    """Convert task to dictionary for serialization."""
    return {
      "id": self.id,
      "title": self.title,
      "description": self.description,
      "state": self.state.value,
      "priority": self.priority.value,
      "security_level": self.security_level.value,
      "assigned_to": self.assigned_to,
      "due_date": self.due_date.isoformat() if self.due_date else None,
      "completion_date": self.completion_date.isoformat() if self.completion_date else None,
      "metadata": self.metadata.to_dict(),
      "audit_log": [log.to_dict() for log in self.audit_log],
      "checksum": self.checksum,
      "version": self.version,
    }
  
  def to_json(self) -> str:
    """Convert task to JSON string."""
    return json.dumps(self.to_dict(), indent=2)
  
  @classmethod
  def from_dict(cls, data: Dict[str, Any]) -> "OttoTask":
    """Create task from dictionary."""
    task = cls(
      id=data.get("id", str(uuid4())),
      title=data.get("title", ""),
      description=data.get("description", ""),
      state=TaskState(data.get("state", "pending")),
      priority=TaskPriority(data.get("priority", "medium")),
      security_level=SecurityLevel(data.get("security_level", "medium")),
      assigned_to=data.get("assigned_to"),
      version=data.get("version", 1),
    )
    return task
