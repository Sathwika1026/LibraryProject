from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .forms import UserForm, RegisterForm, BookForm
from .models import Book

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        register_form = RegisterForm(request.POST)

        if user_form.is_valid() and register_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            register = register_form.save(commit=False)
            register.user = user
            register.save()

            messages.success(request, "Registered successfully! Please login.")
            return redirect('login')
    else:
        user_form = UserForm()
        register_form = RegisterForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'register_form': register_form
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            user_type = getattr(user.profile, 'user_type', None)

            messages.success(request, f"Welcome back, {user.username}!")

            # Redirect based on user type
            return redirect('home')  # you can change redirection if needed
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # reload login form

    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


@login_required
def home(request):
    return render(request, 'home.html')


def csrf_failure(request, reason=""):
    return HttpResponseForbidden("CSRF verification failed. Please refresh the page and try again.")


@login_required
def view_books(request):
    books = Book.objects.all()
    return render(request, 'view_books.html', {'books': books})


@login_required
def profile(request):
    return render(request, 'profile.html', {
        'user': request.user,
        'profile': request.user.profile
    })


@login_required
def add_book(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'admin':
        return HttpResponseForbidden("Only admin can add books.")

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            messages.success(request, 'Book added successfully!')
            return redirect('view_books')
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})
