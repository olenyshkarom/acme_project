from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm

# Импортируем модель дней рождения.
from .models import Birthday

# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()      # Получаем текущий объект.
        # Метод вернёт True или False. 
        # Если пользователь - автор объекта, то тест будет пройден.
        # Если нет, то будет вызвана ошибка 403.
        return object.author == self.request.user


class BirthdayListView(ListView):   # словарь context внутри объект страницы page_obj
    model = Birthday    # Указываем модель, с которой работает CBV...
    ordering = 'id'     # ...сортировку, которая будет применена при выводе списка объектов
    paginate_by = 10    # ...и даже настройки пагинации
    # и перенастроим маршрутизацию: в файле birthday/urls.py
# можно задать собственное название шаблона в атрибуте template_name, а содержимое словаря контекста можно описать явным образом с помощью метода get_context_data().


# class BirthdayMixin:    # Миксины - вспомогательные классы, с помощью которых в наследуемый класс можно добавить необходимые атрибуты и методы
#     model = Birthday
#     success_url = reverse_lazy('birthday:list')

# LoginRequiredMixin добавляет в CBV проверку — аутентифицирован ли пользователь, сделавший запрос.
class BirthdayCreateView(LoginRequiredMixin, CreateView):   # BirthdayMixin, 
    # Не нужно описывать все атрибуты: все они унаследованы от BirthdayMixin.
    model = Birthday
    form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'  # переименовали шаблон birthday.html по правилу в birthday_form.html

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'
    # Не нужно описывать все атрибуты: все они унаследованы от BirthdayMixin.
    # template_name = 'birthday/birthday.html'


class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
    model = Birthday
    # model = Birthday
    # template_name = 'birthday/birthday.html' # есть шаблон с тем именем, которое ожидает класс DeleteView,
    success_url = reverse_lazy('birthday:list')
    # в шаблоне Удаляемый объект доступен и в переменной object, и в переменной с названием модели — birthday


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Получаем словарь контекста:
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday    # Дату рождения берём из объекта в словаре context:
        )
        return context  # Возвращаем словарь контекста.


@login_required
def simple_view(request):   # для CBV не получится, декоратор всегда возвращает функцию
    return HttpResponse('Страница для залогиненных пользователей!')

# можно так
# from django.contrib.auth.mixins import LoginRequiredMixin

# # Наследуем BirthdayCreateView от CreateView и от миксина LoginRequiredMixin:
# class BirthdayCreateView(LoginRequiredMixin, CreateView):
#     model = Birthday
#     form_class = BirthdayForm 
