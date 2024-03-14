"""Process event data"""

import logging

from dateutil.parser import parse

import storage
from api import create_timeoff_events, delete_timeoff_events

logger = logging.getLogger(__name__)


async def process_event(event: dict) -> dict:
    """Process event data"""
    logger.info("Processing event: %s", event)
    event_type, data = parse_event(event)  # pylint:disable=unpacking-non-sequence
    logger.info("Event type: %s", event_type)
    if event_type == "leave_approvalV2":
        match data:
            case {
                "leave_start_time": start_time,
                "leave_end_time": end_time,
                "user_id": user_id,
                "leave_reason": leave_reason,
                "leave_name": leave_name,
                "i18n_resources": i18n_resources,
                "instance_code": instance_code,
                **__,
            }:
                title = next(
                    item for item in i18n_resources if item["locale"] == "zh_cn"
                )["texts"][leave_name]
                data = await create_timeoff_events(
                    user_id=user_id,
                    start_time=int(parse(start_time).timestamp()),
                    end_time=int(parse(end_time).timestamp()),
                    title=title,
                    description=leave_reason,
                )
                storage.new(data["data"]["timeoff_event_id"], instance_code)
            case _:
                pass

    if event_type == "trip_approval":
        match data:
            case {
                "employee_id": employee_id,
                "schedules": [
                    {
                        "remark": remark,
                        "trip_start_time": start_time,
                        "trip_end_time": end_time,
                    },
                    *_,
                ],
            }:
                await create_timeoff_events(
                    user_id=employee_id,
                    start_time=int(parse(start_time).timestamp()),
                    end_time=int(parse(end_time).timestamp()),
                    title="出差",
                    description=remark,
                )
            case _:
                pass

    if event_type == "leave_approval_revert":
        instance_code = data["instance_code"]
        event_id = storage.get_event_id(instance_code)
        await delete_timeoff_events(event_id)

    return event


def parse_event(event: dict) -> tuple[str, dict]:
    """Parse event data"""
    match event:
        case {
            "schema": "2.0",
            "header": {"event_type": event_type},
            "event": event,
            **__,
        }:
            return event_type, event
        case {"event": {"type": event_type, **__}, **___}:
            return event_type, event["event"]
        case {"type": _type, **__}:
            return _type, event
        case _:
            return "unknown", event
