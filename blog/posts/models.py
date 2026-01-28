from django.db import models
from django.contrib.auth import get_user_model

MAX_LENGTH_OF_TITLE = 50
MAX_LENGTH_OF_SUBTITLE = 100
MAX_LENGTH_OF_CATEGORY_NAME = 15

User = get_user_model()

class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True, verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=MAX_LENGTH_OF_CATEGORY_NAME, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Post(BaseModel):
    title = models.CharField(max_length=MAX_LENGTH_OF_TITLE, verbose_name='Заголовок')
    subtitle = models.CharField(max_length=MAX_LENGTH_OF_SUBTITLE, verbose_name='Подзаголовок')
    text = models.TextField(verbose_name='Текст статьи')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор')
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
    )
    category = models.ManyToManyField(
        Category,
        verbose_name='Категория',
        related_name='posts',
    )
    image = models.ImageField(verbose_name='Фото', upload_to='posts_images', blank=True)

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'Посты'
        default_related_name = 'posts_list'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:30] + '...' if len(self.title) > 30 else self.title


class Subscribers(models.Model):
    email = models.EmailField(verbose_name='Адрес электронной почты')
    is_active = models.BooleanField()
    subscribed_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'Подписчики'
        ordering = ('-is_active',)
        default_related_name = 'subscribers_list'
    def __str__(self):
        return self.email[:30] + '...' if len(self.email) > 30 else self.email
