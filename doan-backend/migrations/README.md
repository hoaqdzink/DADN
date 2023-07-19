# Migration using commands

## How?

We use python code to keep track at db schema version, it will be located at `/migrations/versions/*.py` (this will be
put on git/bitbucket).

When there are changes to DB schema, you

- Migrate
- Put generated migrate files on git/bitbucket
- Update DB using command

## Migrate

When there are changes happen in `./entity` (Ex: new columns, new table or alter column).

*Note: Only those change that has effect on the system will be detected (meaning changes that was used, if you add a new
column that hasn't been used in the latest code, it won't change the migration version)*

You need to run

```bash
python run.py --env <env> migrate 
```

Which will produce new files at `/migrations/versions`

You can modify them if needed.

## Update DB

You need to run

```bash
python run.py --env <env> 'migrate up' 
```

To update your DB to match the latest schema in the code
(in case your db isn't the latest schema version).

To know what your db current version is, check it at `alembic_version` table of your db instance.