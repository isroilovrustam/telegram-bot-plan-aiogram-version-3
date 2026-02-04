import logging
import sys


def setup_logging(level: int = logging.INFO):
    """
    Logging sozlamalarini o'rnatish
    
    :param level: Logging darajasi
    """
    logging.basicConfig(
        level=level,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Boshqa kutubxonalar uchun logging darajasini kamaytirish
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
