from .appkafka import produce
from ..core.domain import Request

async def post_on_topic(item: Request):
    return produce(item)
