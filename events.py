import logging

from dateutil.parser import parse

from api import create_timeoff_events

logger = logging.getLogger(__name__)


async def process_event(event: dict) -> None:
    logger.info("Processing event: {}".format(event))
    event_type, data = parse_event(event)
    if event_type == "leave_approvalV2":
        match data:
            case {
                "leave_start_time": start_time,
                "leave_end_time": end_time,
                "user_id": user_id,
                "leave_reason": leave_reason,
                "leave_name": leave_name,
                "i18n_resources": i18n_resources,
                **__,
            }:
                title = next(
                    item for item in i18n_resources if item["locale"] == "zh_cn"
                )["texts"][leave_name]
                await create_timeoff_events(
                    user_id=user_id,
                    start_time=int(parse(start_time).timestamp()),
                    end_time=int(parse(end_time).timestamp()),
                    title=title,
                    description=leave_reason,
                )
            case _:
                pass
    return event


def parse_event(event: dict):
    match event:
        case {
            "schema": "2.0",
            "header": {"event_type": event_type},
            "event": event,
            **__,
        }:
            return event_type, event
        case {"event": {"type": type}}:
            return type, event["event"]