import msgspec

class Status(msgspec.Struct):
    autojoin: bool
    joined: bool
    moderated: bool


class Channel(msgspec.Struct):
    trial: bool
    points: int
    userid: str
    username: str


class Meta(msgspec.Struct):
    status: Status
    channel: Channel
    version: int
    assistant: str