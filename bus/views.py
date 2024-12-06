from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import render, redirect
from .forms import BusForm
from .models import Bus

class BusListView(ListView):
    model = Bus
    template_name = 'bus/bus_list.html'


class BusDetailView(DetailView):
    model = Bus
    template_name = 'bus/bus_detail.html'


def add_bus(request):
    if request.method == "POST":
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bus_list')
    else:
        form = BusForm()
    return render(request, 'bus/add_bus.html', {'form': form})

