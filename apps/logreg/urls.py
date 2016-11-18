from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register_user$', views.register_user, name="register_user"),
    url(r'^success$', views.success, name="success"),
    url(r'^login_user$', views.login_user, name="login_user"),
    url(r'^logout$',views.logout, name="logout"), 
    url(r'^add_plan$', views.add_plan, name="add_plan"),
    url(r'^trip_validation$',views.trip_validation, name="trip_validation"),
    url(r'^plan$', views.plan, name="plan"),
    url(r'^(?P<id>\d+)/join$', views.join, name="join"),
]