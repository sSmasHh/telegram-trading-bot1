import re
import os
from telethon import TelegramClient, events

# Получаем данные из переменных окружения (Render)
API_ID = int(os.getenv("API_ID"))  # API ID
API_HASH = os.getenv("API_HASH")  # API Hash
SESSION_NAME = "session"  # Имя файла сессии

# Подключаемся к Telegram
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Функция для парсинга торговых сигналов
def parse_trade_signal(message_text):
    match = re.search(r'BINANCE:(ENTER|SHORT|LONG)-?(.*?), (\w+),💲current price = ([\d.]+)', message_text)
    if match:
        return {
            "action": match.group(1) + (" " + match.group(2) if match.group(2) else ""),
            "currency_pair": match.group(3),
            "price": float(match.group(4))
        }
    return None

# Обрабатываем новые сообщения из группы
@client.on(events.NewMessage)
async def handle_new_message(event):
    signal = parse_trade_signal(event.message.text)
    if signal:
        print(f"📩 Получен сигнал: {signal['action']} на {signal['currency_pair']} по цене {signal['price']}")

# Запускаем клиента
async def main():
    await client.start()
    print("✅ Бот запущен и слушает Telegram...")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
