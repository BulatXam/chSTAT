from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db.sqlite3', echo=False)

Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)

    def __init__(self, name, link):
        self.name = name
        self.link = link

    def __repr__(self):
        return f'Channel<name="{self.name}",' \
               f'link="{self.link}">'


if __name__ == "__main__":
    Base.metadata.create_all(engine)
