CREATE TABLE references_by_scope (
    scope TEXT PRIMARY KEY,
    revision INTEGER NOT NULL CHECK (revision > 0),
    digest TEXT NOT NULL
);
CREATE TABLE publication_outcomes (
    operation TEXT PRIMARY KEY,
    scope TEXT NOT NULL,
    revision INTEGER NOT NULL,
    digest TEXT NOT NULL
);
