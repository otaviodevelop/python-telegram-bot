#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2020
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""Base class for Telegram InputMedia Objects."""

from dataclasses import dataclass, InitVar
from telegram import TelegramObject, InputFile, PhotoSize, Animation, Video, Audio, Document
from telegram.utils.helpers import DEFAULT_NONE, DefaultValue

from typing import Optional, Union, IO, cast

from telegram.utils.types import FileLike


class InputMedia(TelegramObject):
    """Base class for Telegram InputMedia Objects.

    See :class:`telegram.InputMediaAnimation`, :class:`telegram.InputMediaAudio`,
    :class:`telegram.InputMediaDocument`, :class:`telegram.InputMediaPhoto` and
    :class:`telegram.InputMediaVideo` for detailed use.

    """
    pass


@dataclass(eq=False)
class InputMediaAnimation(InputMedia):
    """Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent.

    Attributes:
        type (:obj:`str`): ``animation``.
        media (:obj:`str` | :class:`telegram.InputFile`): Animation to send.
        caption (:obj:`str`): Optional. Caption of the document to be sent.
        parse_mode (:obj:`str`): Optional. The parse mode to use for text formatting.
        thumb (:class:`telegram.InputFile`): Optional. Thumbnail of the file to send.
        width (:obj:`int`): Optional. Animation width.
        height (:obj:`int`): Optional. Animation height.
        duration (:obj:`int`): Optional. Animation duration.


    Args:
        media (:obj:`str` | `filelike object` | :class:`telegram.Animation`): File to send. Pass a
            file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP
            URL for Telegram to get a file from the Internet. Lastly you can pass an existing
            :class:`telegram.Animation` object to send.
        thumb (`filelike object`, optional): Thumbnail of the file sent; can be ignored if
            thumbnail generation for the file is supported server-side. The thumbnail should be
            in JPEG format and less than 200 kB in size. A thumbnail's width and height should
            not exceed 320. Ignored if the file is not uploaded using multipart/form-data.
            Thumbnails can't be reused and can be only uploaded as a new file.
        caption (:obj:`str`, optional): Caption of the animation to be sent, 0-1024 characters
            after entities parsing.
        parse_mode (:obj:`str`, optional): Send Markdown or HTML, if you want Telegram apps to show
            bold, italic, fixed-width text or inline URLs in the media caption. See the constants
            in :class:`telegram.ParseMode` for the available modes.
        width (:obj:`int`, optional): Animation width.
        height (:obj:`int`, optional): Animation height.
        duration (:obj:`int`, optional): Animation duration.

    Note:
        When using a :class:`telegram.Animation` for the :attr:`media` attribute. It will take the
        width, height and duration from that video, unless otherwise specified with the optional
        arguments.
    """

    media: Union[str, FileLike, Animation]
    thumb: Optional[FileLike] = None
    caption: Optional[str] = None
    parse_mode: Optional[Union[str, DefaultValue]] = DEFAULT_NONE
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None

    def __post_init__(self,
                      media: Union[str, FileLike, Animation],
                      thumb: FileLike = None) -> None:
        self.type = 'animation'

        if isinstance(media, Animation):
            self.media: Union[str, InputFile] = media.file_id
            self.width = media.width
            self.height = media.height
            self.duration = media.duration
        elif InputFile.is_file(media):
            media = cast(IO, media)
            self.media = InputFile(media, attach=True)
        else:
            self.media = media

        if thumb:
            if InputFile.is_file(thumb):
                thumb = cast(IO, thumb)
                self.thumb = InputFile(thumb, attach=True)
            else:
                self.thumb = thumb


@dataclass(eq=False)
class InputMediaPhoto(InputMedia):
    """Represents a photo to be sent.

    Attributes:
        type (:obj:`str`): ``photo``.
        media (:obj:`str` | :class:`telegram.InputFile`): Photo to send.
        caption (:obj:`str`): Optional. Caption of the document to be sent.
        parse_mode (:obj:`str`): Optional. The parse mode to use for text formatting.

    Args:
        media (:obj:`str` | `filelike object` | :class:`telegram.PhotoSize`): File to send. Pass a
            file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP
            URL for Telegram to get a file from the Internet. Lastly you can pass an existing
            :class:`telegram.PhotoSize` object to send.
        caption (:obj:`str`, optional ): Caption of the photo to be sent, 0-1024 characters after
            entities parsing.
        parse_mode (:obj:`str`, optional): Send Markdown or HTML, if you want Telegram apps to show
            bold, italic, fixed-width text or inline URLs in the media caption. See the constants
            in :class:`telegram.ParseMode` for the available modes.
    """

    media: InitVar[Union[str, FileLike, PhotoSize]]
    caption: InitVar[str] = None
    parse_mode: Optional[Union[str, DefaultValue]] = DEFAULT_NONE

    def __post_init__(self, media: Union[str, FileLike, PhotoSize], caption: str = None) -> None:
        self.type = 'photo'

        if isinstance(media, PhotoSize):
            self.media: Union[str, InputFile] = media.file_id
        elif InputFile.is_file(media):
            media = cast(IO, media)
            self.media = InputFile(media, attach=True)
        else:
            self.media = media  # type: ignore[assignment]

        if caption:
            self.caption = caption


@dataclass(eq=False)
class InputMediaVideo(InputMedia):
    """Represents a video to be sent.

    Attributes:
        type (:obj:`str`): ``video``.
        media (:obj:`str` | :class:`telegram.InputFile`): Video file to send.
        caption (:obj:`str`): Optional. Caption of the document to be sent.
        parse_mode (:obj:`str`): Optional. The parse mode to use for text formatting.
        width (:obj:`int`): Optional. Video width.
        height (:obj:`int`): Optional. Video height.
        duration (:obj:`int`): Optional. Video duration.
        supports_streaming (:obj:`bool`): Optional. Pass True, if the uploaded video is suitable
            for streaming.
        thumb (:class:`telegram.InputFile`): Optional. Thumbnail of the file to send.

    Args:
        media (:obj:`str` | `filelike object` | :class:`telegram.Video`): File to send. Pass a
            file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP
            URL for Telegram to get a file from the Internet. Lastly you can pass an existing
            :class:`telegram.Video` object to send.
        caption (:obj:`str`, optional): Caption of the video to be sent, 0-1024 characters after
            entities parsing.
        parse_mode (:obj:`str`, optional): Send Markdown or HTML, if you want Telegram apps to show
            bold, italic, fixed-width text or inline URLs in the media caption. See the constants
            in :class:`telegram.ParseMode` for the available modes.
        width (:obj:`int`, optional): Video width.
        height (:obj:`int`, optional): Video height.
        duration (:obj:`int`, optional): Video duration.
        supports_streaming (:obj:`bool`, optional): Pass True, if the uploaded video is suitable
            for streaming.
        thumb (`filelike object`, optional): Thumbnail of the file sent; can be ignored if
            thumbnail generation for the file is supported server-side. The thumbnail should be
            in JPEG format and less than 200 kB in size. A thumbnail's width and height should
            not exceed 320. Ignored if the file is not uploaded using multipart/form-data.
            Thumbnails can't be reused and can be only uploaded as a new file.

    Note:
        When using a :class:`telegram.Video` for the :attr:`media` attribute. It will take the
        width, height and duration from that video, unless otherwise specified with the optional
        arguments.
    """

    media: Union[str, FileLike, Video]
    caption: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    supports_streaming: Optional[bool] = None
    parse_mode: Union[str, DefaultValue] = DEFAULT_NONE
    thumb: FileLike = None

    def __post_init__(self, media: Union[str, FileLike, Video], thumb: FileLike = None) -> None:
        self.type = 'video'

        if isinstance(media, Video):
            self.media: Union[str, InputFile] = media.file_id
            self.width = media.width
            self.height = media.height
            self.duration = media.duration
        elif InputFile.is_file(media):
            media = cast(IO, media)
            self.media = InputFile(media, attach=True)
        else:
            self.media = media

        if thumb:
            if InputFile.is_file(thumb):
                thumb = cast(IO, thumb)
                self.thumb = InputFile(thumb, attach=True)
            else:
                self.thumb = thumb


@dataclass(eq=False)
class InputMediaAudio(InputMedia):
    """Represents an audio file to be treated as music to be sent.

    Attributes:
        type (:obj:`str`): ``audio``.
        media (:obj:`str` | :class:`telegram.InputFile`): Audio file to send.
        caption (:obj:`str`): Optional. Caption of the document to be sent.
        parse_mode (:obj:`str`): Optional. The parse mode to use for text formatting.
        duration (:obj:`int`): Duration of the audio in seconds.
        performer (:obj:`str`): Optional. Performer of the audio as defined by sender or by audio
            tags.
        title (:obj:`str`): Optional. Title of the audio as defined by sender or by audio tags.
        thumb (:class:`telegram.InputFile`): Optional. Thumbnail of the file to send.

    Args:
        media (:obj:`str` | `filelike object` | :class:`telegram.Audio`): File to send. Pass a
            file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP
            URL for Telegram to get a file from the Internet. Lastly you can pass an existing
            :class:`telegram.Document` object to send.
        caption (:obj:`str`, optional): Caption of the audio to be sent, 0-1024 characters after
            entities parsing.
        parse_mode (:obj:`str`, optional): Send Markdown or HTML, if you want Telegram apps to show
            bold, italic, fixed-width text or inline URLs in the media caption. See the constants
            in :class:`telegram.ParseMode` for the available modes.
        duration (:obj:`int`): Duration of the audio in seconds as defined by sender.
        performer (:obj:`str`, optional): Performer of the audio as defined by sender or by audio
            tags.
        title (:obj:`str`, optional): Title of the audio as defined by sender or by audio tags.
        thumb (`filelike object`, optional): Thumbnail of the file sent; can be ignored if
            thumbnail generation for the file is supported server-side. The thumbnail should be
            in JPEG format and less than 200 kB in size. A thumbnail's width and height should
            not exceed 320. Ignored if the file is not uploaded using multipart/form-data.
            Thumbnails can't be reused and can be only uploaded as a new file.

    Note:
        When using a :class:`telegram.Audio` for the :attr:`media` attribute. It will take the
        duration, performer and title from that video, unless otherwise specified with the
        optional arguments.
    """

    media: InitVar[Union[str, FileLike, Audio]]
    thumb: InitVar[FileLike] = None
    caption: str = None
    parse_mode: Union[str, DefaultValue] = DEFAULT_NONE
    duration: int = None
    performer: str = None
    title: str = None

    def __post_init__(self, media: Union[str, FileLike, Audio], thumb: FileLike = None) -> None:
        self.type = 'audio'

        if isinstance(media, Audio):
            self.media: Union[str, InputFile] = media.file_id
            self.duration = media.duration
            self.performer = media.performer
            self.title = media.title
        elif InputFile.is_file(media):
            media = cast(IO, media)
            self.media = InputFile(media, attach=True)
        else:
            self.media = media  # type: ignore[assignment]

        if thumb:
            if InputFile.is_file(thumb):
                thumb = cast(IO, thumb)
                self.thumb = InputFile(thumb, attach=True)
            else:
                self.thumb = thumb  # type: ignore[assignment]


@dataclass(eq=False)
class InputMediaDocument(InputMedia):
    """Represents a general file to be sent.

    Attributes:
        type (:obj:`str`): ``document``.
        media (:obj:`str` | :class:`telegram.InputFile`): File to send.
        caption (:obj:`str`): Optional. Caption of the document to be sent.
        parse_mode (:obj:`str`): Optional. The parse mode to use for text formatting.
        thumb (:class:`telegram.InputFile`): Optional. Thumbnail of the file to send.

    Args:
        media (:obj:`str` | `filelike object` | :class:`telegram.Document`): File to send. Pass a
            file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP
            URL for Telegram to get a file from the Internet. Lastly you can pass an existing
            :class:`telegram.Document` object to send.
        caption (:obj:`str`, optional): Caption of the document to be sent, 0-1024 characters after
            entities parsing.
        parse_mode (:obj:`str`, optional): Send Markdown or HTML, if you want Telegram apps to show
            bold, italic, fixed-width text or inline URLs in the media caption. See the constants
            in :class:`telegram.ParseMode` for the available modes.
        thumb (`filelike object`, optional): Thumbnail of the file sent; can be ignored if
            thumbnail generation for the file is supported server-side. The thumbnail should be
            in JPEG format and less than 200 kB in size. A thumbnail's width and height should
            not exceed 320. Ignored if the file is not uploaded using multipart/form-data.
            Thumbnails can't be reused and can be only uploaded as a new file.
    """

    media: InitVar[Union[str, FileLike, Document]]
    thumb: InitVar[FileLike] = None
    caption: Optional[str] = None
    parse_mode: Optional[Union[str, DefaultValue]] = DEFAULT_NONE

    def __post_init__(self, media: Union[str, FileLike, Document], thumb: FileLike = None) -> None:
        self.type = 'document'

        if isinstance(media, Document):
            self.media: Union[str, InputFile] = media.file_id
        elif InputFile.is_file(media):
            media = cast(IO, media)
            self.media = InputFile(media, attach=True)
        else:
            self.media = media  # type: ignore[assignment]

        if thumb:
            if InputFile.is_file(thumb):
                thumb = cast(IO, thumb)
                self.thumb = InputFile(thumb, attach=True)
            else:
                self.thumb = thumb  # type: ignore[assignment]
