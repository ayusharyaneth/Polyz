from models.schemas import UserSettings, TradeEvent

class RiskManager:
    @staticmethod
    def calculate_trade_size(event: TradeEvent, settings: UserSettings, user_balance: float) -> float:
        if not settings.is_active:
            return 0.0
            
        base_size = (user_balance / event.trader_balance) * event.position_size
        copy_size = base_size * (settings.copy_percentage / 100.0)
        
        if copy_size > settings.max_trade_size:
            copy_size = settings.max_trade_size
            
        return copy_size

    @staticmethod
    def validate_trade(copy_size: float, current_exposure: float, settings: UserSettings) -> bool:
        if copy_size <= 0: return False
        if current_exposure + copy_size > settings.risk_limit: return False
        return True
