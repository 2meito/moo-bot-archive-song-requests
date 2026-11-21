import msgspec


class Config(msgspec.Struct):
    username: str
    outdir: str
