from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
import pandas as pd
from django.db.models import Q
from .forms import BookForm, ExcelUploadForm
from .forms import UserForm, RegisterForm, BookForm
from .models import Book, Borrow
from django.contrib.auth.forms import UserChangeForm

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

            return redirect('home') 
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  

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
    category_filter = request.GET.get('category')
    books = Book.objects.all()
    if category_filter:
        books = books.filter(category=category_filter)

    categories = Book.objects.values_list('category', flat=True).distinct()

    return render(request, 'view_books.html', {
        'books': books,
        'categories': categories,
        'selected_category': category_filter
    })



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
        if 'submit_book' in request.POST:
            form = BookForm(request.POST)
            if form.is_valid():
                book = form.save(commit=False)
                book.added_by = request.user
                book.save()
                messages.success(request, 'Book added successfully!')
                return redirect('view_books')

        elif 'submit_excel' in request.POST:
            excel_form = ExcelUploadForm(request.POST, request.FILES)
            if excel_form.is_valid():
                try:
                    df = pd.read_excel(request.FILES['file'])
                    for _, row in df.iterrows():
                        Book.objects.create(
                            title=row['Title'],
                            category=row['Category'],
                            author=row['Author'],
                            copies=row['Copies'],
                            description=row['Description'],
                            added_by=request.user
                        )
                    messages.success(request, 'Books added from Excel successfully!')
                except Exception as e:
                    messages.error(request, f"Error reading Excel file: {str(e)}")
                return redirect('view_books')
    else:
        form = BookForm()
        excel_form = ExcelUploadForm()

    return render(request, 'add_book.html', {'form': form, 'excel_form': excel_form})

@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)

    if book.copies <= 0:
        messages.error(request, "This book is currently unavailable.")
        return redirect('view_books')

    
    book.copies -= 1
    book.save()


    Borrow.objects.create(user=request.user, book=book)
    messages.success(request, f"You borrowed: {book.title}")
    return redirect('view_books')

@login_required
def my_books(request):
    borrows = Borrow.objects.filter(user=request.user).select_related('book')
    return render(request, 'my_books.html', {'borrows': borrows})


@login_required
def borrowed_books_admin(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'admin':
        return HttpResponseForbidden("Only admin can view borrow records.")

    borrows = Borrow.objects.select_related('user', 'book').order_by('-borrowed_at')
    return render(request, 'admin_borrowed_books.html', {'borrows': borrows})

@login_required
def edit_book(request, book_id):
    if request.user.profile.user_type != 'admin':
        return HttpResponseForbidden()
    
    book = Book.objects.get(id=book_id)
    form = BookForm(request.POST or None, instance=book)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Book updated successfully!")
        return redirect('view_books')

    return render(request, 'edit_book.html', {'form': form})


@login_required
def delete_book(request, book_id):
    if request.user.profile.user_type != 'admin':
        return HttpResponseForbidden()
    
    book = Book.objects.get(id=book_id)
    book.delete()
    messages.success(request, "Book deleted successfully.")
    return redirect('view_books')

@login_required
def return_book(request, borrow_id):
    borrow = Borrow.objects.get(id=borrow_id, user=request.user)

    borrow.book.copies += 1
    borrow.book.save()

    borrow.delete()

    messages.success(request, f"Returned: {borrow.book.title}")
    return redirect('my_books')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})
