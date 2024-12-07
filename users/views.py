from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, EditProfileForm, EditUserForm
from .models import Profile, User

from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import RegisterForm, EditProfileForm, EditUserForm, UserAddForm
from .models import Profile
from django.views.generic import ListView
from django.shortcuts import get_object_or_404



def home_view(request):
    return render(request, 'users/homepage.html')


class RegisterView(View):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'customer'
            user.skip_signals = False
            user.save()
            # Buat profile dengan data tambahan
            Profile.objects.filter(user=user).update(
                phone=form.cleaned_data.get('phone', ''),
                address=form.cleaned_data.get('address', '')
            )
            messages.success(request, "Registration successful! Please log in.")
            return redirect('users:login')
        messages.error(request, "There was an error in the registration process.")
        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Login successful!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)

class ProfileView(LoginRequiredMixin, View):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            # Buat profile jika tidak ada
            profile = Profile.objects.create(user=request.user)
        return render(request, self.template_name, {'user': request.user, 'profile': profile})

class EditProfileView(LoginRequiredMixin, View):
    template_name = 'users/edit_profile.html'
    user_form_class = EditUserForm
    profile_form_class = EditProfileForm

    def get(self, request, *args, **kwargs):
        user_form = self.user_form_class(instance=request.user)
        profile_form = self.profile_form_class(instance=request.user.profile)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        user_form = self.user_form_class(request.POST, instance=request.user)
        profile_form = self.profile_form_class(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('users:profile')
        messages.error(request, "There was an error updating your profile.")
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})


class UserListView(ListView):
    model = User
    template_name = 'users/admin/user_list.html'
    def get(self, request, *args, **kwargs):
        users = self.model.objects.all()
        return render(request, self.template_name, {
            'users': users,
            })


class UserAddView(View):
    template_name = 'users/admin/user_add.html'
    form_class = UserAddForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Buat user terlebih dahulu
            user = form.save(commit=False)
            user.skip_signals = True
            user.save()
            
            # Buat profil terkait secara manual
            Profile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone', ''),
                address=form.cleaned_data.get('address', '')
            )
            
            messages.success(request, "User added successfully!")
            return redirect('users:login')
        
        messages.error(request, "There was an error in the add user process.")
        return render(request, self.template_name, {'form': form})



class UserDeleteView(View):
    template_name = 'users/admin/user_list.html'
    model = User
    def get(self, request, *args, **kwargs):
        users = self.model.objects.all()
        return render(request, self.template_name, {'users': users})

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect('users:user_list')






# # Register View
# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.role = 'customer' 
#             user.save()
#             Profile.objects.filter(user=user).update(
#                 phone=form.cleaned_data.get('phone', ''),
#                 address=form.cleaned_data.get('address', '')
#             )
#             login(request, user)
#             messages.success(request, "Registration successful! Please log in.")
#             return redirect('users:login')
#         else:
#             messages.error(request, "There was an error in the registration process.")
#     else:
#         form = RegisterForm()
#     return render(request, 'users/register.html', {'form': form})

# # Login View
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Login successful!")
#             return redirect('users:profile')
#         else:
#             messages.error(request, "Invalid username or password.")
#     return render(request, 'users/login.html')

# # Logout View
# @login_required
# def logout_view(request):
#     logout(request)
#     messages.success(request, "You have been logged out.")
#     return redirect('users:login')

# # Profile View
# @login_required
# def profile_view(request):
#     try:
#         profile = request.user.profile 
#     except Profile.DoesNotExist:# Buat profile jika tidak ada
#         profile = Profile.objects.create(user=request.user)
#     return render(request, 'users/profile.html', {'user': request.user, 'profile': profile})

# # Edit Profile View
# @login_required
# def edit_profile_view(request):
#     if request.method == 'POST':
#         user_form = EditUserForm(request.POST, instance=request.user)
#         profile_form = EditProfileForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, "Profile updated successfully.")
#             return redirect('users:profile')
#         else:
#             messages.error(request, "There was an error updating your profile.")
#     else:
#         user_form = EditUserForm(instance=request.user)
#         profile_form = EditProfileForm(instance=request.user.profile)
#     return render(request, 'users/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
