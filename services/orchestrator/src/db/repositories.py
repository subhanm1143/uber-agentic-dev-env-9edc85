"""Repositories: the only place that knows SQL.

Each method maps rows to/from the typed models in models.py. Writes use
INSERT ... ON CONFLICT DO NOTHING so a retried request can't duplicate a row.
"""
from __future__ import annotations

from typing import Optional
from uuid import UUID

from ..models import Project, Run, RunStatus, Task
from .connection import connection


class ProjectRepo:
    def create(self, project: Project) -> Project:
        with connection() as conn:
            conn.execute(
                """INSERT INTO projects (id, name, repo_path, created_at)
                   VALUES (%s, %s, %s, %s)
                   ON CONFLICT (id) DO NOTHING""",
                (project.id, project.name, project.repo_path, project.created_at),
            )
        return project

    def get(self, project_id: UUID) -> Optional[Project]:
        with connection() as conn:
            row = conn.execute(
                "SELECT name, repo_path, id, created_at FROM projects WHERE id = %s",
                (project_id,),
            ).fetchone()
        if row is None:
            return None
        return Project(name=row[0], repo_path=row[1], id=row[2], created_at=row[3])


class TaskRepo:
    def create(self, task: Task) -> Task:
        with connection() as conn:
            conn.execute(
                """INSERT INTO tasks (id, project_id, description, created_at)
                   VALUES (%s, %s, %s, %s)
                   ON CONFLICT (id) DO NOTHING""",
                (task.id, task.project_id, task.description, task.created_at),
            )
        return task


class RunRepo:
    def create(self, run: Run) -> Run:
        with connection() as conn:
            conn.execute(
                """INSERT INTO runs (id, task_id, status, iterations, created_at, updated_at)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   ON CONFLICT (id) DO NOTHING""",
                (run.id, run.task_id, run.status.value, run.iterations,
                 run.created_at, run.updated_at),
            )
        return run

    def get(self, run_id: UUID) -> Optional[Run]:
        with connection() as conn:
            row = conn.execute(
                """SELECT task_id, status, iterations, id, created_at, updated_at
                   FROM runs WHERE id = %s""",
                (run_id,),
            ).fetchone()
        if row is None:
            return None
        return Run(task_id=row[0], status=RunStatus(row[1]), iterations=row[2],
                   id=row[3], created_at=row[4], updated_at=row[5])

    def set_status(self, run_id: UUID, status: RunStatus) -> None:
        with connection() as conn:
            conn.execute(
                "UPDATE runs SET status = %s, updated_at = now() WHERE id = %s",
                (status.value, run_id),
            )


project_repo = ProjectRepo()
task_repo = TaskRepo()
run_repo = RunRepo()
