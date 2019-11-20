from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^test_celery',views.test_celery),
]