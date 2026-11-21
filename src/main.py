import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Iterable, NoReturn

import msgspec

from models.config import Config
from models.history import SongRequest
from moo import Moo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)
log = logging.getLogger(__name__)


def append_jsonl(outfile, song_requests: Iterable[SongRequest]) -> None:
    encoder = msgspec.json.Encoder()
    with (open(outfile, "ab+")) as f:
        for song_request in song_requests:
            f.write(encoder.encode(song_request))
            f.write(b"\n")


def poll(moo: Moo, config: Config, minutes: int = 5)-> NoReturn:
    while True:
        log.info(f"Getting {config.username} song request history...")
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S%z")
        outfile = Path(config.outdir) / f"{config.username}_{timestamp}.jsonl"
        append_jsonl(outfile, moo.get_song_requests_history(config.username))
        log.info(f"History saved to {outfile}.")
        log.info(f"Waiting {minutes} minutes...")
        time.sleep(minutes * 60)


def main()-> None:
    os.chdir("..")
    with open("config.json", "rb") as f:
        config = msgspec.json.decode(f.read(), type=Config)
    os.makedirs(config.outdir, exist_ok=True)
    moo = Moo()
    poll(moo, config)


if __name__ == "__main__":
    main()
