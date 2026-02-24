# 🗄️ SQLite Ma'lumotlar Bazasi — Qo'llanma

## 📋 Mundarija

- [O'rnatish](#-ornatish)
- [Fayl tuzilmasi](#-fayl-tuzilmasi)
- [Ishlash tartibi](#-ishlash-tartibi)
- [Jadvallar](#-jadvallar)
- [Foydalanuvchilar — Users](#-foydalanuvchilar--users)
- [Mahsulotlar — Products](#-mahsulotlar--products)
- [Buyurtmalar — Orders](#-buyurtmalar--orders)
- [Umumiy metodlar](#-umumiy-metodlar)
- [Handlerda ishlatish misollari](#-handlerda-ishlatish-misollari)
- [Ko'p uchraydigan xatolar](#-kop-uchraydigan-xatolar)
- [Barcha metodlar jadvali](#-barcha-metodlar-jadvali)

---

## 📦 O'rnatish

```bash
pip install aiosqlite
```

---

## 📁 Fayl tuzilmasi

Shablonga qo'shilgan/o'zgartirilgan fayllar:

```
telegram-bot/
├── app.py                          ← 🔄 db.create() va db.close() qo'shildi
├── main.db                         ← 🆕 Bot ishga tushganda avtomatik yaratiladi
│
├── utils/
│   └── db_api/
│       ├── __init__.py             ← 🔄 db obyektini yaratadi
│       └── sqlite.py              ← 🆕 Database klassi (barcha metodlar)
│
└── handlers/
    ├── users/
    │   └── start.py               ← 🔄 /start da foydalanuvchini bazaga yozadi
    └── errors/
        └── error_handler.py       ← 🔄 ErrorEvent ga tuzatildi (aiogram 3.x)
```

---

## ⚙️ Ishlash tartibi

**Istalgan faylda bazani chaqirish — faqat 1 qator:**

```python
from utils.db_api import db
```

**Bot ishga tushganda (app.py da avtomatik):**

```
1. await db.create()         → main.db faylini ochadi
2. await db.create_tables()  → users, products, orders jadvallarini yaratadi
3. Bot ishlaydi...
4. await db.close()          → Bazani yopadi (bot to'xtaganda)
```

---

## 📐 Jadvallar

Bot ishga tushganda 3 ta jadval avtomatik yaratiladi:

### 👤 users — Foydalanuvchilar

| Ustun | Tur | Tavsif |
|-------|-----|--------|
| `id` | INTEGER | Tartib raqam (avtomatik: 1, 2, 3, ...) |
| `telegram_id` | INTEGER | Telegram ID (unikal, takrorlanmaydi) |
| `full_name` | TEXT | To'liq ism |
| `username` | TEXT | @username (bo'lmasligi mumkin) |
| `phone` | TEXT | Telefon raqam |
| `created_at` | TEXT | Ro'yxatdan o'tgan vaqti (avtomatik) |

### 📦 products — Mahsulotlar

| Ustun | Tur | Tavsif |
|-------|-----|--------|
| `id` | INTEGER | Tartib raqam (avtomatik) |
| `name` | TEXT | Mahsulot nomi |
| `description` | TEXT | Tavsifi |
| `price` | REAL | Narxi (kasr son) |
| `category` | TEXT | Kategoriya |
| `created_at` | TEXT | Qo'shilgan vaqti (avtomatik) |

### 🛒 orders — Buyurtmalar

| Ustun | Tur | Tavsif |
|-------|-----|--------|
| `id` | INTEGER | Tartib raqam (avtomatik) |
| `user_id` | INTEGER | → users.id ga bog'langan |
| `product_id` | INTEGER | → products.id ga bog'langan |
| `quantity` | INTEGER | Soni (default: 1) |
| `status` | TEXT | Holati (default: "new") |
| `created_at` | TEXT | Buyurtma vaqti (avtomatik) |

---

## 👤 Foydalanuvchilar — Users

### Qo'shish

```python
from utils.db_api import db

await db.add_user(
    telegram_id=123456789,
    full_name="Ali Valiyev",
    username="alivaliyev"    # ixtiyoriy, None bo'lishi mumkin
)
# Qaytaradi: True (muvaffaqiyatli) yoki False (allaqachon bor)
# Agar telegram_id allaqachon bazada bo'lsa — xato bermaydi, shunchaki o'tkazib yuboradi
```

### Tekshirish

```python
bor = await db.user_exists(telegram_id=123456789)
# True — bor, False — yo'q
```

### Bitta foydalanuvchini olish

```python
user = await db.get_user(telegram_id=123456789)
# Qaytaradi: {"id": 1, "telegram_id": 123456789, "full_name": "Ali Valiyev", ...}
# Topilmasa: None

if user:
    print(user["full_name"])     # "Ali Valiyev"
    print(user["telegram_id"])   # 123456789
    print(user["username"])      # "alivaliyev"
    print(user["phone"])         # None (hali kiritilmagan)
    print(user["created_at"])    # "2026-02-20 15:30:00"
```

### Barcha foydalanuvchilarni olish

```python
users = await db.get_all_users()
# [{"telegram_id": 123, ...}, {"telegram_id": 456, ...}, ...]

for user in users:
    print(f"{user['full_name']} — {user['telegram_id']}")
```

### Sonini hisoblash

```python
total = await db.count_users()
# 150
```

### Telefon raqamni yangilash

```python
await db.update_user_phone(telegram_id=123456789, phone="+998901234567")
```

### Ismni yangilash

```python
await db.update_user_fullname(telegram_id=123456789, full_name="Ali Karimov")
```

### O'chirish

```python
await db.delete_user(telegram_id=123456789)
```

---

## 📦 Mahsulotlar — Products

### Qo'shish

```python
product_id = await db.add_product(
    name="iPhone 16",
    price=15000000,
    description="Yangi iPhone 16 128GB",  # ixtiyoriy
    category="Elektronika"                 # ixtiyoriy
)
# Qaytaradi: yangi mahsulot ID si (masalan: 1)
```

### Olish

```python
# Bitta mahsulot
product = await db.get_product(product_id=1)
# {"id": 1, "name": "iPhone 16", "price": 15000000, ...}

# Hammasi
products = await db.get_all_products()

# Kategoriya bo'yicha
electronics = await db.get_products_by_category(category="Elektronika")

# Qidirish (nomi bo'yicha)
results = await db.search_products(query="iPhone")
# Nomi ichida "iPhone" bo'lgan hamma mahsulotlar
```

### Yangilash va o'chirish

```python
await db.update_product_price(product_id=1, new_price=14500000)
await db.delete_product(product_id=1)
```

---

## 🛒 Buyurtmalar — Orders

### Yangi buyurtma

```python
# ⚠️ user_id — bu users jadvalidagi id, telegram_id EMAS!
user = await db.get_user(telegram_id=123456789)

order_id = await db.add_order(
    user_id=user["id"],    # users jadvalidagi id
    product_id=1,           # mahsulot id si
    quantity=2              # nechta dona (default: 1)
)
```

### Buyurtmalarni ko'rish

```python
orders = await db.get_user_orders(telegram_id=123456789)
# [
#     {"order_id": 1, "product_name": "iPhone 16", "price": 15000000,
#      "quantity": 2, "status": "new", "ordered_at": "2026-02-20 15:30:00"},
#     ...
# ]

for order in orders:
    total = order["price"] * order["quantity"]
    print(f"{order['product_name']} x{order['quantity']} = {total} so'm")
```

### Holatni yangilash

```python
await db.update_order_status(order_id=1, status="paid")
# Holatlar: "new" → "paid" → "shipped" → "delivered" | "cancelled"
```

---

## 🔧 Umumiy metodlar

Tayyor metodlar yetarli bo'lmasa — ixtiyoriy SQL yozing:

```python
# Bitta natija
user = await db.fetchone(
    "SELECT * FROM users WHERE username = ?", ("alivaliyev",)
)

# Barcha natijalar
users_with_phone = await db.fetchall(
    "SELECT * FROM users WHERE phone IS NOT NULL"
)

# Narxi 1 mln dan past mahsulotlar
cheap = await db.fetchall(
    "SELECT * FROM products WHERE price < ?", (1000000,)
)

# Oxirgi 10 ta foydalanuvchi
latest = await db.fetchall(
    "SELECT * FROM users ORDER BY id DESC LIMIT 10"
)

# Ixtiyoriy SQL bajarish
await db.execute("UPDATE products SET price = price * 1.1")
await db.execute("DELETE FROM users WHERE id > ?", (100,))
```

---

## 💡 Handlerda ishlatish misollari

### /profil — Foydalanuvchi ma'lumotlarini ko'rsatish

```python
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from utils.db_api import db

router = Router()

@router.message(Command("profil"))
async def show_profile(message: Message):
    user = await db.get_user(message.from_user.id)

    if user:
        await message.answer(
            f"👤 <b>Sizning profilingiz</b>\n\n"
            f"📛 Ism: {user['full_name']}\n"
            f"🆔 ID: {user['telegram_id']}\n"
            f"📱 Telefon: {user['phone'] or 'Kiritilmagan'}\n"
            f"📅 Ro'yxatdan: {user['created_at']}"
        )
```

### Telefon raqamni Contact tugma bilan olish

```python
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

@router.message(Command("telefon"))
async def ask_phone(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=keyboard)


@router.message(lambda msg: msg.contact)
async def save_phone(message: Message):
    phone = message.contact.phone_number
    await db.update_user_phone(message.from_user.id, phone)
    await message.answer(f"✅ Telefon saqlandi: {phone}")
```

### /stat — Admin uchun statistika

```python
from data.config import ADMINS

@router.message(Command("stat"))
async def show_stats(message: Message):
    if str(message.from_user.id) not in ADMINS:
        return

    total = await db.count_users()
    users = await db.get_all_users()

    last_5 = users[:5]
    users_text = ""
    for u in last_5:
        users_text += f"• {u['full_name']} (@{u['username'] or '—'})\n"

    await message.answer(
        f"📊 <b>Statistika</b>\n\n"
        f"👥 Jami: {total}\n\n"
        f"🆕 Oxirgi 5 ta:\n{users_text}"
    )
```

### /reklama — Barcha foydalanuvchilarga xabar

```python
@router.message(Command("reklama"))
async def broadcast(message: Message):
    if str(message.from_user.id) not in ADMINS:
        return

    text = message.text.replace("/reklama ", "", 1)
    if text == "/reklama":
        await message.answer("Foydalanish: /reklama [matn]")
        return

    users = await db.get_all_users()
    success = 0
    fail = 0

    for user in users:
        try:
            await message.bot.send_message(chat_id=user["telegram_id"], text=text)
            success += 1
        except Exception:
            fail += 1

    await message.answer(f"✅ Yuborildi: {success}\n❌ Xato: {fail}")
```

### Mahsulot qo'shish va ro'yxat

```python
@router.message(Command("mahsulot_qosh"))
async def add_product_cmd(message: Message):
    if str(message.from_user.id) not in ADMINS:
        return

    await db.add_product("iPhone 16", 15000000, "128GB", "Elektronika")
    await db.add_product("Samsung S24", 12000000, "256GB", "Elektronika")
    await db.add_product("AirPods Pro", 3500000, "2-avlod", "Aksessuar")
    await message.answer("✅ Mahsulotlar qo'shildi!")


@router.message(Command("mahsulotlar"))
async def show_products(message: Message):
    products = await db.get_all_products()
    if not products:
        await message.answer("Mahsulotlar yo'q")
        return

    text = "📦 <b>Mahsulotlar:</b>\n\n"
    for p in products:
        text += f"#{p['id']} {p['name']} — {p['price']:,.0f} so'm\n"
    await message.answer(text)
```

### Buyurtma berish va ko'rish

```python
@router.message(Command("buyurtma"))
async def make_order(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        await message.answer("Avval /start bosing")
        return

    args = message.text.split()
    if len(args) < 2:
        await message.answer("Foydalanish: /buyurtma [mahsulot_id]")
        return

    product_id = int(args[1])
    product = await db.get_product(product_id)
    if not product:
        await message.answer("Mahsulot topilmadi")
        return

    order_id = await db.add_order(user["id"], product_id)
    await message.answer(
        f"✅ Buyurtma #{order_id}\n"
        f"📦 {product['name']} — {product['price']:,.0f} so'm"
    )


@router.message(Command("buyurtmalarim"))
async def my_orders(message: Message):
    orders = await db.get_user_orders(message.from_user.id)
    if not orders:
        await message.answer("Buyurtmalar yo'q")
        return

    text = "🛒 <b>Buyurtmalaringiz:</b>\n\n"
    for o in orders:
        total = o["price"] * o["quantity"]
        text += (
            f"#{o['order_id']} {o['product_name']} "
            f"x{o['quantity']} = {total:,.0f} so'm "
            f"[{o['status']}]\n"
        )
    await message.answer(text)
```

---

## ❌ Ko'p uchraydigan xatolar

### 1. `ModuleNotFoundError: No module named 'aiosqlite'`

```bash
pip install aiosqlite
```

### 2. `AttributeError: 'NoneType' object has no attribute 'execute'`

**Sabab:** `app.py` da `await db.create()` chaqirilmagan.

### 3. `sqlite3.OperationalError: no such table: users`

**Sabab:** `await db.create_tables()` chaqirilmagan.

### 4. Bitta elementli tuple xatosi

```python
# ❌ NOTO'G'RI — bu tuple emas, oddiy qavs
("SELECT * FROM users WHERE id = ?", (1))

# ✅ TO'G'RI — vergul kerak!
("SELECT * FROM users WHERE id = ?", (1,))
```

### 5. `errors_handler() missing 1 required positional argument`

**Sabab:** Eski `error_handler.py` da `(update, exception)` yozilgan.
**Yechim:** Yangi `error_handler.py` ni qo'ying (`ErrorEvent` bilan).

---

## 📌 Barcha metodlar jadvali

| Metod | Vazifasi | Qaytaradi |
|-------|---------|-----------|
| **Baza** | | |
| `db.create()` | Bazaga ulanish | — |
| `db.close()` | Bazani yopish | — |
| `db.create_tables()` | Jadvallar yaratish | — |
| **Users** | | |
| `db.add_user(telegram_id, full_name, username)` | Qo'shish | `bool` |
| `db.user_exists(telegram_id)` | Bormi? | `bool` |
| `db.get_user(telegram_id)` | Bitta olish | `dict \| None` |
| `db.get_all_users()` | Hammasi | `list[dict]` |
| `db.count_users()` | Soni | `int` |
| `db.update_user_phone(telegram_id, phone)` | Telefon | — |
| `db.update_user_fullname(telegram_id, full_name)` | Ism | — |
| `db.delete_user(telegram_id)` | O'chirish | — |
| **Products** | | |
| `db.add_product(name, price, description, category)` | Qo'shish | `int` (id) |
| `db.get_product(product_id)` | Bitta olish | `dict \| None` |
| `db.get_all_products()` | Hammasi | `list[dict]` |
| `db.get_products_by_category(category)` | Filtrlash | `list[dict]` |
| `db.search_products(query)` | Qidirish | `list[dict]` |
| `db.update_product_price(product_id, new_price)` | Narx | — |
| `db.delete_product(product_id)` | O'chirish | — |
| **Orders** | | |
| `db.add_order(user_id, product_id, quantity)` | Yaratish | `int` (id) |
| `db.get_user_orders(telegram_id)` | Ko'rish | `list[dict]` |
| `db.update_order_status(order_id, status)` | Holat | — |
| **Umumiy** | | |
| `db.execute(sql, params)` | SQL bajarish | — |
| `db.fetchone(sql, params)` | 1 ta natija | `dict \| None` |
| `db.fetchall(sql, params)` | Hammasi | `list[dict]` |