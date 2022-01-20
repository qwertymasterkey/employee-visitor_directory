from django.urls import path,include
from django.contrib import admin
from django.contrib.auth.views import LoginView
from . import views
from .views import RegisterAPI
from knox import views as knox_views
from .views import LoginAPI
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path('',views.index,name="index"),
    path('home.html',views.index,name="home"),
    path("register", views.register_request, name="register"),
    path("login.html",views.login_request,name='login'),
    path("logout", views.logout_request, name= "logout"),
    path("employee.html",views.emp,name="employee"),
    path("delete_emp/<emp_id>",views.delete_emp,name="delete_emp"),
    path("update_emp/<emp_id>",views.update_emp,name="update_emp"),
    path("updated_emp/<emp_id>",views.updated_emp,name="updated_emp"),
    path("visitor.html",views.vis,name="visitor"),
    path("delete_vis/<vis_id>",views.delete_vis,name="delete_vis"),
    path("update_vis/<vis_id>",views.update_vis,name="update_vis"),
    path("updated_vis/<vis_id>",views.updated_vis,name="updated_vis"),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='api/login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='api/logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='api/logoutall'),
    path('api/emp',views.emplist.as_view()),
    path('api/emp/<int:pk>',views.empdetail.as_view()),
    path('api/vis',views.visitorlist.as_view()),
    path('api/vis/<int:pk>',views.visitordetail.as_view()),
    path('auth/',include('rest_framework.urls',namespace='rest_framework'))
]