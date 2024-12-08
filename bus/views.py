from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import BusForm
from .models import Bus
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bookings.forms import BookingForm
from django.db.models import Avg, Count


class BusListView(ListView):
    model = Bus
    template_name = 'bus/bus_list.html'
    def get(self, request, *args, **kwargs):
        buss = self.model.objects.all()
        return render(request, self.template_name, {
            'buss': buss,
            })

class BusDetailView(DetailView):
    model = Bus
    template_name = 'bus/bus_detail.html'

class AddBusView(View):
    template_name = 'bus/bus_add.html'
    form_class = BusForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            bus = form.save(commit=False)
            bus.role = 'customer'
            bus.save()
            
            messages.success(request, "adding bus successful!")
            return redirect('bus:bus_list')
        messages.error(request, "There was an error in the adding bus process.")
        return render(request, self.template_name, {'form': form})

class UpdateBusView(UpdateView):
    model = Bus
    form_class = BusForm
    template_name = 'bus/bus_update.html'

    def form_valid(self, form):
        messages.success(self.request, "Bus updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the bus.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('bus:bus_list')

class DeleteBusView(View):
    template_name = 'bus/bus_list.html'
    model = Bus
    def get(self, request, *args, **kwargs):
        buss = self.model.objects.all()
        return render(request, self.template_name, {'buss': buss})

    def post(self, request, pk, *args, **kwargs):
        bus = get_object_or_404(Bus, pk=pk)
        bus.delete()
        messages.success(request, "Bus deleted successfully!")
        return redirect('bus:bus_list')



# customer
from django.db.models import Q

class BusListCustomerView(ListView):
    model = Bus
    template_name = 'bus/bus_customer_list.html'
    context_object_name = 'buses'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('search', '').strip()
        departure = self.request.GET.get('departure', '').strip()
        destination = self.request.GET.get('destination', '').strip()
        per_page = request.GET.get('per_page', 12)

        try:
            per_page = int(per_page)
        except ValueError:
            per_page = 12

        buses = Bus.objects.all().annotate(
            average_rating=Avg('review__rating'),
            rating_count=Count('review')
        )

        if query:
            buses = buses.filter(name__icontains=query)
        if departure:
            buses = buses.filter(departure__icontains=departure)
        if destination:
            buses = buses.filter(destination__icontains=destination)

        paginator = Paginator(buses, per_page)
        page_number = self.request.GET.get('page')
        try:
            bus_page = paginator.page(page_number)
        except PageNotAnInteger:
            bus_page = paginator.page(1)
        except EmptyPage:
            bus_page = paginator.page(paginator.num_pages)

        unique_departures = Bus.objects.values_list('departure', flat=True).distinct()
        unique_destinations = Bus.objects.values_list('destination', flat=True).distinct()

        context = {
            'buses': bus_page,
            'per_page': per_page,
            'total_items': paginator.count,
            'search': query,
            'departure': unique_departures,
            'destination': unique_destinations,
        }

        return render(request, self.template_name, context)

class BusDetailCustomerView(DetailView):
    model = Bus
    template_name = 'bus/bus_customer_detail.html'
    context_object_name = 'bus'

    def get(self, request, pk,  *args, **kwargs):
        form = BookingForm()
        bus = get_object_or_404(Bus, pk=pk)
        return render(request, self.template_name, {'form': form, 'bus': bus})