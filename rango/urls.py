from django.conf.urls import url
from rango import views
urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'^about/$', views.about, name='about'),
url(r'^add_category/$', views.add_category, name='add_category'),
url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
views.show_category, name='show_category'),
]

"""Map this view to /rango/about/. For this step, you’ll only need to edit the urls.py
of the Rango app. Remember the /rango/ part is handled by the projects urls.py."""