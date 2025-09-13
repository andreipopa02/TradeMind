from business.bto.trade_bto import TradeBTO
from persistence.dto.trade_dto import TradeDTO


class TradeMapper:
    @staticmethod
    def dto_to_bto(trade_dto: TradeDTO) -> TradeBTO:
        return TradeBTO(
            id=trade_dto.id,
            user_id=trade_dto.user_id,

            market=trade_dto.market,
            volume=trade_dto.volume,
            type=trade_dto.type,

            open_date=trade_dto.open_date,
            open_time=trade_dto.open_time,
            close_date=trade_dto.close_date,
            close_time=trade_dto.close_time,
            session=trade_dto.session,

            open_price=trade_dto.open_price,
            close_price=trade_dto.close_price,
            sl_price=trade_dto.sl_price,
            tp_price=trade_dto.tp_price,

            swap=trade_dto.swap,
            commission=trade_dto.commission,
            profit=trade_dto.profit,
            pips=trade_dto.pips,

            link_photo=trade_dto.link_photo,
            source_type=trade_dto.source_type,
            backtest_id=trade_dto.backtest_id
        )

    @staticmethod
    def bto_to_dto(trade_bto: TradeBTO) -> TradeDTO:
        return TradeDTO(
            id=trade_bto.id,
            user_id=trade_bto.user_id,

            market=trade_bto.market,
            volume=trade_bto.volume,
            type=trade_bto.type,

            open_date=trade_bto.open_date,
            open_time=trade_bto.open_time,
            close_date=trade_bto.close_date,
            close_time=trade_bto.close_time,
            session=trade_bto.session,

            open_price=trade_bto.open_price,
            close_price=trade_bto.close_price,
            sl_price=trade_bto.sl_price,
            tp_price=trade_bto.tp_price,

            swap=trade_bto.swap,
            commission=trade_bto.commission,
            profit=trade_bto.profit,
            pips=trade_bto.pips,

            link_photo=trade_bto.link_photo,
            source_type=trade_bto.source_type,
            backtest_id=trade_bto.backtest_id
        )
