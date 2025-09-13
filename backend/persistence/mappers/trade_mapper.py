from persistence.dto.trade_dto import TradeDTO
from persistence.entities.trade_entity import TradeEntity


class TradeMapper:
    @staticmethod
    def entity_to_dto(trade: TradeEntity) -> TradeDTO:
        return TradeDTO(
            id              = trade.id,
            user_id         = trade.user_id,

            market          = trade.market,
            volume          = trade.volume,
            type            = trade.type,

            open_date       = trade.open_date,
            open_time       = trade.open_time,
            close_date      = trade.close_date,
            close_time      = trade.close_time,
            session         = trade.session,

            open_price      = trade.open_price,
            close_price     = trade.close_price,
            sl_price        = trade.sl_price,
            tp_price        = trade.tp_price,

            swap            = trade.swap,
            commission      = trade.commission,
            profit          = trade.profit,
            pips            = trade.pips,

            link_photo      = trade.link_photo,

            source_type     = trade.source_type,
            backtest_id     = trade.backtest_id
        )

    @staticmethod
    def dto_to_entity(dto: TradeDTO) -> TradeEntity:
        return TradeEntity(
            id              = dto.id,
            user_id         = dto.user_id,

            market          = dto.market,
            volume          = dto.volume,
            type            = dto.type,

            open_date       = dto.open_date,
            open_time       = dto.open_time,
            close_date      = dto.close_date,
            close_time      = dto.close_time,
            session         = dto.session,

            open_price      = dto.open_price,
            close_price     = dto.close_price,
            sl_price        = dto.sl_price,
            tp_price        = dto.tp_price,

            swap            = dto.swap,
            commission      = dto.commission,
            profit          = dto.profit,
            pips            = dto.pips,

            link_photo      = dto.link_photo,

            source_type     = dto.source_type,
            backtest_id     = dto.backtest_id
        )
