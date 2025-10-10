from django import forms

from .models import Birthday, Congratulation

# Импортируем функцию-валидатор.
# from .validators import real_age

from django.core.exceptions import ValidationError

# Импорт функции для отправки почты.
from django.core.mail import send_mail

# Множество с именами участников Ливерпульской четвёрки.
BEATLES = {'Джон Леннон', 'Пол Маккартни', 'Джордж Харрисон', 'Ринго Старр'}


class BirthdayForm(forms.ModelForm):

    # Все настройки задаём в подклассе Meta.
    class Meta:
        model = Birthday    # Указываем модель, на основе которой должна строиться форма.
        # fields = '__all__'  # Указываем, что надо отобразить все поля.
        exclude = ('author',)

        # для поля с датой рождения используется виджет с типом данных date.
        widgets = {
            'birthday': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})    # Виджеты полей описываются в подклассе Meta:
        }

    def clean_first_name(self):     # Метод clean для полей
        # Получаем значение имени из словаря очищенных данных.
        first_name = self.cleaned_data['first_name']
        # Разбиваем полученную строку по пробелам
        # и возвращаем только первое имя.
        return first_name.split()[0]

    def clean(self):        # Метод clean() для формы
        # Вызов родительского метода clean.
        super().clean()     # чтобы сработал clean constraints в модели
        # Получаем имя и фамилию из очищенных полей формы.
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        # Проверяем вхождение сочетания имени и фамилии во множество имён.
        if f'{first_name} {last_name}' in BEATLES:
            # Отправляем письмо, если кто-то представляется 
            # именем одного из участников Beatles.
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                'Мы тоже любим Битлз, но введите, пожалуйста, настоящее имя!'
            )


class CongratulationForm(forms.ModelForm):

    class Meta:
        model = Congratulation
        fields = ('text',)

# IntegerField для целочисленных полей,
# CharField для текстовых полей,
# DateField для полей с датой.

# В аргументе attrs задан атрибут type="date" для тега <input>. Если HTML-форму верстают вручную, этот атрибут описывают прямо в теге: <input type="date">.
# python manage.py makemigrations
# python manage.py migrate

# class BirthdayForm(forms.Form):
#     first_name = forms.CharField(label='Имя', max_length=20)
#     last_name = forms.CharField(
#         label='Фамилия', required=False, help_text='Необязательное поле') # required=True указывать не требуется
#     birthday = forms.DateField(
#         label='Дата рождения',
# #         widget=forms.DateInput(attrs={'type': 'date'})
#         # В аргументе validators указываем список или кортеж 
#         # валидаторов этого поля (валидаторов может быть несколько). Если форма не на основе модели.
#         validators=(real_age,),
#     )

# Можно поправить формат и без изменения локализации USE_L10N: для этого нужно
# переопределить формат даты на уровне виджета, используя параметр input_formats=['%Y-%m-%d']. тут работало только так format='%Y-%m-%d'

# В каком порядке выполняются валидаторы в формах Django? Ответ введите в строку в формате ABCD.
# A Значение каждого поля проверяется на возможность приведения к нужному типу данных.
# B «Очистка» всей формы с помощью метода clean.
# C Для каждого поля формы выполняются функции-валидаторы.
# D «Очистка» каждого отдельного поля с помощью методов clean_имя-поля.


# ACDB


# Если класс формы унаследован от другого пользовательского класса то в методе clean() первым делом нужно вызвать метод super().clean() родительского класса
