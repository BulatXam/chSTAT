from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

Base = declarative_base()


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)

    channels = relationship("Channel", backref="channels")


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(String, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id", ondelete="CASCADE"))

    title = Column(String)
    username = Column(String)
    description = Column(String)
    invite_link = Column(String)
    linked_chat_id = Column(String)

    def __init__(self, id, author_id, title, username, description,
                 invite_link, linked_chat_id):
        self.id = id
        self.author_id = author_id
        self.title = title
        self.username = username
        self.description = description
        self.invite_link = invite_link
        self.linked_chat_id = linked_chat_id

    def __repr__(self):
        return f'Channel<name="{self.name}",' \
               f'link="{self.link}">'


if __name__ == "__main__":
    from sqlalchemy import create_engine

    engine = create_engine('sqlite:///db.sqlite3', echo=False)
    Base.metadata.create_all(engine)
