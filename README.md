# Telegram Bot Template - Aiogram 3.x

Bu shablon Aiogram 3.x versiyasi uchun yozilgan Telegram bot strukturasidir.

## 📋 Talablar

- Python 3.10+
- aiogram 3.4.0+

## 🚀 O'rnatish

### 1. Virtual muhit yaratish

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 2. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 3. .env faylini yaratish

`.env-shablon` faylidan nusxa oling va `.env` deb nomlang:

```bash
cp .env-shablon .env
```

Keyin `.env` faylini tahrirlang:

```env
ADMINS=123456789
BOT_TOKEN=your_bot_token_here
```

### 4. Botni ishga tushirish

```bash
python app.py
```

## 📁 Loyiha strukturasi

```
telegram-bot/
├── app.py              # Asosiy fayl - botni ishga tushirish
├── loader.py           # Bot va Dispatcher yaratish (eski versiya uchun)
├── requirements.txt    # Kutubxonalar ro'yxati
├── .env-shablon        # Muhit o'zgaruvchilari namunasi
├── .gitignore          # Git ignore fayli
│
├── data/               # Konfiguratsiya
│   ├── __init__.py
│   └── config.py       # Muhit o'zgaruvchilarini o'qish
│
├── filters/            # Maxsus filterlar
│   ├── __init__.py
│   └── is_admin.py     # Admin filteri
│
├── handlers/           # Handlerlar
│   ├── __init__.py     # Routerlarni sozlash
│   ├── users/          # Foydalanuvchilar uchun handlerlar
│   │   ├── __init__.py
│   │   ├── start.py    # /start buyrug'i
│   │   ├── help.py     # /help buyrug'i
│   │   └── echo.py     # Echo handler
│   ├── groups/         # Guruhlar uchun handlerlar
│   │   └── __init__.py
│   ├── channels/       # Kanallar uchun handlerlar
│   │   └── __init__.py
│   └── errors/         # Xatolarni ushlash
│       ├── __init__.py
│       └── error_handler.py
│
├── keyboards/          # Klaviaturalar
│   ├── __init__.py
│   ├── default/        # Oddiy klaviaturalar
│   │   └── __init__.py
│   └── inline/         # Inline klaviaturalar
│       └── __init__.py
│
├── middlewares/        # Middlewarelar
│   ├── __init__.py
│   └── throttling.py   # Antiflood middleware
│
├── states/             # FSM holatlar
│   └── __init__.py
│
└── utils/              # Yordamchi funksiyalar
    ├── __init__.py
    ├── notify_admins.py    # Adminlarga xabar yuborish
    ├── set_bot_commands.py # Bot buyruqlarini o'rnatish
    ├── db_api/             # Database API
    │   └── __init__.py
    └── misc/               # Boshqa yordamchi funksiyalar
        ├── __init__.py
        ├── logging.py
        └── throttling.py
```

## 🔧 Aiogram 2.x dan 3.x ga o'tish farqlari

### 1. Bot va Dispatcher yaratish

**Eski (2.x):**
```python
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
```

**Yangi (3.x):**
```python
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
```

### 2. Handlerlar

**Eski (2.x):**
```python
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer("Salom!")
```

**Yangi (3.x):**
```python
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Salom!")
```

### 3. Botni ishga tushirish

**Eski (2.x):**
```python
from aiogram import executor
executor.start_polling(dp, on_startup=on_startup)
```

**Yangi (3.x):**
```python
import asyncio

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
```

### 4. Middlewarelar

**Eski (2.x):**
```python
from aiogram.dispatcher.middlewares import BaseMiddleware

class MyMiddleware(BaseMiddleware):
    async def on_process_message(self, message, data):
        pass
```

**Yangi (3.x):**
```python
from aiogram import BaseMiddleware

class MyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        return await handler(event, data)
```

### 5. Filterlar

**Eski (2.x):**
```python
from aiogram.dispatcher.filters import BoundFilter

class IsAdmin(BoundFilter):
    async def check(self, message):
        return message.from_user.id in ADMINS
```

**Yangi (3.x):**
```python
from aiogram.filters import BaseFilter

class IsAdmin(BaseFilter):
    async def __call__(self, message):
        return message.from_user.id in ADMINS
```

## 📚 Foydali havolalar

- [Aiogram rasmiy dokumentatsiyasi](https://docs.aiogram.dev/)
- [Aiogram GitHub](https://github.com/aiogram/aiogram)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## 📝 Litsenziya

MIT

## 👤 Muallif

Telegram bot shabloni aiogram 3.x uchun moslashtirildi.
