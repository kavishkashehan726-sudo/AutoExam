"""RQ worker entry point: `python -m app.worker`."""

from redis import Redis
from rq import Queue, Worker

from app.core.config import get_settings

QUEUES = ["generation", "default"]


def main() -> None:
    connection = Redis.from_url(get_settings().redis_url)
    queues = [Queue(name, connection=connection) for name in QUEUES]
    Worker(queues, connection=connection).work()


if __name__ == "__main__":
    main()
