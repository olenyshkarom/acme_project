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


class BirthdayListView(ListView):   # словарь context внутри объект страницы page_obj
    model = Birthday    # Указываем модель, с которой работает CBV...
    ordering = 'id'     # ...сортировку, которая будет применена при выводе списка объектов
    paginate_by = 10    # ...и даже настройки пагинации
    # и перенастроим маршрутизацию: в файле birthday/urls.py
# можно задать собственное название шаблона в атрибуте template_name, а содержимое словаря контекста можно описать явным образом с помощью метода get_context_data().


# class BirthdayMixin:    # Миксины - вспомогательные классы, с помощью которых в наследуемый класс можно добавить необходимые атрибуты и методы
#     model = Birthday
#     success_url = reverse_lazy('birthday:list')


class BirthdayCreateView(CreateView):   # BirthdayMixin, 
    # Не нужно описывать все атрибуты: все они унаследованы от BirthdayMixin.
    model = Birthday
    form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'  # переименовали шаблон birthday.html по правилу в birthday_form.html


class BirthdayUpdateView(UpdateView):
    model = Birthday
    form_class = BirthdayForm
    # template_name = 'birthday/birthday.html'
    # Не нужно описывать все атрибуты: все они унаследованы от BirthdayMixin.
    # template_name = 'birthday/birthday.html'


class BirthdayDeleteView(DeleteView):
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
