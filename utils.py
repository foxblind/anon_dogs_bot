def send_copy(user_id: str, text: str, file: str, file_type: str, bot):
    from telegram.files import photosize, audio, voice, video, videonote, document, animation, sticker, contact

    if file_type == f"{type(None)}":
        bot.send_message(user_id, text)
    elif file_type == f"{photosize.PhotoSize}":
        bot.send_photo(user_id, file, caption=text)
    elif file_type == f"{audio.Audio}":
        bot.send_audio(user_id, file, caption=text)
    elif file_type == f"{voice.Voice}":
        bot.send_voice(user_id, file, caption=text)
    elif file_type == f"{document.Document}":
        bot.send_document(user_id, file, caption=text)
    elif file_type == f"{video.Video}":
        bot.send_video(user_id, file, caption=text)
    elif file_type == f"{videonote.VideoNote}":
        bot.send_video_note(user_id, file)
    elif file_type == f"{animation.Animation}":
        bot.send_animation(user_id, file, caption=text)
    elif file_type == f"{sticker.Sticker}":
        bot.send_sticker(user_id, file)
    elif file_type == f"{contact.Contact}":
        bot.send_contact(user_id, file, "Anon", "User")


def get_input_media(file_id: str, media_type: str):
    from telegram.files import photosize, video, videonote, document, animation, sticker
    from telegram import InputMedia, InputMediaPhoto, InputMediaDocument, InputMediaVideo, InputMediaAnimation, Sticker
    if media_type == f"{photosize.PhotoSize}":
        return InputMediaPhoto(file_id)
    if media_type == f"{video.Video}" or media_type == f"{videonote.VideoNote}":
        return InputMediaVideo(file_id)
    if media_type == f"{document.Document}":
        return InputMediaDocument(file_id)
    if media_type == f"{animation.Animation}":
        return InputMediaAnimation(file_id)


def is_admin(user_id: int):
    import config
    if str(user_id) in config.ADMINS:
        return True
    return False
