
from django.conf.urls import url
from . import views


urlpatterns = [
    # http://127.0.0.1:8000/v1/topics/<username>
    url(r'^/(?P<author_id>\w{1,11})$',views.topics),
]