import logging

from fastapi import FastAPI, Request

from events import process_event

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/")
async def callback(request: Request) -> dict:
    event = await request.json()
    await process_event(event)
    return event


logger.info("App initialized.")
