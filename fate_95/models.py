from django.contrib.auth.models import User
from django.db import models


class RiasecCategory(models.Model):
    name = models.CharField(max_length=1)
    description = models.TextField()

    def __str__(self):
        return self.name

class Question(models.Model):
    ELEMENT_CHOICES = [
        ("feu", "Feu"),
        ("eau", "Eau"),
        ("vent", "Vent"),
        ("terre", "Terre"),
        ("ombre", "Ombre"),
        ("lumiere", "Lumière"),
        
        ("bleu", "Bleu"),
        ("jaune", "Jaune"),
        ("rouge", "Rouge"),
        ("noir", "Noir"),
        ("blanc", "Blanc"),
        
        ("carre", "Carré"),
        ("triangle", "Triangle"),
        ("rectangle", "Rectangle"),
        ("cercle", "Cercle"),   
        ("losange", "Losange"),
        ("parallelogramme", "Parallélogramme"),
    ]

    element = models.CharField(max_length=20, choices=ELEMENT_CHOICES)
    text = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    type_a = models.CharField(max_length=1)
    type_b = models.CharField(max_length=1)
    type_c = models.CharField(max_length=1)
    type_d = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.element} - {self.text[:50]}"

class Answer(models.Model):
    session_id = models.CharField(max_length=100, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, null=True, blank=True)
    riasec_type = models.CharField(max_length=1, null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, null=True, blank=True)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    school_class = models.CharField(max_length=20, null=True, blank=True)
    element = models.CharField(max_length=20, null=True, blank=True)