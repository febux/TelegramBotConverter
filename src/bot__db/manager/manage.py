from src.bot__db.app import db_flask_app
from src.bot__db.manager.drop_db import drop_db
from src.bot__db.manager.init_db import init_db
from src.bot__db.manager.script_manager import Manager, Command
from src.bot__db.manager.upgrade_db import upgrade_db


class InitDb(Command):
    """initialize database"""

    def run(self):
        init_db()


class DropDb(Command):
    """remove database"""

    def run(self):
        drop_db()


class UpgradeDb(Command):
    """upgrade database records"""

    def run(self):
        upgrade_db()


manager = Manager(db_flask_app.app)

manager.add_command('init_db', InitDb())
manager.add_command('drop_db', DropDb())
manager.add_command('upgrade_db', UpgradeDb())


if __name__ == '__main__':
    manager.run()
