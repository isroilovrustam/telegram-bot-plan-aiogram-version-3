from typing import Callable, Any


def rate_limit(limit: float, key: str = None) -> Callable:
    """
    Handler uchun rate limit o'rnatish dekoratori
    
    :param limit: So'rovlar orasidagi minimal vaqt (soniyalarda)
    :param key: Throttling uchun kalit
    :return: Decorator
    """
    def decorator(func: Callable) -> Callable:
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func
    return decorator
