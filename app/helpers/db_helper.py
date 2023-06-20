from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MySQLAlchemy(SQLAlchemy):
    def __init__(self, app: Flask = None, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.read_engine = create_engine(app.config['READ_DATABASE_URI'])
        self.write_engine = create_engine(app.config['WRITE_DATABASE_URI'])
        self.ReadSession = sessionmaker(bind=self.read_engine)
        self.WriteSession = sessionmaker(bind=self.write_engine)

    def _make_session_factory(self, options):
        # 根据选项返回适当的会话对象
        if options.get('read'):
            return self.ReadSession()
        elif options.get('write'):
            return self.WriteSession()
        else:
            return super()._make_session_factory(options)
