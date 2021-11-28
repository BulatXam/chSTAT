from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

import asyncio

from bot import bot

from loguru import logger

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), default=datetime.now(), nullable=False)
    updated_at = Column(DateTime(True), default=datetime.now(), nullable=False)


class Author(BaseModel):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)

    channels = relationship("Channel", backref="channels")

    def __init__(self, id, first_name, last_name=None, username=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username


class Channel(BaseModel):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.id"))
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

    def get_info(self):
        return f"Канал {self.title}: \n" \
               f"Username: {self.username} \n" \
               f"Описание: {self.description} \n" \
               # f"Ссылка приглашения: {self.invite_link}"


class Post(TimedBaseModel):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey("channel.id"))

    text = Column(String, nullable=True)
    right_time = Column(DateTime(True))

    medias = relationship("PostMedia", backref="postMedias")

    def __init__(self, channel_id, text, right_time):
        self.channel_id = channel_id
        self.text = text
        self.right_time = right_time

    def get_remaining_time(self):
        return self.right_time - datetime.now()

    async def sleep_before_right_time(self):
        total_seconds = self.get_remaining_time().total_seconds()
        logger.info(f"The task fell asleep for {total_seconds} seconds")
        await asyncio.sleep(total_seconds)

    async def send_post(self):
        logger.info(f"Send Post<{self.id}> in Channel<{self.channel_id}>")
        await bot.send_message(
            chat_id=self.channel_id,
            text=self.text
        )


class PostMedia(BaseModel):
    __tablename__ = "postMedia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("post.id"))

    file_id = Column(String)

    file_type = Column(String)

    def __init__(self, post_id, file_id, file_type):
        self.post_id = post_id
        self.file_type = file_type
        self.file_id = file_id


if __name__ == "__main__":
    from sqlalchemy import create_engine

    engine = create_engine('sqlite:///db.sqlite3', echo=False)
    Base.metadata.create_all(engine)
