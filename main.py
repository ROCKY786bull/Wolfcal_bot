import ccxt
import pandas as pd
import pandas_ta as ta
import telebot
import schedule
import time

TELEGRAM_BOT_TOKEN =
TELEGRAM_CHAT_ID 

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def check_coins():
    exchange = ccxt.binance()
    coins = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'XRP/USDT', 'SOL/USDT']
    
    for coin in coins:
        try:
            data = exchange.fetch_ohlcv(coin, timeframe='1h', limit=50)
            df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
            df['rsi'] = ta.rsi(df['close'], length=14)
            df['ema7'] = ta.ema(df['close'], length=7)
            df['ema25'] = ta.ema(df['close'], length=25)

            if df['rsi'].iloc[-2] < 30 and df['rsi'].iloc[-1] > df['rsi'].iloc[-2] and df['ema7'].iloc[-1] > df['ema25'].iloc[-1]:
                msg = f"🔥 *Bullish Alert!* {coin}\n\n📈 RSI Rising from Oversold\n📊 EMA(7) > EMA(25)\n\n🖼️ [Chart](https://www.tradingview.com/chart/?symbol=BINANCE:{coin.replace('/', '')})"
                bot.send_message(TELEGRAM_CHAT_ID, msg, parse_mode='Markdown', disable_web_page_preview=False)
        except Exception as e:
            print(f"Error for {coin}: {e}")

schedule.every(30).minutes.do(check_coins)

while True:
    schedule.run_pending()
    time.sleep(5)
