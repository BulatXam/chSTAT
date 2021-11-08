from sqlalchemy.orm import sessionmaker
from models import Channel, Author

from config import DB_ENGINE


Session = sessionmaker(DB_ENGINE)
session = Session()


async def getOrCreateAuthor(id, first_name, last_name, username) -> Author:
    author = session.query(Author).get(id)
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
