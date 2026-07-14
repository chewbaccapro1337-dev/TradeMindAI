from app.database import save_trade

save_trade(
    user_id=1,
    symbol="BTCUSDT",
    side="BUY",
    entry=108000,
    exit_price=109500,
    risk=1,
    pnl=1500,
)

print("Сделка сохранена!")