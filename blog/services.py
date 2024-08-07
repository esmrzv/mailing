from django.core.cache import cache

from blog.models import Blog
from config.settings import CACHE_ENABLED


def get_blogs_from_cache():
    """
        Возвращает список блогов из кэша или из базы,
        если кэш не включен.
        """
    if not CACHE_ENABLED:  # если кэш не включен
        return Blog.objects.all()  # возвращаем список продуктов
    key = 'blog_list'  # ключ
    blog = cache.get(key)  # получаем кэш по ключу
    if blog is not None:  # если кэш не пустой
        return blog  # возвращаем кэш
    blog = Blog.objects.all()  # получаем список продуктов из базы
    cache.set(key, blog)  # кладем список продуктов в кэш
    return blog
