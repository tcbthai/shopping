import os
from app import db, create_app
from app.models_sqldb import User, Category, Product
from flask.ext.script import Manager, Shell, Server
from flask_migrate import MigrateCommand, Migrate

# from flask.ext.migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


# migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Category=Category, Product=Product)


manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True)
                    )
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
