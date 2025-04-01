from event.controller import EventConsumeController
from event.schema.fast import CreateStageFast
from event.schema.official import CreateStageOfficial
from event.schema.stage import StageConfirmReq
from event.schema.ticket import TicketShopBuyReq


event_topic = {
    'stage_create_fast': (EventConsumeController.create_stage_fast, CreateStageFast),
    'stage_create_official': (EventConsumeController.create_stage_official, CreateStageOfficial),
    'stage_confirm': (EventConsumeController.stage_confirm, StageConfirmReq),
    'ticket_point_minus': (EventConsumeController.ticket_buy, TicketShopBuyReq)
}