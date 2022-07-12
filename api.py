"""Feishu API"""
import logging

import httpx

from config import get_settings

logger = logging.getLogger(__name__)
default_client = httpx.AsyncClient()


async def get_access_token(client: httpx.AsyncClient = default_client) -> str:
    """Get access token"""
    resp = await client.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": get_settings().app_id, "app_secret": get_settings().app_secret},
    )
    return resp.json()["tenant_access_token"]


async def create_timeoff_events(
    user_id: str, start_time: int, end_time: int, title: str, description: str
) -> None:
    """Create timeoff events"""
    resp = await default_client.post(
        "https://open.feishu.cn/open-apis/calendar/v4/timeoff_events?user_id_type=user_id",
        json={
            "timezone": "Asia/Shanghai",
            "user_id": user_id,
            "start_time": start_time,
            "end_time": end_time,
            "title": title,
            "description": description,
        },
        headers={"Authorization": f"Bearer {await get_access_token()}"},
    )
    logger.info("Create timeoff event: %s", resp.json())
