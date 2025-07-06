# forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Register
from .models import Book

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    otp = forms.CharField(max_length=6, required=False)  # Add this line

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned_data




class RegisterForm(forms.ModelForm):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ]

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect()
    )

    class Meta:
        model = Register
        fields = ['user_type']



from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'category', 'author', 'copies', 'description']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'background-color:#2a2a2a; color:white; border:1px solid #444;'
            field.widget.attrs['placeholder'] = f'Enter {field.label.lower()}'

        # Customize description field separately
        self.fields['description'].widget.attrs['rows'] = 5
        self.fields['description'].widget.attrs['style'] += ' height:150px; resize: vertical;'

class ExcelUploadForm(forms.Form):
    file = forms.FileField(label="Upload Excel File")

