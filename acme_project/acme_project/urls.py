# Импортируем настройки проекта.
from django.conf import settings
# Импортируем функцию, позволяющую серверу разработки отдавать файлы.
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
# import debug_toolbar

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('birthday/', include('birthday.urls')),
    # Подключаем urls.py приложения для работы с пользователями.
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('pages:homepage'),
        ),
        name='registration',
    ),
    # Применим этот подход: в проекте нет отдельного
    # приложения для работы с пользователями, и разместить CBV некуда; создавать приложение ради единственного view-класса не хочется.

    # В конце добавляем к списку вызов функции static.
] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # исключительно для этапа разработки

# Этот способ будет работать только в режиме разработки (когда проект запускается командой python manage.py runserver) и при настройке DEBUG = True в settings.py.
# потом заменить на DEBUG = False

handler404 = 'core.views.page_not_found'


# Если проект запущен в режиме разработки...
if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

# Если Django Debug Toolbar показывает 404 ошибку на странице SQL
# надо подключать тулбар до подключения функции static(): 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
