from environs import Env
# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
ADMINS = env.list("ADMINS")  # adminlar ro'yxati

# Majburiy obuna kanallar ro'yxati
# Misol: ["@kanal_username", -1001234567890]
def parse_channels(channels_list):
    """Kanallarni to'g'ri formatga o'tkazish"""
    result = []
    for channel in channels_list:
        channel = channel.strip()
        if channel.startswith("-100") or channel.lstrip("-").isdigit():
            # Bu ID (masalan: -1001234567890)
            result.append(int(channel))
        else:
            # Bu username (masalan: @channel_name)
            result.append(channel)
    return result
CHANNELS = env.list("CHANNELS", default=[])
