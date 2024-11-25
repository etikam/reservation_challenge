from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    resource = GenericForeignKey('content_type', 'object_id')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=status_choices, default='pending')


    @staticmethod
    def is_overlapping(resource, start_time, end_time):
        # Récupérer le `ContentType` pour le modèle de la ressource
        content_type = ContentType.objects.get_for_model(type(resource))

        # Vérifier les chevauchements
        return Reservation.objects.filter(
            content_type=content_type,
            object_id=resource.id,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status="confirmed",
        ).exists()

    def __str__(self):
        return f"Réservation de {self.resource} par {self.user} de {self.start_time} à {self.end_time}"
    

#model de la fille d'attente
class Waitlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    resource = GenericForeignKey('content_type', 'object_id')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    priority = models.PositiveIntegerField(default=0)  # Gère l'ordre de priorité dans la file d'attente
    added_at = models.DateTimeField(auto_now_add=True)  # Date d'ajout à la file d'attente

    class Meta:
        ordering = ['priority', 'added_at']  # Priorité, puis ordre d'ajout
        unique_together = ('user', 'content_type', 'object_id', 'start_time', 'end_time')

    def __str__(self):
        return f"File d'attente : {self.user} pour {self.resource} du {self.start_time} au {self.end_time}"

    @staticmethod
    def add_to_waitlist(user, resource, start_time, end_time):
        """Ajoute un utilisateur à la file d'attente pour une ressource donnée."""
        content_type = ContentType.objects.get_for_model(resource)
        
        # Vérifie si une entrée existe déjà
        if Waitlist.objects.filter(
            user=user,
            content_type=content_type,
            object_id=resource.id,
            start_time=start_time,
            end_time=end_time
        ).exists():
            raise ValueError("Vous êtes déjà dans la file d'attente pour cette ressource et période.")
        else:
            # Calcule la priorité basée sur le nombre existant dans la file d'attente
            priority = Waitlist.objects.filter(
                content_type=content_type,
                object_id=resource.id
            ).count() + 1
            
            # Crée l'entrée dans la file d'attente
            Waitlist.objects.create(
                user=user,
                content_type=content_type,
                object_id=resource.id,
                start_time=start_time,
                end_time=end_time,
                priority=priority
            )


    def promote(self):
        """Augmente la priorité dans la file d'attente."""
        if self.priority > 1:
            self.priority -= 1
            self.save()

    def remove_from_waitlist(self):
        """Supprime l'utilisateur de la file d'attente."""
        self.delete()