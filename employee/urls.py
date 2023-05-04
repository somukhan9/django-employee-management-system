from django.urls import path

from . import views

app_name = 'employee'

urlpatterns = [
    path("", views.view_all, name='view_all'),
    path('<int:id>/', views.view_single_employee, name='view_single_employee'),
    path('add/', views.add, name='add'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
]
