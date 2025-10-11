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
from django.shortcuts import get_object_or_404, redirect
from .forms import CongratulationForm


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()      # Получаем текущий объект.
        # Метод вернёт True или False. 
        # Если пользователь - автор объекта, то тест будет пройден.
        # Если нет, то будет вызвана ошибка 403.
        return object.author == self.request.user


class BirthdayListView(ListView):   # словарь context внутри объект страницы page_obj
    model = Birthday    # Указываем модель, с которой работает CBV...
    # По умолчанию этот класс 
    # выполняет запрос queryset = Birthday.objects.all(),
    # но мы его переопределим:
    queryset = Birthday.objects.prefetch_related(
        'tags'
        ).select_related('author')  # чтобы «снизить стоимость» получения объектов, связанных «многие-ко-многим»
    # При вызове prefetch_related() в него передаётся имя поля, через которое модель Birthday связана с Tag:
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
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
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


# Будут обработаны POST-запросы только от залогиненных пользователей.
@login_required
def add_comment(request, pk):
    # Получаем объект дня рождения или выбрасываем 404 ошибку.
    birthday = get_object_or_404(Birthday, pk=pk)
    # Функция должна обрабатывать только POST-запросы.
    form = CongratulationForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        congratulation = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        congratulation.author = request.user
        # В поле birthday передаём объект дня рождения.
        congratulation.birthday = birthday
        # Сохраняем объект в БД.
        congratulation.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('birthday:detail', pk=pk) 

# Для получения данных из моделей, связанных «один-ко-многим», можно применять метод select_related(),
# он позволит снизить количество выполняемых запросов к базе. «Под капотом» при этом выполняется SQL-запрос с использованием JOIN.

# Для получения данных из моделей, связанных «многие-ко-многим», можно применять метод prefetch_related(),
# он позволит снизить количество выполняемых запросов к базе. При этом под капотом последовательно выполняются два SQL-запроса,
# а потом их результат объединяется в один QuerySet.

# Такая оптимизация не всегда применима. Например, если на страницу выводится не список объектов,
# а только один объект, то никакой экономии в запросах prefetch_related() не даст. 

# Собрать несколько тегов в единую строку можно с помощью фильтра шаблонизатора join

# {{ names|join:", " }}
# <!-- Выведет: Гена, Чебурашка, Шапокляк, Лариска -->

# <!-- templates/birthday/birthday_list.html -->
# ...
#     <div class="col-10">  
#       <div>
#         {{ birthday.first_name }} {{ birthday.last_name }} - {{ birthday.birthday }}<br>
#         <a href="{% url 'birthday:detail' birthday.id %}">Сколько до дня рождения?</a>
#       </div>

#       <!-- Начало нового блока кода -->
#       <div>
#         <!-- Чтобы сократить количество кода —
#           введём переменную all_tags, в которой будут лежать все теги объекта -->
#         {% with all_tags=birthday.tags.all %}
#           <!-- Если у записи есть хоть один тег -->
#           {% if all_tags %}
#             <!-- Выводим теги через запятую, самую первую букву делаем заглавной -->
#             {{ all_tags|join:", "|lower|capfirst }} 
#             <!-- Также выводим username пользователя -->
#             пользователя {{ birthday.author.username }}
#           {% endif %}
#         {% endwith %}
#       </div>
#       <!-- Конец нового блока кода -->

# Последовательность фильтров {{ all_tags|join:", "|lower|capfirst }} 
# объединяет все теги через запятую,
# делает все буквы внутри полученной строки маленькими,
# делает заглавной первую букву строки.
