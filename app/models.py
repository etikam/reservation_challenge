from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

User = get_user_model()


# Modèle Parent - Ressource (Resource)
class Resource(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField() #Price par heure de l'équipement en franc 
    is_available = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
    
# Modèle Salle (Room) - Hérite de Resource
class Room(Resource):
    capacity = models.IntegerField(null=True, blank=True)  # Spécifique aux salles
    location = models.CharField(max_length=255)  # Localisation spécifique des salles
    # image = models.ImageField(upload_to="rooms_images")
    image = models.CharField(max_length=255)

    def __str__(self):
        return f"Salle : {self.name} - {self.location}"


# Modèle Équipement (Equipment) - Hérite de Resource
class Equipment(Resource):
    # equipment_type = models.CharField(max_length=100)  # Type d'équipement
    maintenance_required = models.BooleanField(default=False)  # Indique si un entretien est nécessaire
    # image = models.ImageField(upload_to="equipement_images")
    image = models.CharField(max_length=255)

    def __str__(self):
        return f"Équipement : {self.name}"


class ServiceProvider(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default="Aucune description")
    contact = models.CharField(max_length=200)



# Modèle Service (Service) - Hérite de Resource
class Service(Resource):
    service_type = models.CharField(max_length=100)  # Type de service
    provider = models.ManyToManyField(ServiceProvider,related_name="services")
    # image = models.ImageField(upload_to="service_images",blank=True,null=True)
    image = models.CharField(max_length=255)
    def __str__(self):
        return f"Service : {self.name} - Fournisseur : {self.provider}"


# Modèle Réservation (Reservation)
class Reservation(models.Model):
    status_choices = [
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    resource = GenericForeignKey('content_type', 'object_id')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

    def clean(self):
        # Vérifie si la réservation chevauche une réservation existante
        overlapping_reservations = Reservation.objects.filter(
            content_type=self.content_type,
            object_id=self.object_id,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )
        if overlapping_reservations.exists():
            raise ValidationError("Cette ressource est déjà réservée pour ce créneau horaire.")

    def save(self, *args, **kwargs):
        # Appelle la méthode de validation avant de sauvegarder
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Réservation de {self.resource} par {self.user} de {self.start_time} à {self.end_time}"