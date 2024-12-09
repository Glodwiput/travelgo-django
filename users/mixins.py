from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404



class NotLoggedInRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.filter(name="customer").exists():
                return redirect('bookings:booking_list')
            elif request.user.groups.filter(name__in=["admin", "staff"]).exists():
                return redirect('bus:bus_list')
            messages.warning(request, "You are already logged in.")
            return redirect('users:profile')
        
        return super().dispatch(request, *args, **kwargs)



class RoleRequiredMixin(LoginRequiredMixin):
    allowed_roles = [] 
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        
        if self.allowed_roles and request.user.groups.filter(name__in=self.allowed_roles).exists():
            return super().dispatch(request, *args, **kwargs)
        
        raise Http404("Page not found")

from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin

class CustomLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
       
        if not request.user.is_authenticated:
            
            return redirect('users:login')
        
        return super().dispatch(request, *args, **kwargs)

