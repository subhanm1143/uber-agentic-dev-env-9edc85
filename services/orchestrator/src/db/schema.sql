-- Core domain for the agentic dev environment.
-- Every entity carries a UUID id and a created_at to make runs traceable.

CREATE TABLE IF NOT EXISTS projects (
    id          UUID PRIMARY KEY,
    name        TEXT NOT NULL,
    repo_path   TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS tasks (
    id           UUID PRIMARY KEY,
    project_id   UUID NOT NULL REFERENCES projects (id),
    description  TEXT NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS runs (
    id           UUID PRIMARY KEY,
    task_id      UUID NOT NULL REFERENCES tasks (id),
    status       TEXT NOT NULL DEFAULT 'QUEUED',
    iterations   INT  NOT NULL DEFAULT 0,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS runs_task_id_idx ON runs (task_id);
CREATE INDEX IF NOT EXISTS runs_status_idx  ON runs (status);

-- Raw agent I/O is stored verbatim so a run can be replayed and debugged.
CREATE TABLE IF NOT EXISTS messages (
    id          UUID PRIMARY KEY,
    run_id      UUID NOT NULL REFERENCES runs (id),
    role        TEXT NOT NULL,        -- 'planner' | 'codegen' | 'executor' | 'system'
    content     TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS messages_run_id_idx ON messages (run_id);

CREATE TABLE IF NOT EXISTS artifacts (
    id          UUID PRIMARY KEY,
    run_id      UUID NOT NULL REFERENCES runs (id),
    kind        TEXT NOT NULL,        -- 'patch' | 'log' | 'backup'
    path        TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
