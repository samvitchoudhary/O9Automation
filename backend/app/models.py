"""
Database models for O9 Test Automation Platform
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class TestCaseStatus(enum.Enum):
    """Test case status enumeration"""
    DRAFT = "draft"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TestStepStatus(enum.Enum):
    """Test step status enumeration"""
    NOT_STARTED = "not_started"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"


class ExecutionStatus(enum.Enum):
    """Execution status enumeration"""
    NOT_RUN = "not_run"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"


class TestCase(Base):
    """Test case model"""
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TestCaseStatus), default=TestCaseStatus.DRAFT, nullable=False)
    assigned_to = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    requirements = Column(Text, nullable=True)
    test_case_version = Column(Integer, default=1, nullable=False)

    # Relationship to test steps
    steps = relationship("TestStep", back_populates="test_case", cascade="all, delete-orphan", order_by="TestStep.step_number")


class TestStep(Base):
    """Test step model"""
    __tablename__ = "test_steps"

    id = Column(Integer, primary_key=True, index=True)
    test_case_id = Column(Integer, ForeignKey("test_cases.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    expected_result = Column(Text, nullable=False)
    actual_result = Column(Text, nullable=True)
    status = Column(Enum(TestStepStatus), default=TestStepStatus.NOT_STARTED, nullable=False)
    transaction_code = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Selenium execution fields
    selenium_script = Column(Text, nullable=True)
    selenium_script_json = Column(Text, nullable=True)
    execution_status = Column(Enum(ExecutionStatus), default=ExecutionStatus.NOT_RUN, nullable=False)
    execution_time_ms = Column(Integer, nullable=True)
    last_executed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)

    # Relationship to test case
    test_case = relationship("TestCase", back_populates="steps")

