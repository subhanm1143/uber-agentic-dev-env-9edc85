"""Pydantic DTOs: the API's request/response contract.

These are deliberately separate from the domain models — the wire shape is
allowed to differ from the storage shape, and validation lives here at the edge.
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreateProjectRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    repo_path: str = Field(min_length=1)


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    repo_path: str
    created_at: datetime


class CreateTaskRequest(BaseModel):
    description: str = Field(min_length=1, max_length=4000)


class TaskResponse(BaseModel):
    id: UUID
    project_id: UUID
    description: str


class RunResponse(BaseModel):
    id: UUID
    task_id: UUID
    status: str
    iterations: int
