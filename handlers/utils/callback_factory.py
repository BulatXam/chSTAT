from aiogram.utils.callback_data import CallbackData

# Callbacks

get_channel = CallbackData("get_channel", "channel_id")
get_my_channels = CallbackData("get_my_channels", "author_id")

delete_channel = CallbackData("delete_channel", "channel_id")

get_channel_posts = CallbackData("get_channels_posts", "channel_id")
get_post = CallbackData("get_post", "post_id")

create_post = CallbackData("create_post", "channel_id")
edit_post = CallbackData("edit_post", "post_id")
delete_post = CallbackData("delete_post", "post_id")
