from django.db import models

# ============================================
# MODÈLE PERSON (Classe parent)
# ============================================
class Person(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=32)
    date_naissance = models.DateField()
    email = models.EmailField(unique=True)  # unique=True pour éviter les doublons
    tlf = models.CharField(max_length=20)
    password = models.CharField(max_length=32)
    
    # Relation Many-to-Many : Amis (une personne peut avoir plusieurs amis)
    amis = models.ManyToManyField('self', blank=True)
    
    # Relation Many-to-One : Une personne appartient à une faculté
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


# ============================================
# MODÈLE STUDENT (Hérite de Person)
# ============================================
class Student(Person):
    annee = models.IntegerField()
    cursus = models.ForeignKey('Cursus', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.prenom} {self.nom} - Année {self.annee}"


# ============================================
# MODÈLE EMPLOYEE (Hérite de Person)
# ============================================
class Employee(Person):
    office = models.CharField(max_length=32)
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.job}"


# ============================================
# MODÈLE FACULTY
# ============================================
class Faculty(models.Model):
    nom = models.CharField(max_length=32)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name_plural = "Faculties"


# ============================================
# MODÈLE CURSUS
# ============================================
class Cursus(models.Model):
    titre = models.CharField(max_length=32)
    
    def __str__(self):
        return self.titre
    
    class Meta:
        verbose_name_plural = "Cursus"


# ============================================
# MODÈLE JOB
# ============================================
class Job(models.Model):
    titre = models.CharField(max_length=32)
    
    def __str__(self):
        return self.titre
    
    class Meta:
        verbose_name_plural = "Jobs"


# ============================================
# MODÈLE CAMPUS
# ============================================
class Campus(models.Model):
    nom = models.CharField(max_length=32)
    adresse = models.CharField(max_length=60)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name_plural = "Campus"


# ============================================
# MODÈLE MESSAGE
# ============================================
class Message(models.Model):
    contenu = models.TextField()
    date_publication = models.DateTimeField(
        auto_now_add=True, 
        auto_now=False,
        verbose_name="Date de publication"
    )
    auteur = models.ForeignKey('Person', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Message de {self.auteur} - {self.date_publication.strftime('%d/%m/%Y')}"
    
    class Meta:
        ordering = ['-date_publication']  # Messages les plus récents en premier