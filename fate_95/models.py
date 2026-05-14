from django.contrib.auth.models import User
from django.db import models


class AdminConfig(models.Model):
    openai_api_key = models.CharField(max_length=255, default='')
    openai_model = models.CharField(max_length=50, default='gpt-4.1')
    chatbot_prompt = models.TextField(default='')

    class Meta:
        verbose_name = "Configuration Admin"


class OrientationAdvice(models.Model):
    text = models.TextField()
    embedding = models.TextField(default='')  # JSON float array

    class Meta:
        verbose_name = "Conseil d'orientation"


class AdminAccount(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Compte admin"


class GameSession(models.Model):
    code = models.CharField(max_length=20, unique=True)
    label = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Session de jeu"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.label or self.code} ({'ouverte' if self.is_open else 'fermée'})"


class GameResult(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    game_session = models.ForeignKey(
        GameSession, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='results'
    )
    firstname = models.CharField(max_length=100, default='')
    school_class = models.CharField(max_length=20, default='')
    element = models.CharField(max_length=20, default='')
    quest = models.CharField(max_length=20, default='')
    dominant = models.CharField(max_length=1, default='')
    score_r = models.IntegerField(default=0)
    score_i = models.IntegerField(default=0)
    score_a = models.IntegerField(default=0)
    score_s = models.IntegerField(default=0)
    score_e = models.IntegerField(default=0)
    score_c = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Résultat de partie"


class RiasecCategory(models.Model):
    name = models.CharField(max_length=1)
    description = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):
    ELEMENT_CHOICES = [
        ("feu", "Feu"), ("eau", "Eau"), ("vent", "Vent"),
        ("terre", "Terre"), ("ombre", "Ombre"), ("lumiere", "Lumière"),
        ("bleu", "Bleu"), ("jaune", "Jaune"), ("rouge", "Rouge"),
        ("noir", "Noir"), ("blanc", "Blanc"),
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
