from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    phone = forms.CharField(
        max_length=15, 
        required=True, 
        label="Phone Number",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Phone Number',
        })
    )
    address = forms.CharField(
        required=True, 
        label="Address",
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Address',
            'rows': 3,
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'address']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Password',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Confirm Password',
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )
        return user

class UserAddForm(UserCreationForm):
    phone = forms.CharField(
        max_length=15, 
        required=True, 
        label="Phone Number",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Phone Number',
        })
    )
    address = forms.CharField(
        required=True, 
        label="Address",
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Address',
            'rows': 3,
        })
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'address','role']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Email',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Password',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Confirm Password',
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )
        return user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']

class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role']
        exclude = ['password']
