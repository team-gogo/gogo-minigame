from multiprocessing import Queue

from logging_loki import LokiQueueHandler

from config import LOKI_ENDPOINT

loki_handler = LokiQueueHandler(
    Queue(-1),
    url=LOKI_ENDPOINT,
    tags={"application": "GOGO-Minigame"},
    version="1",
)
