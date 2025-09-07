from django import forms

from .models import Birthday


class BirthdayForm(forms.ModelForm):

    # Все настройки задаём в подклассе Meta.
    class Meta:
        model = Birthday    # Указываем модель, на основе которой должна строиться форма.
        fields = '__all__'  # Указываем, что надо отобразить все поля.

        # для поля с датой рождения используется виджет с типом данных date.
        widgets = {
            'birthday': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})    # Виджеты полей описываются в подклассе Meta:
        }

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
#         widget=forms.DateInput(attrs={'type': 'date'})
#     )

# Можно поправить формат и без изменения локализации USE_L10N: для этого нужно
# переопределить формат даты на уровне виджета, используя параметр input_formats=['%Y-%m-%d']. тут работало только так format='%Y-%m-%d'
