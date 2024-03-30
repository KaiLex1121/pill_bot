from aiogram.types import Message


def render_response(message: Message, is_media=False) -> str:

    response = None

    if not is_media:
        response = message.html_text + f"\n\n\
            @{message.from_user.username} (#id{message.from_user.id})"
    else:
        response = ((message.caption or "") + f"\n\n\
            @{message.from_user.username} (#id{message.from_user.id})")

    return response