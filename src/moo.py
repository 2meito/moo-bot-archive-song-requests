from typing import Any, Literal, Generator

import msgspec
import requests

from models import Meta
from models.history import SongRequest, History

class Moo:
    def __init__(self) -> None:
        self._api = MooAPI()

    def get_song_requests_history(self, username: str) -> Generator[SongRequest, None, None]:
        meta = self._api.meta(username)
        return self._api.songrequests_history(meta.channel.userid)


class MooAPI:
    root = "https://moo.bot/a/1"

    def __init__(self):
        self.session = requests.Session()

    def _call(self, uri, params=None) -> dict[str, Any]:
        url = self.root + uri
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def meta(self, name: str) -> Meta:
        uri = "/channel/meta"
        params = {
            "name": name,
        }
        data = self._call(uri, params)
        return msgspec.convert(data, type=Meta)

    def songrequests_history(
            self,
            channel: str,
            _limit: int = 50,
            _offset: int = 0,
            _order: Literal["date"] = "date",
            _direction: Literal["desc", "asc"] = "desc"
    ) -> Generator[SongRequest, None, None]:
        uri = "/channel/features/songrequests/history"
        params = {
            "_limit": _limit,
            "_offset": _offset,
            "_order": _order,
            "channel": channel,
            "_direction": _direction,
        }
        has_more = True
        while has_more:
            data = self._call(uri, params)
            history = msgspec.convert(data, type=History)
            yield from history.list
            params["_offset"] += params["_limit"]
            has_more = bool(history.list)

