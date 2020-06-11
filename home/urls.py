from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    path('admin/advisor', views.addAdvisor, name='Add_Advisor'),
    path('user/login/', views.loginView, name='login'),
    path('user/register/', views.registerView, name='register'),
    path('user/<int:user_id>/advisor', views.getAdvisors, name='get_advisors'),
    path('user/<int:user_id>/advisor/<int:advisor_id>', views.bookCall, name='book_call'),
    path('user/<int:user_id>/advisor/bookings', views.getAllCalls, name='get_all_call'),
]