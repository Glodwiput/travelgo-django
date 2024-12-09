from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, User
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import RegisterForm, EditProfileForm, EditUserForm, UserAddForm
from django.views.generic import ListView
from django.contrib.auth.models import Group
from django.db.models import Sum, Count
from bookings.models import Booking
from bus.models import Bus
from services.models import Service
from reviews.models import Review
from .decorators import role_required
from django.http import Http404
from .mixins import RoleRequiredMixin, NotLoggedInRequiredMixin, CustomLoginRequiredMixin









def home_view(request):
    return render(request, 'users/homepage.html')


class RegisterView(NotLoggedInRequiredMixin,View):
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
            
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
            user.save()
           
            Profile.objects.filter(user=user).update(
                phone=form.cleaned_data.get('phone', ''),
                address=form.cleaned_data.get('address', '')
            )
            messages.success(request, "Registration successful! Please log in.")
            return redirect('users:login')
        messages.error(request, "There was an error in the registration process.")
        return render(request, self.template_name, {'form': form})


class CustomLoginView(NotLoggedInRequiredMixin,LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Login successful!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user
        if not user.is_authenticated:
            return reverse_lazy('users:login')

        if user.is_superuser or user.groups.filter(name='staff').exists():
            return reverse_lazy('bus:bus_list')
        elif user.groups.filter(name='customer').exists():
            return reverse_lazy('bookings:booking_list')

        return reverse_lazy('bookings:booking_list')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)

class ProfileView(CustomLoginRequiredMixin, View):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            
            profile = Profile.objects.create(user=request.user)
        return render(request, self.template_name, {'user': request.user, 'profile': profile})


class EditProfileView(CustomLoginRequiredMixin, View):
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


class UserListView(RoleRequiredMixin,ListView):
    model = User
    template_name = 'users/admin/user_list.html'
    allowed_roles = ['admin']
    def get(self, request, *args, **kwargs):
        users = self.model.objects.all()
        return render(request, self.template_name, {
            'users': users,
            })

class UserAddView(RoleRequiredMixin,View):
    template_name = 'users/admin/user_add.html'
    form_class = UserAddForm
    allowed_roles = ['admin']


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            
            user = form.save(commit=False)
            user.skip_signals = True
            
            if role == 'admin':
                user.is_superuser = True
                user.is_staff = True
            elif role == 'staff':
                user.is_staff = True

            user.save()
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
            
            
            Profile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone', ''),
                address=form.cleaned_data.get('address', '')
            )
            
            messages.success(request, "User added successfully!")
            return redirect('users:login')
        
        messages.error(request, "There was an error in the add user process.")
        return render(request, self.template_name, {'form': form})

class UserDeleteView(RoleRequiredMixin,View):
    template_name = 'users/admin/user_list.html'
    model = User
    allowed_roles = ['admin']

    def get(self, request, *args, **kwargs):
        users = self.model.objects.all()
        return render(request, self.template_name, {'users': users})

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect('users:user_list')





@login_required
@role_required(['admin','staff'])
def reports_view(request):
    
    bus_id = request.GET.get('bus')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    
    bookings = Booking.objects.all()
    
    
    if bus_id:
        bookings = bookings.filter(bus_id=bus_id)

   
    if start_date and end_date:
        bookings = bookings.filter(booking_date__range=[start_date, end_date])

    
    if min_price:
        bookings = bookings.filter(price_total__gte=min_price)
    if max_price:
        bookings = bookings.filter(price_total__lte=max_price)

    
    total_revenue = bookings.aggregate(Sum('price_total'))['price_total__sum'] or 0
    total_bookings = bookings.count()
    most_popular_bus = Bus.objects.annotate(booking_count=Count('booking')).order_by('-booking_count').first()

   
    user_counts = User.objects.annotate(total_bookings=Count('booking')).order_by('-total_bookings')[:10]  # Top 10 users by number of bookings

    
    review_counts = Review.objects.values('user__username').annotate(total_reviews=Count('id')).order_by('-total_reviews')[:10]  # Top 10 users by number of reviews

   
    context = {
        'bookings': bookings,
        'buses': Bus.objects.all(),
        'total_revenue': total_revenue,
        'total_bookings': total_bookings,
        'most_popular_bus': most_popular_bus,
        'user_report': user_counts,
        'review_report': review_counts,
    }
    return render(request, 'reports/reports.html', context)


