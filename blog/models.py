from django.db import models


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to="preview/photo", blank=True, null=True, verbose_name="Превью")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return f'{self.title} - {self.content}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
