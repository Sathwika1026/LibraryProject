"""
URL configuration for LibrarySystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from  LibraryApp import views
from LibraryApp.views import edit_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.register, name='register'),
    path('login/', views.login_view, name='login'),  # renamed view
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
      

    path('books/', views.view_books, name='view_books'),
    path('add-book/', views.add_book, name='add_book'),  # Optional if you use it
    path('profile/', views.profile, name='profile'),   
    

    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('my-books/', views.my_books, name='my_books'),
    path('admin-borrows/', views.borrowed_books_admin, name='admin_borrowed_books'),

    path('edit-book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete-book/<int:book_id>/', views.delete_book, name='delete_book'),

    path('my-books/', views.my_books, name='my_books'),
    path('return-book/<int:borrow_id>/', views.return_book, name='return_book'),

    path('edit-profile/', edit_profile, name='edit_profile'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('',views.main),

]
