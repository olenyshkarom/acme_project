from django import forms


class BirthdayForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=20)
    last_name = forms.CharField(
        label='Фамилия', required=False, help_text='Необязательное поле') # required=True указывать не требуется
    birthday = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

# IntegerField для целочисленных полей,
# CharField для текстовых полей,
# DateField для полей с датой.

# В аргументе attrs задан атрибут type="date" для тега <input>. Если HTML-форму верстают вручную, этот атрибут описывают прямо в теге: <input type="date">.
