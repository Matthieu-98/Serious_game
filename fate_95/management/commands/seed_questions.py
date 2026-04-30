from django.core.management.base import BaseCommand
from fate_95.models import Question


class Command(BaseCommand):
    help = "Insère les 30 questions RIASEC"

    def handle(self, *args, **kwargs):
        Question.objects.all().delete()

        questions = [

# 🔥 FEU
{
    "element": "feu",
    "text": "Tu dois organiser un projet de groupe :",
    "option_a": "Je prends la direction du groupe",
    "option_b": "J’analyse les meilleures solutions",
    "option_c": "Je propose des idées originales",
    "option_d": "Je m’assure que tout le monde participe",
    "type_a": "E", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "feu",
    "text": "On te donne un défi difficile :",
    "option_a": "Je fonce",
    "option_b": "J’analyse",
    "option_c": "Je crée une solution originale",
    "option_d": "Je demande de l’aide",
    "type_a": "E", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "feu",
    "text": "En équipe :",
    "option_a": "Je dirige",
    "option_b": "Je comprends",
    "option_c": "Je crée",
    "option_d": "Je soutiens",
    "type_a": "E", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "feu",
    "text": "Face à un problème :",
    "option_a": "Je décide vite",
    "option_b": "Je réfléchis",
    "option_c": "J’imagine",
    "option_d": "Je demande",
    "type_a": "E", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "feu",
    "text": "Tu préfères :",
    "option_a": "Diriger",
    "option_b": "Comprendre",
    "option_c": "Créer",
    "option_d": "Aider",
    "type_a": "E", "type_b": "I", "type_c": "A", "type_d": "S"
},

# 💧 EAU
{
    "element": "eau",
    "text": "Un ami a un problème :",
    "option_a": "Je conseille",
    "option_b": "J’analyse",
    "option_c": "Je divertis",
    "option_d": "J’écoute",
    "type_a": "E", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "eau",
    "text": "Tu préfères :",
    "option_a": "Motiver",
    "option_b": "Comprendre",
    "option_c": "Exprimer",
    "option_d": "Aider",
    "type_a": "E", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "eau",
    "text": "En groupe :",
    "option_a": "Je guide",
    "option_b": "J’observe",
    "option_c": "Je crée",
    "option_d": "Je soutiens",
    "type_a": "E", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "eau",
    "text": "Activité idéale :",
    "option_a": "Débattre",
    "option_b": "Étudier",
    "option_c": "Créer",
    "option_d": "Aider",
    "type_a": "E", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "eau",
    "text": "Tu es quelqu’un qui :",
    "option_a": "Influence",
    "option_b": "Analyse",
    "option_c": "Imagine",
    "option_d": "Comprend",
    "type_a": "E", "type_b": "I", "type_c": "A", "type_d": "S"
},

# 🌪️ VENT
{
    "element": "vent",
    "text": "Projet scolaire :",
    "option_a": "Organiser",
    "option_b": "Rechercher",
    "option_c": "Créer",
    "option_d": "Collaborer",
    "type_a": "C", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "vent",
    "text": "Tu préfères :",
    "option_a": "Structurer",
    "option_b": "Comprendre",
    "option_c": "Inventer",
    "option_d": "Aider",
    "type_a": "C", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "vent",
    "text": "Activité :",
    "option_a": "Ranger",
    "option_b": "Étudier",
    "option_c": "Dessiner",
    "option_d": "Collaborer",
    "type_a": "C", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "vent",
    "text": "Face à un problème :",
    "option_a": "Méthode",
    "option_b": "Analyse",
    "option_c": "Imagination",
    "option_d": "Aide",
    "type_a": "C", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "vent",
    "text": "Tu aimes :",
    "option_a": "Ordre",
    "option_b": "Idées",
    "option_c": "Création",
    "option_d": "Relations",
    "type_a": "C", "type_b": "I", "type_c": "A", "type_d": "S"
},

# 🌱 TERRE
{
    "element": "terre",
    "text": "Travail à faire :",
    "option_a": "Planifier",
    "option_b": "Comprendre",
    "option_c": "Créer",
    "option_d": "Aider",
    "type_a": "C", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "terre",
    "text": "Tu préfères :",
    "option_a": "Organisation",
    "option_b": "Réflexion",
    "option_c": "Imagination",
    "option_d": "Collaboration",
    "type_a": "C", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "terre",
    "text": "En groupe :",
    "option_a": "Organiser",
    "option_b": "Analyser",
    "option_c": "Innover",
    "option_d": "Soutenir",
    "type_a": "C", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "terre",
    "text": "Activité :",
    "option_a": "Classer",
    "option_b": "Étudier",
    "option_c": "Créer",
    "option_d": "Aider",
    "type_a": "C", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "terre",
    "text": "Tu es :",
    "option_a": "Méthodique",
    "option_b": "Curieux",
    "option_c": "Créatif",
    "option_d": "Sociable",
    "type_a": "C", "type_b": "I", "type_c": "A", "type_d": "S"
},

# 🌑 OMBRE
{
    "element": "ombre",
    "text": "Tu préfères :",
    "option_a": "Construire",
    "option_b": "Comprendre",
    "option_c": "Imaginer",
    "option_d": "Aider",
    "type_a": "R", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "ombre",
    "text": "Activité :",
    "option_a": "Réparer",
    "option_b": "Étudier",
    "option_c": "Créer",
    "option_d": "Aider",
    "type_a": "R", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "ombre",
    "text": "Projet :",
    "option_a": "Manipuler",
    "option_b": "Analyser",
    "option_c": "Inventer",
    "option_d": "Collaborer",
    "type_a": "R", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "ombre",
    "text": "Tu es :",
    "option_a": "Manuel",
    "option_b": "Logique",
    "option_c": "Créatif",
    "option_d": "Empathique",
    "type_a": "R", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "ombre",
    "text": "Tu aimes :",
    "option_a": "Concret",
    "option_b": "Comprendre",
    "option_c": "Imaginer",
    "option_d": "Aider",
    "type_a": "R", "type_b": "I", "type_c": "A", "type_d": "S"
},

# 💡 LUMIERE
{
    "element": "lumiere",
    "text": "Face à un problème :",
    "option_a": "Tester",
    "option_b": "Analyser",
    "option_c": "Imaginer",
    "option_d": "Demander",
    "type_a": "R", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "lumiere",
    "text": "Tu préfères :",
    "option_a": "Faire",
    "option_b": "Comprendre",
    "option_c": "Créer",
    "option_d": "Aider",
    "type_a": "R", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "lumiere",
    "text": "Activité :",
    "option_a": "Manipuler",
    "option_b": "Étudier",
    "option_c": "Créer",
    "option_d": "Collaborer",
    "type_a": "R", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "lumiere",
    "text": "Tu es :",
    "option_a": "Pratique",
    "option_b": "Curieux",
    "option_c": "Créatif",
    "option_d": "Sociable",
    "type_a": "R", "type_b": "I", "type_c": "A", "type_d": "S"
},
{
    "element": "lumiere",
    "text": "Tu aimes :",
    "option_a": "Construire",
    "option_b": "Apprendre",
    "option_c": "Imaginer",
    "option_d": "Aider",
    "type_a": "R", "type_b": "I", "type_c": "A", "type_d": "S"
},
        ]

        for q in questions:
            Question.objects.create(**q)

        self.stdout.write(self.style.SUCCESS("✅ 30 questions ajoutées !"))