from django.core.cache import cache
from django.db.models import F
from blog.models import Blog
from config.settings import CACHE_ENABLED


def get_blogs_from_cache():
    if not CACHE_ENABLED:
        return Blog.objects.all().annotate(views_count=F('views'))
    key = 'blog_list'
    blog = cache.get(key)
    if blog is not None:
        return blog.annotate(views_count=F('views'))  # Добавляем количество просмотров
    blog = Blog.objects.all().annotate(views_count=F('views'))
    cache.set(key, blog)
    return blog


