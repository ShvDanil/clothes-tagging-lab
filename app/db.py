from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.models import Base


class Database:
    def __init__(self, url: str):
        self.engine = create_engine(url, pool_pre_ping=True, connect_args={"connect_timeout": 5})
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)

    def initialize(self) -> None:
        # Creates missing tables only. Schema changes need a migration or a fresh dev volume.
        Base.metadata.create_all(self.engine)

    def check(self) -> None:
        with self.engine.connect() as connection:
            connection.execute(text("SELECT 1"))

    def close(self) -> None:
        self.engine.dispose()
