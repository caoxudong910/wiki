"""wiki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test/',views.test),
    # http://127.0.0.1:8000/v1/users
    url(r'^v1/users',include('user.urls')),
    # http://127.0.0.1:8000/v1/tokens
    url(r'^v1/tokens',include('wtoken.urls')),
    # http://127.0.0.1:8000/v1/topic
    url(r'^v1/topics',include('topic.urls')),
    # http://127.0.0.1:8000/v1/message
    url(r'^v1/messages',include('message.urls'))
]

# 绑定 media_url 和 media_root,
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)