from django.db import models
from django.contrib.auth import get_user_model

# Импортируется функция-валидатор.
from .validators import real_age

# Импортируем функцию reverse() для получения ссылки на объект.
from django.urls import reverse

# Да, именно так всегда и ссылаемся на модель пользователя!
User = get_user_model()


class Tag(models.Model):
    tag = models.CharField('Тег', max_length=20)

    # Переопределяем метод:
    def __str__(self):
        return self.tag


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
    )
    # Валидатор указывается в описании поля модели, если форма на основе модели.
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)
    author = models.ForeignKey(
        User, verbose_name='Автор записи', on_delete=models.CASCADE, null=True
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True,
        help_text='Удерживайте Ctrl для выбора нескольких вариантов'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )

    def get_absolute_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.pk})

# blank=True - допустимы пустые значения
# для полей модели с классом models.CharField обязательно должна быть указана максимальная длина поля; в нашем случае — max_length=20
# кастомное название поля формы указывается в параметре label, а в модели это название указывают первым позиционным аргументом или в параметре verbose_name.


class Congratulation(models.Model):
    text = models.TextField('Текст поздравления')
    birthday = models.ForeignKey(
        Birthday,
        on_delete=models.CASCADE,
        related_name='congratulations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)


# from django.db import models

# from django.core.validators import MinValueValidator, MaxValueValidator


# # Опишите модель Contest здесь!
# class Contest(models.Model):
#     title = models.CharField('Название', max_length=20)
#     description = models.TextField('Описание')
#     price = models.IntegerField(
#         'Цена',
#         validators=[MinValueValidator(10), MaxValueValidator(100)],
#         help_text='Рекомендованная розничная цена'
#     )
#     comment = models.TextField('Комментарий', blank=True)

# from django import forms

# from .models import Contest


# class ContestForm(forms.ModelForm):

#     class Meta:
#         model = Contest
#         fields = '__all__'
#         widgets= {
#             'comment': forms.Textarea({'cols': '22', 'rows': '5'}),
#             'description': forms.Textarea({'cols': '22', 'rows': '5'})
#         }

