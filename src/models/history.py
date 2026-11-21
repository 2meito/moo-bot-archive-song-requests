import datetime

import msgspec


class User(msgspec.Struct):
    userid: str
    username: str


class SongRequest(msgspec.Struct):
    type: str
    youtube_id: str
    title: str
    by: User
    length: int
    start: int
    end: int
    date: datetime.datetime


class History(msgspec.Struct):
    list: list[SongRequest]
    _total: int
