from django.conf.urls import url
from rango import views
urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'^about/$', views.about, name='about'),
]

"""Map this view to /rango/about/. For this step, you’ll only need to edit the urls.py
of the Rango app. Remember the /rango/ part is handled by the projects urls.py."""