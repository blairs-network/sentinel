-- sentinel.db schema
-- Append-only. No UPDATE except build status progression. No DELETE. Ever.

CREATE TABLE IF NOT EXISTS observations (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  ts      TEXT    NOT NULL,
  source  TEXT    NOT NULL,
  content TEXT    NOT NULL,
  cycle   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS signals (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  ts             TEXT    NOT NULL,
  observation_id INTEGER REFERENCES observations(id),
  pattern        TEXT    NOT NULL,
  frequency      INTEGER DEFAULT 1,
  status         TEXT    DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS decisions (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  ts        TEXT    NOT NULL,
  signal_id INTEGER REFERENCES signals(id),
  decision  TEXT    NOT NULL,
  rationale TEXT    NOT NULL,
  action    TEXT
);

CREATE TABLE IF NOT EXISTS builds (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  ts          TEXT    NOT NULL,
  decision_id INTEGER REFERENCES decisions(id),
  skill_name  TEXT    NOT NULL,
  skill_path  TEXT    NOT NULL,
  mandate_gap TEXT    NOT NULL,
  status      TEXT    DEFAULT 'scoped'
);
