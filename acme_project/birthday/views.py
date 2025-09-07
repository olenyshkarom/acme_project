from django.shortcuts import render

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm

# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


def birthday(request):
    form = BirthdayForm(request.POST or None)    # если же объект request.GET пуст — срабатывает условиe or и форма создаётся без параметров
    # Создаём словарь контекста сразу после инициализации формы.
    context = {'form': form}

    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']   # 3 урок обработка данных
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        # context = {'form': form}
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)

    # print(request.GET)
    # if request.GET:
    #     # Создаём экземпляр класса формы.
    #     # ...передаём параметры запроса в конструктор класса формы.
    #     form = BirthdayForm(request.GET)
    #     # Если данные валидны...
    #     if form.is_valid():
    #         # ...то считаем, сколько дней осталось до дня рождения.
    #         # Пока функции для подсчёта дней нет — поставим pass:
    #         pass
    # # Если нет параметров GET-запроса.
    # else:
    #     # То просто создаём пустую форму.
    #     form = BirthdayForm()
    # # Передаём форму в словарь контекста:
    # # Добавляем его в словарь контекста под ключом form:
    # context = {'form': form}
    # return render(request, 'birthday/birthday.html', context=context)
