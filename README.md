# 🤖 Telegram Guruh Boti Shablon (Aiogram 3.x)

Guruhlarni boshqarish uchun tayyor Telegram bot shabloni - moderatsiya, a'zolarni boshqarish va guruh sozlamalari.

---

## 📋 Imkoniyatlar

- ✅ Aiogram 3.x versiyasi
- ✅ Moderatsiya buyruqlari (ban, unban, ro, unro)
- ✅ Guruh sozlamalarini o'zgartirish (rasm, nom, tavsif)
- ✅ Yangi a'zolarni kutib olish
- ✅ Guruh/Shaxsiy chat filterlari
- ✅ Admin tekshirish filterlari
- ✅ Antiflood himoyasi
- ✅ Xatolarni ushlash

---

## 🚀 O'rnatish

### 1. Repozitoriyani yuklab oling

```bash
git clone <repo-url>
cd telegram-bot-shablon-group
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

### 4. `.env` faylini yarating

```bash
cp .env.example .env
```

---

## ⚙️ Sozlamalar (.env fayli)

```env
# Bot token - @BotFather dan oling
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Admin ID lar (vergul bilan ajratilgan)
# Bu adminlar moderatsiya buyruqlarini ishlata oladi
ADMINS=123456789,987654321
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

---

## 📝 Buyruqlar ro'yxati

### 🛡️ Moderatsiya buyruqlari

Barcha moderatsiya buyruqlarini `/` yoki `!` bilan ishlatish mumkin.

| Buyruq | Vazifasi | Ishlatish |
|--------|----------|-----------|
| `/ro` yoki `!ro` | Foydalanuvchini read-only rejimiga o'tkazish | Xabarga reply qilib `/ro 10 sabab` |
| `/unro` yoki `!unro` | Read-only dan chiqarish | Xabarga reply qilib `/unro` |
| `/ban` yoki `!ban` | Foydalanuvchini guruhdan haydash | Xabarga reply qilib `/ban` |
| `/unban` yoki `!unban` | Bandan chiqarish | Xabarga reply qilib `/unban` |

#### Misollar:

```
# 10 daqiqaga read-only (sabab bilan)
/ro 10 spam uchun

# 5 daqiqaga read-only (default)
!ro

# Bandan chiqarish
/unban
```

### ⚙️ Guruh sozlamalari

| Buyruq | Vazifasi | Ishlatish |
|--------|----------|-----------|
| `/set_photo` | Guruh rasmini o'zgartirish | Rasmga reply qilib `/set_photo` |
| `/set_title` | Guruh nomini o'zgartirish | Matn xabariga reply qilib `/set_title` |
| `/set_description` | Guruh tavsifini o'zgartirish | Matn xabariga reply qilib `/set_description` |

---

## 🤖 Avtomatik xabarlar

### Yangi a'zo qo'shilganda
Bot avtomatik ravishda yangi a'zolarni kutib oladi:
```
Xush kelibsiz, @username.
```

### A'zo ketganda
```
@username guruhni tark etdi
```

### Admin haydaganda
```
Username guruhdan haydaldi. Admin: @admin_username
```

---

## ⚠️ Muhim: Botni guruhga admin qilish

**Bot to'g'ri ishlashi uchun uni guruhga admin qilishingiz SHART!**

### Qadamlar:

1. Guruhni oching
2. Guruh nomini bosing → **Tahrirlash** → **Administratorlar**
3. **Administrator qo'shish** → Botingizni toping
4. Quyidagi ruxsatlarni bering:
   - ✅ Xabarlarni o'chirish (Delete messages)
   - ✅ Foydalanuvchilarni cheklash (Restrict members)
   - ✅ Foydalanuvchilarni bloklash (Ban users)
   - ✅ Guruh ma'lumotlarini o'zgartirish (Change group info) - agar `/set_photo`, `/set_title` ishlatmoqchi bo'lsangiz

---

## 📁 Loyiha strukturasi

```
telegram-bot-group/
├── app.py                  # Asosiy fayl
├── loader.py               # Bot va Dispatcher
├── .env                    # Sozlamalar
├── requirements.txt        # Kutubxonalar
│
├── data/
│   └── config.py           # Konfiguratsiya
│
├── filters/
│   ├── is_admin.py         # Admin tekshirish
│   ├── is_group.py         # Guruh tekshirish
│   └── is_private.py       # Shaxsiy chat tekshirish
│
├── handlers/
│   ├── users/              # Shaxsiy chat handlerlari
│   │   ├── start.py
│   │   ├── help.py
│   │   └── echo.py
│   ├── groups/             # Guruh handlerlari
│   │   ├── moderator.py    # /ro, /ban, /unban
│   │   ├── edit.py         # /set_photo, /set_title
│   │   ├── service.py      # Yangi a'zo, ketgan a'zo
│   │   └── start.py
│   └── errors/
│       └── error_handler.py
│
├── middlewares/
│   └── throttling.py       # Antiflood
│
├── keyboards/              # Klaviaturalar
├── states/                 # FSM holatlar
└── utils/                  # Yordamchi funksiyalar
```

---

## 🔧 Filterlar

### IsGroup - Guruhda tekshirish
```python
from filters import IsGroup

@router.message(IsGroup())
async def only_in_group(message: Message):
    await message.answer("Bu xabar faqat guruhda ko'rinadi")
```

### IsPrivate - Shaxsiy chatda tekshirish
```python
from filters import IsPrivate

@router.message(IsPrivate())
async def only_in_private(message: Message):
    await message.answer("Bu xabar faqat shaxsiy chatda ko'rinadi")
```

### IsAdminFilter - Admin tekshirish
```python
from filters import IsAdminFilter

@router.message(IsAdminFilter())
async def only_for_admins(message: Message):
    await message.answer("Bu xabar faqat adminlar uchun")
```

### Kombinatsiya
```python
@router.message(IsGroup(), Command("ban"), IsAdminFilter())
async def ban_in_group_by_admin(message: Message):
    # Faqat guruhda, faqat admin ishlatishi mumkin
    pass
```

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

## ➕ Yangi buyruq qo'shish

### 1. Handler yarating

`handlers/groups/` papkasida yangi fayl yoki mavjud faylga:

```python
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from filters import IsGroup, IsAdminFilter

router = Router(name="my_commands")


@router.message(IsGroup(), Command("kick"), IsAdminFilter())
async def kick_user(message: Message, bot: Bot):
    """Foydalanuvchini guruhdan chiqarish (qayta qo'shilishi mumkin)"""
    
    if not message.reply_to_message:
        await message.answer("❗ Foydalanuvchi xabariga reply qiling!")
        return
    
    member = message.reply_to_message.from_user
    
    # Kick = ban + unban
    await bot.ban_chat_member(
        chat_id=message.chat.id, 
        user_id=member.id
    )
    await bot.unban_chat_member(
        chat_id=message.chat.id, 
        user_id=member.id
    )
    
    await message.answer(f"👢 {member.full_name} guruhdan chiqarildi")
```

### 2. Routerni ulang

`handlers/groups/__init__.py` da:

```python
from .my_commands import router as my_router
groups_router.include_router(my_router)
```

---

## ❓ Ko'p so'raladigan savollar

### Bot buyruqlarga javob bermayapti?
- Bot guruhda admin ekanligini tekshiring
- Foydalanuvchi `.env` dagi ADMINS ro'yxatida borligini tekshiring
- Group Privacy sozlamasini tekshiring (@BotFather → /mybots → Bot Settings → Group Privacy → Turn off)

### "Not enough rights" xatosi?
- Botga kerakli admin huquqlarini bering
- Siz haydamoqchi bo'lgan odam bot/guruh egasi bo'lishi mumkin

### Yangi a'zo xabari kelmayapti?
- Bot guruhda admin bo'lishi kerak
- Guruh sozlamalarida "Yangi a'zolar haqida xabar berish" yoqilgan bo'lishi kerak

### Bot shaxsiy chatda ham guruh buyruqlarini qabul qiladimi?
- Yo'q, `IsGroup()` filteri faqat guruhlarda ishlashini ta'minlaydi

---

## 📞 Aloqa

Savollar bo'lsa, murojaat qiling:
- Telegram: [Abruisdev](https://t.me/abruisdev)

---

## 📄 Litsenziya

MIT License - Erkin foydalanishingiz mumkin.
