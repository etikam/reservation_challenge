from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Reservation, Room, Service, Equipment, Waitlist
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.http import Http404
from django.contrib import messages


# Create your views here.


def index(request):
    ressources = {
        "room": Room.objects.all().order_by("name"),
        "equipment": Equipment.objects.all().order_by("name"),
        "service": Service.objects.all().order_by("name"),
    }
    context = {"ressources": ressources}
    return render(request, "app/index.html", context)


# Vue de details pour une réssource


class DetailRoom(generic.DetailView):
    model = Room
    template_name = "app/ressourceDetail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ressource_type"] = "Room"

        return context


class DetailService(generic.DetailView):
    model = Service
    template_name = "app/ressourceDetail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ressource_type"] = "Service"

        return context


class DetailEquipment(generic.DetailView):
    model = Equipment
    template_name = "app/ressourceDetail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["ressource_type"] = "Equipment"

        return context

#===============================RESERVATION========================================
@login_required(login_url="account:login")
def reserver(request, id, ressource_type):
    resource_models = {
        "Room": Room,
        "Service": Service,
        "Equipment": Equipment,
    }

    model = resource_models.get(ressource_type)
    if not model:
        raise Http404("Type de ressource invalide.")

    ressource = get_object_or_404(model, id=id)
    content_type = ContentType.objects.get_for_model(ressource)

    start_time = timezone.now()
    end_time = start_time + timedelta(days=1)
  
    if Reservation.is_overlapping(ressource, start_time, end_time):
        messages.warning(
            request,
            "La ressource est déjà réservée pendant cette période. Vous pouvez entrer en file d'attente.",
        )
        return redirect("add-to-waitelist", resource_model=ressource._meta.model_name, resource_id=ressource.id)

    Reservation.objects.create(
        user=request.user,
        content_type=content_type,
        object_id=ressource.id,
        start_time=start_time,
        end_time=end_time,
    )

    messages.success(
        request,
        "Vous avez commencé à faire une réservation. Veuillez continuer "
        "vers le paiement pour terminer, sinon un autre utilisateur pourra occuper la ressource.",
    )
    return redirect("my-reservations")


@login_required(login_url="account:login")
def my_reservation(request):
    # Récupération de toutes les réservations de l'utilisateur connecté
    reservations = Reservation.objects.filter(user=request.user)



    context = {
        "my_reservations": reservations,
        "no_reservations": not reservations.exists(),  # Indique si l'utilisateur n'a pas de réservations
    }

    return render(request, "app/my_reservations.html", context)



@login_required(login_url="account:login")
def cancel_reservation(request, reservation_id):
    # Récupérer la réservation en vérifiant qu'elle appartient à l'utilisateur connecté
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if reservation.status == "cancelled":
        messages.warning(request, "Cette réservation est déjà annulée.")
    else:
        # Mettre à jour le statut de la réservation
        reservation.status = "cancelled"
        reservation.save()
        messages.success(request, "Votre réservation a été annulée avec succès.")

    # Rediriger vers la liste des réservations
    return redirect("my-reservations")


@login_required(login_url="account:login")
def delete_reservation(request, reservation_id):
    # Récupérer la réservation appartenant à l'utilisateur
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if reservation.status != "cancelled":
        messages.warning(
            request, "Vous ne pouvez supprimer qu'une réservation annulée."
        )
        return redirect("my_reservations")

    # Supprimer la réservation
    reservation.delete()
    messages.success(request, "Réservation supprimée avec succès.")
    return redirect("my-reservations")


@login_required
def add_to_waitlist(request, resource_model, resource_id):
    # Récupère la classe du modèle dynamique
    model = ContentType.objects.get(model=resource_model).model_class()
    resource = get_object_or_404(model, id=resource_id)


  #CES HORAIRE DOIVENT VENIR DU FORMULAIRE RESERVATION
    start_time = timezone.now()
    end_time = start_time + timedelta(hours=1)

    Waitlist.add_to_waitlist(request.user, resource, start_time, end_time)
    messages.success(request, "Vous avez été ajouté à la file d'attente.")
#=======================================================================================
    # Redirection vers la page de détails ou liste
    return redirect("my-waitlite")

@login_required
def view_user_waitlist(request):
    # Récupère tous les enregistrements dans la file d'attente pour l'utilisateur connecté
    waitlist = Waitlist.objects.filter(user=request.user).order_by('priority', 'added_at')
    context = {
        "waitlist": waitlist,
    }
    return render(request, "app/view_user_waitlist.html", context)
