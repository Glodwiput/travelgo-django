from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from .forms import ServiceForm
from .models import Service
from django.contrib.auth.mixins import LoginRequiredMixin
from users.mixins import RoleRequiredMixin

class ServiceListView(RoleRequiredMixin,ListView):
    model = Service
    template_name = 'service/service_list.html'
    allowed_roles = ['admin','staff']

    def get(self, request, *args, **kwargs):
        services = self.model.objects.all()
        return render(request, self.template_name, {
            'services': services,
            })

class ServiceDetailView(RoleRequiredMixin,DetailView):
    model = Service
    template_name = 'service/service_detail.html'
    allowed_roles = ['admin','staff']


class AddServiceView(RoleRequiredMixin,View):
    template_name = 'service/service_add.html'
    form_class = ServiceForm
    allowed_roles = ['admin','staff']


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            services = form.save(commit=False)
            services.role = 'customer'
            services.save()
            
            messages.success(request, "adding Service successful!")
            return redirect('services:service_list')
        messages.error(request, "There was an error in the adding Service process.")
        return render(request, self.template_name, {'form': form})

class UpdateServiceView(RoleRequiredMixin,UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service/service_update.html'
    allowed_roles = ['admin','staff']


    def form_valid(self, form):
        messages.success(self.request, "Service updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the Service.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('services:service_list')

class DeleteServiceView(RoleRequiredMixin,View):
    template_name = 'service/Service_list.html'
    model = Service
    allowed_roles = ['admin','staff']

    def get(self, request, *args, **kwargs):
        services = self.model.objects.all()
        return render(request, self.template_name, {'services': services})

    def post(self, request, pk, *args, **kwargs):
        service = get_object_or_404(Service, pk=pk)
        service.delete()
        messages.success(request, "Service deleted successfully!")
        return redirect('services:service_list')



