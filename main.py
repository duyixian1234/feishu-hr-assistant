"""
Define the FastAPI application.
"""

import logging

from fastapi import FastAPI, Request

import storage
from events import process_event

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("./log/app.log")],
)
logger = logging.getLogger(__name__)
storage.init_db()
app = FastAPI()


@app.post("/")
async def callback(request: Request) -> dict:
    """event callback handler"""
    event = await request.json()
    await process_event(event)
    return event


logger.info("App initialized.")
