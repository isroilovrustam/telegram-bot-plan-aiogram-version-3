# 🤖 Telegram Bot Shablon (Aiogram 3.x)

Majburiy obuna (forced subscription) funksiyasi bilan tayyor Telegram bot shabloni.

---

## 📋 Imkoniyatlar

- ✅ Aiogram 3.x versiyasi
- ✅ Majburiy obuna (bir nechta kanal)
- ✅ Username yoki Kanal ID orqali ishlash
- ✅ Antiflood (throttling) himoyasi
- ✅ Xatolarni ushlash (error handler)
- ✅ Modulli struktura

---

## 🚀 O'rnatish

### 1. Repozitoriyani yuklab oling

```bash
git clone <repo-url>
cd telegram-bot-shablon
```

### 2. Virtual muhit yarating

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Kutubxonalarni o'rnating

```bash
pip install -r requirements.txt
```

### 4. `.env` faylini sozlang

`.env.example` faylidan nusxa oling:

```bash
cp .env.example .env
```

---

## ⚙️ Sozlamalar (.env fayli)

`.env` faylini oching va quyidagilarni to'ldiring:

```env
# Bot token - @BotFather dan oling
BOT_TOKEN=1234567890:ABCdefGHIjklMNOdfhdpqrsTUVwxyz

# Admin ID lar (vergul bilan ajratilgan)
ADMINS=123456789,987654321

# Majburiy obuna kanallari (vergul bilan ajratilgan)
CHANNELS=@channel_username,-1001234567890
```

### 🔑 BOT_TOKEN olish

1. Telegram da [@BotFather](https://t.me/BotFather) ga yozing
2. `/newbot` buyrug'ini yuboring
3. Bot nomini va username ni kiriting
4. Token ni nusxalab `.env` ga yozing

### 👤 ADMINS - Admin ID olish

1. Telegram da [@userinfobot](https://t.me/userinfobot) ga yozing
2. `/start` bosing
3. `Id` qatoridagi raqamni nusxalang

### 📢 CHANNELS - Kanal sozlash

#### Kanal username orqali:
```env
CHANNELS=@my_channel,@another_channel
```

#### Kanal ID orqali:
```env
CHANNELS=-1001234567890,-1009876543210
```

#### Aralash (username va ID):
```env
CHANNELS=@my_channel,-1001234567890
```

---

## 📢 Kanal ID ni qanday olish mumkin?

### 1-usul: @userinfobot orqali
1. Kanalingizdan istalgan xabarni [@userinfobot](https://t.me/userinfobot) ga forward qiling
2. `Id` qatoridagi raqamni nusxalang (masalan: `-1001234567890`)

### 2-usul: @getmyid_bot orqali
1. [@getmyid_bot](https://t.me/getmyid_bot) ni kanalingizga admin qiling
2. Kanalda istalgan xabar yozing
3. Bot kanal ID sini ko'rsatadi

### 3-usul: Web orqali
1. Telegram Web ([web.telegram.org](https://web.telegram.org)) ga kiring
2. Kanalingizni oching
3. URL dagi raqamni oling va oldiga `-100` qo'shing

---

## ⚠️ Muhim: Botni kanalga admin qilish

**Bot to'g'ri ishlashi uchun uni barcha kanallarga admin qilishingiz SHART!**

### Qadamlar:

1. Kanalingizni oching
2. Kanal nomini bosing → **Administratorlar**
3. **Administrator qo'shish** → Botingizni toping
4. Quyidagi ruxsatlarni bering:
   - ✅ Foydalanuvchilarni boshqarish (Invite users via link)

Agar bot admin bo'lmasa, obunani tekshira olmaydi!

---

## 🏃 Botni ishga tushirish

```bash
python app.py
```

Muvaffaqiyatli ishga tushganda:
```
Bot ishga tushdi!
Start polling
Run polling for bot @your_bot...
```

---

## 📁 Loyiha strukturasi

```
telegram-bot/
├── app.py                  # Asosiy fayl
├── loader.py               # Bot va Dispatcher
├── .env                    # Sozlamalar (yaratilishi kerak)
├── .env.example            # Sozlamalar namunasi
├── requirements.txt        # Kutubxonalar
│
├── data/
│   └── config.py           # Konfiguratsiya (TOKEN, ADMINS, CHANNELS)
│
├── handlers/
│   ├── users/
│   │   ├── start.py        # /start buyrug'i
│   │   ├── help.py         # /help buyrug'i
│   │   ├── subscription.py # Obuna tekshirish callback
│   │   └── echo.py         # Echo handler
│   └── errors/
│       └── error_handler.py # Xatolarni ushlash
│
├── keyboards/
│   ├── inline/
│   │   └── subscription.py # Obuna tugmalari
│   └── default/            # Reply klaviaturalar
│
├── middlewares/
│   ├── checksub.py         # Majburiy obuna middleware
│   └── throttling.py       # Antiflood middleware
│
├── states/                 # FSM holatlar
├── filters/                # Maxsus filterlar
└── utils/
    └── misc/
        └── subscription.py # Obuna tekshirish funksiyasi
```

---

## 🔧 Qo'shimcha sozlamalar

### Majburiy obunani o'chirish

Agar majburiy obuna kerak bo'lmasa, `middlewares/__init__.py` faylida quyidagi qatorlarni o'chiring:

```python
# Bu qatorlarni o'chiring yoki kommentga oling:
dp.message.middleware(CheckSubscriptionMiddleware())
dp.callback_query.middleware(CheckSubscriptionMiddleware())
```

### Throttling (antiflood) vaqtini o'zgartirish

`middlewares/__init__.py` faylida:

```python
# limit - soniyalarda (default: 0.5)
dp.message.middleware(ThrottlingMiddleware(limit=1.0))  # 1 soniya
```

---

## ❓ Ko'p so'raladigan savollar

### Bot "Start polling" da qotib qoldi?
- Internet aloqasini tekshiring
- BOT_TOKEN to'g'riligini tekshiring

### Obuna tekshirilmayapti?
- Bot kanalda admin ekanligini tekshiring
- Kanal username/ID to'g'ri yozilganini tekshiring
- Private kanal bo'lsa, faqat ID ishlaydi

### "Chat not found" xatosi?
- Kanal ID to'g'ri yozilganini tekshiring
- ID `-100` bilan boshlanishi kerak

### Bot xabar yubormayapti?
- Foydalanuvchi botni bloklagan bo'lishi mumkin
- Bot tokenni tekshiring

---

## 📞 Aloqa

Savollar bo'lsa, murojaat qiling:
- Telegram: [@your_username](https://t.me/your_username)

---

## 📄 Litsenziya

MIT License - Erkin foydalanishingiz mumkin.