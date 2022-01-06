from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine

from .models import Author, Channel, Post, PostMedia

from aiogram import types

# from config import DB_ENGINE

from datetime import datetime

DB_ENGINE = create_engine('sqlite:///db.sqlite3', echo=False)

Session = sessionmaker(DB_ENGINE)
session = Session()


async def deletePost(id):
    post: Post = session.query(Post).get(id)

    session.delete(post)
    session.commit()
    return post


async def getPost(id):
    post: Post = session.query(Post).get(id)

    return post


async def getPosts(text=None,
                   right_time=None,
                   channel_id=None):
    posts = session.query(Post).filter_by(
        text=text,
        right_time=right_time,
        channel_id=channel_id,
    )

    return posts


async def createPost(text: str,
                     files: list[types.Audio, types.PhotoSize, types.Video,
                                 types.Voice],
                     right_time: datetime,
                     channel_id: str or int) -> Post:
    post = Post(text=text,
                right_time=right_time,
                channel_id=channel_id)

    for file in files:
        media_file = PostMedia(post_id=post.id, file_id=file.file_id,
                               file_type=file.__class__.__name__)
        session.add(media_file)

        post.medias.append(media_file)

    session.add(post)

    channel = session.query(Channel).get(channel_id)
    channel.posts.append(post)

    session.commit()

    return post


async def getAuthor(id: int) -> Author:
    author = session.query(Author).get(id)

    return author


async def getChannel(id: int) -> Channel:
    channel = session.query(Channel).get(id)

    return channel


async def getOrCreateAuthor(id, first_name, last_name, username) -> Author:
    author = session.query(Author).filter_by(id=id,
                                             first_name=first_name,
                                             last_name=last_name,
                                             username=username).first()
    if author:
        return author
    else:
        author = Author(id=id,
                        first_name=first_name,
                        last_name=last_name,
                        username=username)
        session.add(author)
        session.commit()

        return author



async def createAuthor(id, first_name, last_name, username) -> Author:
    if not session.query(Author).get(id):
        author = Author(id=id,
                        first_name=first_name,
                        last_name=last_name,
                        username=username)
        session.add(author)
        session.commit()

        return author


async def createChannel(id, author_id, title, username, description,
                        invite_link, linked_chat_id) -> Channel:
    if not session.query(Channel).get(id):
        channel = Channel(id=id,
                          author_id=author_id,
                          title=title,
                          username=username,
                          description=description,
                          invite_link=invite_link,
                          linked_chat_id=linked_chat_id)
        session.add(channel)
        session.commit()

        return channel
