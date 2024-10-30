# from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
# class Personne(models.Model):
#     nom = models.CharField(max_length=100)
#     prenom = models.CharField(max_length=100)
#     date_naissance = models.DateField()
#     email = models.EmailField(unique=True)

#     class Meta:
#         abstract = True

#     def __str__(self):
#         return f"{self.prenom} {self.nom}"


# class Etudiant(Personne):
#     niveau_etude = models.CharField(max_length=50)
#     numero_etudiant = models.CharField(max_length=20, unique=True)

#     def __str__(self):
#         return f"Étudiant : {self.prenom} {self.nom}, Niveau : {self.niveau_etude}"


# class Professeur(Personne):
#     departement = models.CharField(max_length=100)
#     date_embauche = models.DateField()

#     def __str__(self):
#         return f"Professeur : {self.prenom} {self.nom}, Département : {self.departement}"


# class Administrateur(Personne):
#     niveau_acces = models.CharField(max_length=50)

#     def __str__(self):
#         return f"Administrateur : {self.prenom} {self.nom}, Niveau d'accès : {self.niveau_acces}"


# class Cours(models.Model):
#     nom_cours = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
#     etudiants = models.ManyToManyField(Etudiant, related_name='cours')

#     def __str__(self):
#         return self.nom_cours


# class Contact(models.Model):
#     personne = models.ForeignKey(Personne, on_delete=models.CASCADE)
#     numero_telephone = models.CharField(max_length=15, blank=True)
#     adresse = models.CharField(max_length=255, blank=True)

#     def __str__(self):
#         return f"Contact de {self.personne} - Tel: {self.numero_telephone}"
# from django.db import models

# class Personne(models.Model):
#     nom = models.CharField(max_length=100)
#     prenom = models.CharField(max_length=100)
#     date_naissance = models.DateField()
#     email = models.EmailField(unique=True)

#     class Meta:
#         abstract = True

#     def __str__(self):
#         return f"{self.prenom} {self.nom}"


# class Etudiant(Personne):
#     niveau_etude = models.CharField(max_length=50)
#     numero_etudiant = models.CharField(max_length=20, unique=True)

#     def __str__(self):
#         return f"Étudiant : {self.prenom} {self.nom}, Niveau : {self.niveau_etude}"


# class Professeur(Personne):
#     departement = models.CharField(max_length=100)
#     date_embauche = models.DateField()

#     def __str__(self):
#         return f"Professeur : {self.prenom} {self.nom}, Département : {self.departement}"


# class Administrateur(Personne):
#     niveau_acces = models.CharField(max_length=50)

#     def __str__(self):
#         return f"Administrateur : {self.prenom} {self.nom}, Niveau d'accès : {self.niveau_acces}"


# class Cours(models.Model):
#     nom_cours = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
#     etudiants = models.ManyToManyField(Etudiant, related_name='cours')

#     def __str__(self):
#         return self.nom_cours


# class Contact(models.Model):
   
#     numero_telephone = models.CharField(max_length=15, blank=True)
#     adresse = models.CharField(max_length=255, blank=True)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     personne = GenericForeignKey('content_type', 'object_id')
#     def __str__(self):
#         return f"Contact de {self.personne} - Tel: {self.numero_telephone}"
