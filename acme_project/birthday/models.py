from django.db import models


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
    )
    birthday = models.DateField('Дата рождения')

# blank=True - допустимы пустые значения
# для полей модели с классом models.CharField обязательно должна быть указана максимальная длина поля; в нашем случае — max_length=20
# кастомное название поля формы указывается в параметре label, а в модели это название указывают первым позиционным аргументом или в параметре verbose_name.





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

