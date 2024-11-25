from django.contrib import admin
from .models import Room, Service, ServiceProvider, Equipment, Reservation, Waitlist

# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'location', 'is_available')  # Affiche ces champs dans la liste
    search_fields = ('name', 'location')  # Permet de rechercher par nom et localisation
    list_filter = ('is_available',)  # Filtre par disponibilité


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'is_available')  # Affiche ces champs dans la liste
    search_fields = ('name', 'service_type')  # Permet de rechercher par nom et type de service
    list_filter = ('is_available',)  # Filtre par disponibilité


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact')  # Affiche ces champs dans la liste
    search_fields = ('name', 'contact')  # Permet de rechercher par nom et contact


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'maintenance_required', 'is_available')  # Affiche ces champs dans la liste
    search_fields = ('name',)  # Permet de rechercher par nom et type d'équipement
    list_filter = ('maintenance_required', 'is_available')  # Filtre par entretien requis et disponibilité


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'start_time', 'end_time', 'status')  # Affiche ces champs dans la liste
    search_fields = ('user__username', 'resource__name', 'status')  # Permet de rechercher par nom d'utilisateur, ressource et statut
    list_filter = ('status', 'start_time')  # Filtre par statut et temps de début
    readonly_fields = ('user',)  # Rendre le champ utilisateur en lecture seule


@admin.register(Waitlist)
class AdminWaitlist(admin.ModelAdmin):
    pass