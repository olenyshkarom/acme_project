from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    # path('', views.birthday, name='create'),
    path('', views.BirthdayCreateView.as_view(), name='create'),
    # path('list/', views.birthday_list, name='list'),
    path('list/', views.BirthdayListView.as_view(), name='list'),   # Этот метод есть у всех встроенных CBV
    # наследники класса ListView ищут шаблон <название приложения>/<название модели>_list.html;
    path('<int:pk>/', views.BirthdayDetailView.as_view(), name='detail'),
    # path('<int:pk>/edit/', views.birthday, name='edit'),
    path('<int:pk>/edit/', views.BirthdayUpdateView.as_view(), name='edit'),
    # path('<int:pk>/delete/', views.delete_birthday, name='delete'),
    path('<int:pk>/delete/', views.BirthdayDeleteView.as_view(), name='delete'),
    path('login_only/', views.simple_view),
    # path('create/', views.BirthdayCreateView.as_view(), name='create'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
]
