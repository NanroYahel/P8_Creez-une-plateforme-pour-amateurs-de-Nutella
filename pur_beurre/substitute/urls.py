from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.legal, name="legal"),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^sign_in/$', views.sign_in, name='sign_in'),
    url(r'^account/$', views.user_account, name='account'),
    url(r'^product/(?P<product_id>[0-9]+)/$', views.product_sheet, name='product_sheet'),
    url(r'^search/$', views.search, name='search'),

]