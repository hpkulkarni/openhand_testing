# Data Model

Defined in `config-admin/app/db.py` (`SCHEMA`). Tables are created with `CREATE TABLE IF NOT EXISTS`; there is **no migration tool**. Changing a column means editing `SCHEMA` and handling existing databases by hand (or deleting `config-admin/data/config_admin.db` in dev).

## users
| column | type | notes |
|---|---|---|
| id | INTEGER PK | |
| username | TEXT UNIQUE | |
| password_hash | TEXT | `salt_hex$digest_hex`, PBKDF2-SHA256, 200,000 iterations |
| role | TEXT | CHECK in `admin`, `viewer` |

## sessions
| column | type | notes |
|---|---|---|
| token | TEXT PK | `secrets.token_urlsafe(32)` |
| user_id | INTEGER FK | ON DELETE CASCADE |
| created_at | TEXT | default `datetime('now')`; **not currently used for expiry** |

## configs
| column | type | notes |
|---|---|---|
| id | INTEGER PK | |
| key | TEXT | lowercase letters, digits, `_ . -`; 1-100 chars |
| value | TEXT | always stored as text; interpreted by `value_type` |
| value_type | TEXT | CHECK in `string`, `int`, `bool`, `json` |
| environment | TEXT | CHECK in `dev`, `staging`, `prod` |
| description | TEXT | default empty, max 500 (API level) |
| updated_at | TEXT | set to `datetime('now')` on create/update |
| updated_by | TEXT | username of the admin who last wrote it |

`UNIQUE (key, environment)`: the same key may exist once per environment.

## Value validation (`schemas.validate_value`)
- `int`: must parse with `int()`.
- `bool`: exactly `true` or `false` (lowercase).
- `json`: must parse with `json.loads`.
- `string`: anything.
A failure returns HTTP 422 with a string `detail`.

## Seed data (`seed.py`)
Only inserted when the table is empty.
- Users: `admin` / `admin123` (admin), `viewer` / `viewer123` (viewer). **Demo credentials, local use only.**
- 10 sample configs across dev/staging/prod: `feature.new_dashboard` (bool, all 3 envs), `api.rate_limit_per_minute` (int, dev+prod), `smtp.host` (string, dev+prod), `log.level` (string, dev+prod), `retry.policy` (json, staging).
Tests assert there are exactly 10 seed rows; update `tests/test_configs.py::test_seed_data_present` if you change the seed list.
