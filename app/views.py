from typing import Any
from django.shortcuts import render
from django.views import generic
from .models import (Reservation, 
                     Room, Service, 
                     ServiceProvider,
                     Equipment
                    )

# Create your views here.


def index(request):
    ressources = {
        'room':Room.objects.all().order_by('name'),
        'equipment':Equipment.objects.all().order_by('name'),
        'service':Service.objects.all().order_by('name')
    }
    context = {
        'ressources':ressources
    }
    return render(request,"app/index.html",context)


# Vue de details pour une réssource

class DetailRoom(generic.DetailView):
    model = Room
    template_name = 'app/ressourceDetail.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ressource_type'] = "Room"
        
        return context
    
    
class DetailService(generic.DetailView):
    model = Service
    template_name = 'app/ressourceDetail.html'

    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ressource_type'] = "Service"
        
        return context
    


class DetailEquipment(generic.DetailView):
    model = Equipment
    template_name = 'app/ressourceDetail.html'

    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ressource_type'] = "Equipment"
        
        return context
    
    