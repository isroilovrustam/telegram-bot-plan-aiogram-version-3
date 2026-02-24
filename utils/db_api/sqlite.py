"""
══════════════════════════════════════════════════════════════
📦 SQLITE BAZA BILAN ISHLASH — TO'LIQ TUSHUNTIRISH
══════════════════════════════════════════════════════════════

SQLite nima?
─────────────
SQLite — bu FAYLGA asoslangan ma'lumotlar bazasi.
PostgreSQL yoki MySQL dan farqi — alohida server kerak emas.
Bitta fayl (masalan: main.db) ichida hamma ma'lumot saqlanadi.

Kichik va o'rta botlar uchun juda qulay!

aiosqlite nima?
────────────────
SQLite oddiy holatda SINXRON ishlaydi (ya'ni kutib turadi).
Lekin aiogram ASINXRON. Shuning uchun aiosqlite kerak —
u SQLite ni asinxron qilib beradi (await bilan ishlatamiz).

O'rnatish:
    pip install aiosqlite
"""

# ┌──────────────────────────────────────────────────────────┐
# │  📥 IMPORTLAR                                            │
# └──────────────────────────────────────────────────────────┘

import aiosqlite  # SQLite ni asinxron ishlatish uchun kutubxona
import logging    # Xatoliklarni konsolga chiqarish uchun


# ┌──────────────────────────────────────────────────────────┐
# │  🗄️ DATABASE KLASS                                      │
# └──────────────────────────────────────────────────────────┘

class Database:
    """
    SQLite baza bilan ishlash uchun klass.

    Ishlatish tartibi:
        1. db = Database("main.db")   ← Obyekt yaratish
        2. await db.create()           ← Bazaga ulanish
        3. await db.create_tables()    ← Jadvallar yaratish
        4. await db.add_user(...)      ← Ma'lumot qo'shish
        5. await db.close()            ← Bazani yopish (bot to'xtaganda)
    """

    def __init__(self, path: str):
        """
        Konstruktor — Database obyekti yaratilganda chaqiriladi.

        path: baza fayli nomi (masalan: "main.db")
              Bu fayl avtomatik yaratiladi agar mavjud bo'lmasa.

        self.path — fayl yo'lini saqlaymiz
        self.db   — hozircha None, create() da ulanadi
        """
        self.path = path  # Baza fayli yo'li (masalan: "main.db")
        self.db = None     # Baza ulanishi (hozircha bo'sh)

    # ══════════════════════════════════════════════════════════
    #  🔌 BAZAGA ULANISH VA YOPISH
    # ══════════════════════════════════════════════════════════

    async def create(self):
        """
        Bazaga ulanish.
        Bot ishga tushganda BIR MARTA chaqiriladi.

        aiosqlite.connect() — fayl bilan ulanish ochadi.
        Agar fayl mavjud bo'lmasa — yangi fayl yaratadi.
        """
        self.db = await aiosqlite.connect(self.path)

        # row_factory — natijalarni dict (lug'at) ko'rinishda olish uchun
        # Bu bilan result["ism"] deb yozish mumkin bo'ladi
        # Agar bu qator bo'lmasa result[0], result[1] deb yozish kerak
        self.db.row_factory = aiosqlite.Row

        logging.info(f"✅ SQLite bazaga ulandi: {self.path}")

    async def close(self):
        """
        Bazani yopish.
        Bot to'xtaganda chaqiriladi.
        Yopmasangiz ma'lumot yo'qolishi mumkin!
        """
        if self.db:
            await self.db.close()
            logging.info("🔒 SQLite baza yopildi")

    # ══════════════════════════════════════════════════════════
    #  📐 JADVALLAR YARATISH (CREATE TABLE)
    # ══════════════════════════════════════════════════════════

    async def create_tables(self):
        """
        Barcha jadvallarni yaratish.
        Bot ishga tushganda BIR MARTA chaqiriladi.

        IF NOT EXISTS — agar jadval allaqachon bor bo'lsa
        qayta yaratmaydi (xato bermaydi).

        SQL da ma'lumot turlari:
        ─────────────────────────
        INTEGER  — butun son (1, 2, 3, ...)
        TEXT     — matn ("Salom", "Ali", ...)
        REAL     — kasr son (3.14, 99.99, ...)

        PRIMARY KEY — asosiy kalit (har bir qator uchun UNIKAL)
        NOT NULL    — bo'sh bo'lishi MUMKIN EMAS
        DEFAULT     — agar qiymat berilmasa, shu qiymat qo'yiladi
        UNIQUE      — takrorlanmas (faqat bitta bo'lishi kerak)
        AUTOINCREMENT — avtomatik 1, 2, 3, ... bo'lib oshadi
        """

        # ─── 1. FOYDALANUVCHILAR jadvali ───
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id  INTEGER NOT NULL UNIQUE,
                full_name    TEXT    NOT NULL,
                username     TEXT,
                phone        TEXT,
                created_at   TEXT    DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # id           — jadval ichidagi tartib raqam (avtomatik oshadi: 1, 2, 3, ...)
        # telegram_id  — Telegram bergan ID raqam (masalan: 123456789)
        #                UNIQUE = bitta odam faqat BIR MARTA yoziladi
        # full_name    — Telegramdagi to'liq ismi
        # username     — @username (bo'lmasligi mumkin, shuning uchun NOT NULL yo'q)
        # phone        — telefon raqami (keyinroq so'raymiz)
        # created_at   — qachon ro'yxatdan o'tgani (avtomatik yoziladi)

        # ─── 2. MAHSULOTLAR jadvali (namuna) ───
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                description TEXT,
                price       REAL    NOT NULL DEFAULT 0,
                category    TEXT,
                created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # name        — mahsulot nomi
        # description — tavsifi
        # price       — narxi (REAL = kasr son, masalan 49999.99)
        # category    — kategoriya ("Elektronika", "Oziq-ovqat", ...)

        # ─── 3. BUYURTMALAR jadvali (namuna) ───
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                product_id  INTEGER NOT NULL,
                quantity    INTEGER NOT NULL DEFAULT 1,
                status      TEXT    NOT NULL DEFAULT 'new',
                created_at  TEXT    DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id)    REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        # user_id    — qaysi foydalanuvchi (users jadvaliga bog'langan)
        # product_id — qaysi mahsulot (products jadvaliga bog'langan)
        # quantity   — nechta dona
        # status     — holati: "new", "paid", "delivered"
        # FOREIGN KEY — boshqa jadvalga bog'lanish (aloqa)

        # O'zgarishlarni saqlash (MUHIM! Busiz ma'lumot saqlanmaydi)
        await self.db.commit()

        logging.info("📐 Jadvallar yaratildi")

    # ══════════════════════════════════════════════════════════
    #  👤 FOYDALANUVCHILAR (USERS) — CRUD
    # ══════════════════════════════════════════════════════════

    # ─── C: CREATE (QO'SHISH) ───

    async def add_user(self, telegram_id: int, full_name: str, username: str = None) -> bool:
        """
        Yangi foydalanuvchini bazaga qo'shish.

        INSERT OR IGNORE — agar telegram_id allaqachon bazada bo'lsa,
        xato bermaydi, shunchaki e'tiborsiz qoldiradi.

        ? belgilari — parametrlar o'rnida turadi (SQL injection dan himoya)
        Hech qachon f-string bilan SQL yozmang!
            ❌ f"INSERT INTO users VALUES ({telegram_id})"
            ✅ "INSERT INTO users VALUES (?)", (telegram_id,)
        """
        try:
            await self.db.execute(
                """INSERT OR IGNORE INTO users (telegram_id, full_name, username) 
                   VALUES (?, ?, ?)""",
                (telegram_id, full_name, username)
                # TARTIB muhim: 1-? → telegram_id, 2-? → full_name, 3-? → username
            )
            await self.db.commit()  # Saqlash
            return True
        except Exception as e:
            logging.error(f"❌ Foydalanuvchi qo'shishda xato: {e}")
            return False

    # ─── R: READ (O'QISH) ───

    async def user_exists(self, telegram_id: int) -> bool:
        """
        Foydalanuvchi bazada bormi?

        SELECT 1 — faqat borligini tekshiradi (tez ishlaydi)
        fetchone() — bitta natija olish (bor → Row, yo'q → None)
        """
        cursor = await self.db.execute(
            "SELECT 1 FROM users WHERE telegram_id = ?",
            (telegram_id,)  # ⚠️ Bitta element bo'lsa ham tuple kerak: (qiymat,)
        )
        result = await cursor.fetchone()
        return result is not None  # None emas = bor = True

    async def get_user(self, telegram_id: int) -> dict | None:
        """
        Bitta foydalanuvchini olish.

        * — barcha ustunlarni olish
        Qaytaradi: {"id": 1, "telegram_id": 123, "full_name": "Ali", ...}
        Topilmasa: None
        """
        cursor = await self.db.execute(
            "SELECT * FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None  # Row → dict ga aylantirish

    async def get_all_users(self) -> list[dict]:
        """
        Barcha foydalanuvchilarni olish.

        ORDER BY id DESC — eng oxirgi qo'shilganlar birinchi
        fetchall() — BARCHA natijalarni ro'yxat sifatida olish
        """
        cursor = await self.db.execute(
            "SELECT * FROM users ORDER BY id DESC"
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]  # Har bir Row → dict

    async def count_users(self) -> int:
        """
        Jami foydalanuvchilar soni.

        COUNT(*) — qatorlar sonini hisoblaydi
        result[0] — birinchi ustun (COUNT natijasi)
        """
        cursor = await self.db.execute("SELECT COUNT(*) FROM users")
        result = await cursor.fetchone()
        return result[0]

    # ─── U: UPDATE (YANGILASH) ───

    async def update_user_phone(self, telegram_id: int, phone: str):
        """
        Telefon raqamini yangilash.

        UPDATE — mavjud qatorni o'zgartirish
        SET    — qaysi ustunni o'zgartirish
        WHERE  — qaysi qatorni (shart)

        ⚠️ WHERE siz UPDATE yozsangiz BARCHA qatorlar o'zgaradi!
        """
        await self.db.execute(
            "UPDATE users SET phone = ? WHERE telegram_id = ?",
            (phone, telegram_id)
        )
        await self.db.commit()

    async def update_user_fullname(self, telegram_id: int, full_name: str):
        """Ismini yangilash."""
        await self.db.execute(
            "UPDATE users SET full_name = ? WHERE telegram_id = ?",
            (full_name, telegram_id)
        )
        await self.db.commit()

    # ─── D: DELETE (O'CHIRISH) ───

    async def delete_user(self, telegram_id: int):
        """
        Foydalanuvchini o'chirish.

        ⚠️ WHERE siz DELETE yozsangiz BARCHA ma'lumot o'chadi!
        """
        await self.db.execute(
            "DELETE FROM users WHERE telegram_id = ?",
            (telegram_id,)
        )
        await self.db.commit()

    # ══════════════════════════════════════════════════════════
    #  📦 MAHSULOTLAR (PRODUCTS)
    # ══════════════════════════════════════════════════════════

    async def add_product(self, name: str, price: float,
                          description: str = None, category: str = None) -> int:
        """
        Mahsulot qo'shish.
        cursor.lastrowid — oxirgi qo'shilgan qatorning ID si
        """
        cursor = await self.db.execute(
            """INSERT INTO products (name, price, description, category)
               VALUES (?, ?, ?, ?)""",
            (name, price, description, category)
        )
        await self.db.commit()
        return cursor.lastrowid

    async def get_product(self, product_id: int) -> dict | None:
        """ID bo'yicha bitta mahsulot olish."""
        cursor = await self.db.execute(
            "SELECT * FROM products WHERE id = ?", (product_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def get_all_products(self) -> list[dict]:
        """Barcha mahsulotlar."""
        cursor = await self.db.execute("SELECT * FROM products ORDER BY id DESC")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def get_products_by_category(self, category: str) -> list[dict]:
        """Kategoriya bo'yicha filtrlash."""
        cursor = await self.db.execute(
            "SELECT * FROM products WHERE category = ? ORDER BY price",
            (category,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def search_products(self, query: str) -> list[dict]:
        """
        Nomi bo'yicha qidirish.

        LIKE — qisman mos kelishni tekshiradi
        %query% — ichida query bo'lgan hamma natijalar
        Masalan: "%telefon%" → "Yangi telefon", "Telefon g'ilofi"
        """
        cursor = await self.db.execute(
            "SELECT * FROM products WHERE name LIKE ?",
            (f"%{query}%",)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def update_product_price(self, product_id: int, new_price: float):
        """Narxini yangilash."""
        await self.db.execute(
            "UPDATE products SET price = ? WHERE id = ?",
            (new_price, product_id)
        )
        await self.db.commit()

    async def delete_product(self, product_id: int):
        """Mahsulotni o'chirish."""
        await self.db.execute("DELETE FROM products WHERE id = ?", (product_id,))
        await self.db.commit()

    # ══════════════════════════════════════════════════════════
    #  🛒 BUYURTMALAR (ORDERS)
    # ══════════════════════════════════════════════════════════

    async def add_order(self, user_id: int, product_id: int, quantity: int = 1) -> int:
        """Buyurtma yaratish. user_id — users jadvalidagi id (telegram_id EMAS!)"""
        cursor = await self.db.execute(
            "INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)",
            (user_id, product_id, quantity)
        )
        await self.db.commit()
        return cursor.lastrowid

    async def get_user_orders(self, telegram_id: int) -> list[dict]:
        """
        Foydalanuvchining buyurtmalari.

        JOIN — ikki yoki undan ko'p jadvalni birlashtirish
        Bu yerda orders + users + products birlashtiriladi
        """
        cursor = await self.db.execute("""
            SELECT 
                orders.id       AS order_id,
                products.name   AS product_name,
                products.price  AS price,
                orders.quantity AS quantity,
                orders.status   AS status,
                orders.created_at AS ordered_at
            FROM orders
            JOIN users    ON orders.user_id    = users.id
            JOIN products ON orders.product_id = products.id
            WHERE users.telegram_id = ?
            ORDER BY orders.id DESC
        """, (telegram_id,))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def update_order_status(self, order_id: int, status: str):
        """Buyurtma holatini yangilash: 'new', 'paid', 'shipped', 'delivered', 'cancelled'"""
        await self.db.execute(
            "UPDATE orders SET status = ? WHERE id = ?", (status, order_id)
        )
        await self.db.commit()

    # ══════════════════════════════════════════════════════════
    #  🔧 UMUMIY METODLAR — IXTIYORIY SQL YOZISH UCHUN
    # ══════════════════════════════════════════════════════════

    async def execute(self, sql: str, params: tuple = None):
        """Ixtiyoriy SQL bajarish. Masalan: await db.execute("DELETE FROM users WHERE id > ?", (100,))"""
        if params:
            await self.db.execute(sql, params)
        else:
            await self.db.execute(sql)
        await self.db.commit()

    async def fetchone(self, sql: str, params: tuple = None) -> dict | None:
        """Bitta natija olish. Masalan: await db.fetchone("SELECT * FROM users WHERE id = ?", (1,))"""
        cursor = await self.db.execute(sql, params) if params else await self.db.execute(sql)
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def fetchall(self, sql: str, params: tuple = None) -> list[dict]:
        """Barcha natijalar. Masalan: await db.fetchall("SELECT * FROM users WHERE phone IS NOT NULL")"""
        cursor = await self.db.execute(sql, params) if params else await self.db.execute(sql)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]