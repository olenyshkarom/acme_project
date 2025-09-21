# from django.shortcuts import get_object_or_404, redirect, render

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm

# Импортируем модель дней рождения.
from .models import Birthday

# Импортируем из utils.py функцию для подсчёта дней.
# from .utils import calculate_birthday_countdown

# Импортируем класс пагинатора.
# from django.core.paginator import Paginator

from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy


class BirthdayMixin:    # Миксины - вспомогательные классы, с помощью которых в наследуемый класс можно добавить необходимые атрибуты и методы
    model = Birthday
    # form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list')


class BirthdayFormMixin:
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'


class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin, CreateView):
    # Не нужно описывать все атрибуты: все они унаследованы от BirthdayMixin.
    # form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'
    pass
    # # Указываем модель, с которой работает CBV...
    # model = Birthday
    # # Этот класс сам может создать форму на основе модели!
    # # Нет необходимости отдельно создавать форму через ModelForm.
    # # Указываем поля, которые должны быть в форме:
    # # fields = '__all__'    # подключим форму BirthdayForm ниже в form_class, чтобы сработал валидатор и виджеты
    # # Указываем имя формы:
    # form_class = BirthdayForm
    # # Явным образом указываем шаблон:
    # template_name = 'birthday/birthday.html'
    # # Указываем namespace:name страницы, куда будет перенаправлен пользователь
    # # после создания объекта:
    # success_url = reverse_lazy('birthday:list') # отвечает за переадресацию после успешного создания объекта. 


class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin, UpdateView):
    # form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'
    # Не нужно описывать все атрибуты: все они унаследованы от BirthdayMixin.
    pass
    # model = Birthday
    # form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'
    # success_url = reverse_lazy('birthday:list')


# # Добавим опциональный параметр pk.
# def birthday(request, pk=None):
#     # Если в запросе указан pk (если получен запрос на редактирование объекта):
#     if pk is not None:
#         # Получаем объект модели или выбрасываем 404 ошибку.
#         instance = get_object_or_404(Birthday, pk=pk)
#     # Если в запросе не указан pk
#     # (если получен запрос к странице создания записи):
#     else:
#         # Связывать форму с объектом не нужно, установим значение None.
#         instance = None
#     # Передаём в форму либо данные из запроса, либо None. 
#     # В случае редактирования прикрепляем объект модели.
#     form = BirthdayForm(
#         request.POST or None,
#         # Файлы, переданные в запросе, указываются отдельно.
#         files=request.FILES or None,
#         instance=instance
#     )
#     # Остальной код без изменений.
#     context = {'form': form}
#     # Сохраняем данные, полученные из формы, и отправляем ответ:
#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#         )
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context) 

# def birthday(request):
#     form = BirthdayForm(request.POST or None)    # если же объект request.GET пуст — срабатывает условиe or и форма создаётся без параметров
#     # Создаём словарь контекста сразу после инициализации формы.
#     context = {'form': form}

#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']   # 3 урок обработка данных
#         )
#         # Обновляем словарь контекста: добавляем в него новый элемент.
#         # context = {'form': form}
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context)

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


class BirthdayListView(ListView):   # словарь context внутри объект страницы page_obj
    model = Birthday    # Указываем модель, с которой работает CBV...
    ordering = 'id'     # ...сортировку, которая будет применена при выводе списка объектов
    paginate_by = 10    # ...и даже настройки пагинации
    # и перенастроим маршрутизацию: в файле birthday/urls.py
# можно задать собственное название шаблона в атрибуте template_name, а содержимое словаря контекста можно описать явным образом с помощью метода get_context_data().

# def birthday_list(request):

#     birthdays = Birthday.objects.order_by('id') # Получаем список всех объектов с сортировкой по id.
#     paginator = Paginator(birthdays, 10) # Создаём объект пагинатора с количеством 10 записей на страницу.
#     page_number = request.GET.get('page') # Получаем из запроса значение параметра page.
#     # Получаем запрошенную страницу пагинатора. 
#     # Если параметра page нет в запросе или его значение не приводится к числу,
#     # вернётся первая страница.
#     page_obj = paginator.get_page(page_number)
#     # Вместо полного списка объектов передаём в контекст
#     # объект страницы пагинатора
#     context = {'page_obj': page_obj}
#     return render(request, 'birthday/birthday_list.html', context) 

    # birthdays = Birthday.objects.all() # Получаем все объекты модели Birthday из БД.
    # context = {'birthdays': birthdays} # # Передаём их в контекст шаблона.
    # return render(request, 'birthday/birthday_list.html', context)


# def edit_birthday(request, pk):
#     # Находим запрошенный объект для редактирования по первичному ключу
#     # или возвращаем 404 ошибку, если такого объекта нет.
#     instance = get_object_or_404(Birthday, pk=pk)
#     # Связываем форму с найденным объектом: передаём его в аргумент instance.
#     form = BirthdayForm(request.POST or None, instance=instance)
#     # Всё остальное без изменений.
#     context = {'form': form}
#     # Сохраняем данные, полученные из формы, и отправляем ответ:
#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#         )
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context)

# http://127.0.0.1:8000/birthday/1/edit/


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    # model = Birthday
    # template_name = 'birthday/birthday.html' # есть шаблон с тем именем, которое ожидает класс DeleteView,
    # success_url = reverse_lazy('birthday:list')
    # в шаблоне Удаляемый объект доступен и в переменной object, и в переменной с названием модели — birthday
    pass


# def delete_birthday(request, pk):
#     # Получаем объект модели или выбрасываем 404 ошибку.
#     instance = get_object_or_404(Birthday, pk=pk)
#     # В форму передаём только объект модели;
#     # передавать в форму параметры запроса не нужно.
#     form = BirthdayForm(instance=instance)
#     context = {'form': form}
#     # Если был получен POST-запрос...
#     if request.method == 'POST':
#         # ...удаляем объект:
#         instance.delete()
#         # ...и переадресовываем пользователя на страницу со списком записей.
#         return redirect('birthday:list')
#     # Если был получен GET-запрос — отображаем форму.
#     return render(request, 'birthday/birthday.html', context)
