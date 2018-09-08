from playhouse.migrate import *

DATABASE = SqliteDatabase('todos.sqlite')

migrator = SqliteMigrator(DATABASE)

completed = BooleanField(default=False)

migrate(
    migrator.add_column('todo', 'completed', completed),
)
