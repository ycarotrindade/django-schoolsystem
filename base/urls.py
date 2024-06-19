from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('',views.login_page,name='login'),
    path('students/create/',views.students_create,name='students_create'),
    path('students/delete/<str:pk>/',views.students_delete,name='student_delete'),
    path('students/edit/<str:pk>/',views.student_edit,name='student_edit'),
    path('students/<str:page>/',views.students,name='students'),
    path('employees/delete/<str:pk>/',views.employee_delete,name='employee_delete'),
    path('employees/edit/<str:pk>/',views.employee_edit,name='employee_edit'),
    path('employees/add/',views.employee_add,name='employee_add'),
    path('employees/reset/<str:pk>/',views.reset_password,name='reset_password'),
    path('employees/<str:page>/',views.employees,name='employees'),
    path('logout/',views.logout_func,name='logout')
]