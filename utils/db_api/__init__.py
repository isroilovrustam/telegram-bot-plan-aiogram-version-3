# ┌──────────────────────────────────────────────────────────┐
# │  Database ni shu yerdan import qilamiz                   │
# │  Boshqa fayllarda: from utils.db_api import db           │
# └──────────────────────────────────────────────────────────┘

from .sqlite import Database

# Database obyektini yaratish
# "main.db" — baza fayli nomi (loyiha papkasida yaratiladi)
# Bu obyekt BUTUN botda bitta bo'ladi
db = Database(path="main.db")