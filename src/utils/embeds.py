import datetime
from typing import Any
from discord import Embed
from discord import Color, Colour, Embed
from discord.embeds import EmbedAuthor, EmbedField, EmbedFooter, EmbedMedia
from discord.types.embed import EmbedType
import datetime

class SuccessEmbed(Embed):
    def __init__(
            self, 
            *, 
            colour: int | Colour | None = None, 
            color: int | Colour | None = None, 
            title: Any | None = None, 
            type: EmbedType = "rich", 
            url: Any | None = None, 
            description: Any | None = None, 
            timestamp = None, 
            fields: list[EmbedField] | None = None, 
            author: EmbedAuthor | None = None, 
            footer: EmbedFooter | None = None, 
            image: str | EmbedMedia | None = None, 
            thumbnail: str | EmbedMedia | None = None
        ):
        color = color if color else Color.green()
        timestamp = timestamp if timestamp else datetime.datetime.now()
        super().__init__(
            colour=colour,
            color=color, 
            title=title, 
            type=type, 
            url=url, 
            description=description, 
            timestamp=timestamp, fields=fields, 
            author=author, 
            footer=footer, 
            image=image, 
            thumbnail=thumbnail
        )

class ErrorEmbed(Embed):
    def __init__(
            self, 
            *, 
            colour: int | Colour | None = None, 
            color: int | Colour | None = None, 
            title: Any | None = None, 
            type: EmbedType = "rich", 
            url: Any | None = None, 
            description: Any | None = None, 
            timestamp = None, 
            fields: list[EmbedField] | None = None, 
            author: EmbedAuthor | None = None, 
            footer: EmbedFooter | None = None, 
            image: str | EmbedMedia | None = None, 
            thumbnail: str | EmbedMedia | None = None
        ):
        color = color if color else Color.red()
        timestamp = timestamp if timestamp else datetime.datetime.now()
        super().__init__(
            colour=colour,
            color=color, 
            title=title, 
            type=type, 
            url=url, 
            description=description, 
            timestamp=timestamp, fields=fields, 
            author=author, 
            footer=footer, 
            image=image, 
            thumbnail=thumbnail
        )

class UnsureEmbed(Embed):
    def __init__(
            self, 
            *, 
            colour: int | Colour | None = None, 
            color: int | Colour | None = None, 
            title: Any | None = None, 
            type: EmbedType = "rich", 
            url: Any | None = None, 
            description: Any | None = None, 
            timestamp = None, 
            fields: list[EmbedField] | None = None, 
            author: EmbedAuthor | None = None, 
            footer: EmbedFooter | None = None, 
            image: str | EmbedMedia | None = None, 
            thumbnail: str | EmbedMedia | None = None
        ):
        color = color if color else Color.orange()
        timestamp = timestamp if timestamp else datetime.datetime.now()
        super().__init__(
            colour=colour,
            color=color, 
            title=title, 
            type=type, 
            url=url, 
            description=description, 
            timestamp=timestamp, fields=fields, 
            author=author, 
            footer=footer, 
            image=image, 
            thumbnail=thumbnail
        )