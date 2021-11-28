from db import models

from loguru import logger


async def add_post_in_shedule(post: models.Post):
    logger.info(f"Post<{post.id}> add in shedule!")

    await post.sleep_before_right_time()
    await post.send_post()

    logger.info(
        f"The Post<{post.id}> has been sent in "
        f"Chat<{post.chat_id_for_sending}>"
    )
