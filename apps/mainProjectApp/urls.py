from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
    url(r'^new$', views.newUser),
    url(r'^signOn$', views.signOn),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^add_item$', views.add_item),
    url(r'^add_item_db$', views.add_item_db),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^add_to_wishlist/(?P<id>\d+)$', views.add_to_wishlist),
    url(r'^item_page/(?P<id>\d+)$', views.item_page),
    url(r'^remove_wishlist/(?P<id>\d+)$', views.remove_wishlist),



]
