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

# 🔵 BLEU
{
    "element": "bleu",
    "text": "Face à un problème compliqué :",
    "option_a": "Je cherche une solution logique",
    "option_b": "J’écoute les autres",
    "option_c": "Je propose une idée créative",
    "option_d": "Je garde une méthode organisée",
    "type_a": "I", "type_b": "S", "type_c": "A", "type_d": "C"
},
{
    "element": "bleu",
    "text": "Quand je travaille :",
    "option_a": "Je comprends en profondeur",
    "option_b": "J’aide mon groupe",
    "option_c": "Je crée une présentation",
    "option_d": "Je suis un plan",
    "type_a": "I", "type_b": "S", "type_c": "A", "type_d": "C"
},
{
    "element": "bleu",
    "text": "Dans un projet :",
    "option_a": "J’analyse",
    "option_b": "Je rassure",
    "option_c": "Je crée",
    "option_d": "J’organise",
    "type_a": "I", "type_b": "S", "type_c": "A", "type_d": "C"
},
{
    "element": "bleu",
    "text": "Ce qui me motive :",
    "option_a": "Apprendre",
    "option_b": "Aider",
    "option_c": "Exprimer",
    "option_d": "Bien faire",
    "type_a": "I", "type_b": "S", "type_c": "A", "type_d": "C"
},
{
    "element": "bleu",
    "text": "Je préfère :",
    "option_a": "Résoudre",
    "option_b": "Aider",
    "option_c": "Créer",
    "option_d": "Organiser",
    "type_a": "I", "type_b": "S", "type_c": "A", "type_d": "C"
},

# 🟡 JAUNE
{
    "element": "jaune",
    "text": "Dans une activité créative :",
    "option_a": "J’invente",
    "option_b": "Je motive",
    "option_c": "Je comprends",
    "option_d": "J’aide",
    "type_a": "A", "type_b": "E", "type_c": "I", "type_d": "S"
},
{
    "element": "jaune",
    "text": "En groupe :",
    "option_a": "Je propose",
    "option_b": "Je parle",
    "option_c": "J’analyse",
    "option_d": "Je soutiens",
    "type_a": "A", "type_b": "E", "type_c": "I", "type_d": "S"
},
{
    "element": "jaune",
    "text": "Quand je découvre :",
    "option_a": "J’imagine",
    "option_b": "Je présente",
    "option_c": "Je comprends",
    "option_d": "Je partage",
    "type_a": "A", "type_b": "E", "type_c": "I", "type_d": "S"
},
{
    "element": "jaune",
    "text": "Je suis à l’aise pour :",
    "option_a": "Créer",
    "option_b": "Convaincre",
    "option_c": "Comprendre",
    "option_d": "Aider",
    "type_a": "A", "type_b": "E", "type_c": "I", "type_d": "S"
},
{
    "element": "jaune",
    "text": "Dans un projet :",
    "option_a": "Rendre original",
    "option_b": "Défendre",
    "option_c": "Chercher",
    "option_d": "Aider",
    "type_a": "A", "type_b": "E", "type_c": "I", "type_d": "S"
},

# 🔴 ROUGE
{
    "element": "rouge",
    "text": "Face à un défi :",
    "option_a": "Je dirige",
    "option_b": "Je fais",
    "option_c": "J’analyse",
    "option_d": "Je motive",
    "type_a": "E", "type_b": "R", "type_c": "I", "type_d": "S"
},
{
    "element": "rouge",
    "text": "Dans un groupe :",
    "option_a": "Je dirige",
    "option_b": "Je fais",
    "option_c": "J’analyse",
    "option_d": "Je soutiens",
    "type_a": "E", "type_b": "R", "type_c": "I", "type_d": "S"
},
{
    "element": "rouge",
    "text": "Quand il faut agir :",
    "option_a": "Je décide",
    "option_b": "Je fais",
    "option_c": "Je réfléchis",
    "option_d": "Je demande",
    "type_a": "E", "type_b": "R", "type_c": "I", "type_d": "S"
},
{
    "element": "rouge",
    "text": "Je préfère :",
    "option_a": "Responsabilité",
    "option_b": "Concret",
    "option_c": "Analyse",
    "option_d": "Équipe",
    "type_a": "E", "type_b": "R", "type_c": "I", "type_d": "S"
},
{
    "element": "rouge",
    "text": "Pour réussir :",
    "option_a": "Diriger",
    "option_b": "Faire",
    "option_c": "Comprendre",
    "option_d": "Motiver",
    "type_a": "E", "type_b": "R", "type_c": "I", "type_d": "S"
},

# ⚫ NOIR
{
    "element": "noir",
    "text": "Situation difficile :",
    "option_a": "Observer",
    "option_b": "Organiser",
    "option_c": "Tester",
    "option_d": "Imaginer",
    "type_a": "I", "type_b": "C", "type_c": "R", "type_d": "A"
},
{
    "element": "noir",
    "text": "Seul :",
    "option_a": "Analyser",
    "option_b": "Méthode",
    "option_c": "Manipuler",
    "option_d": "Créer",
    "type_a": "I", "type_b": "C", "type_c": "R", "type_d": "A"
},
{
    "element": "noir",
    "text": "Mystère :",
    "option_a": "Indices",
    "option_b": "Classer",
    "option_c": "Tester",
    "option_d": "Imaginer",
    "type_a": "I", "type_b": "C", "type_c": "R", "type_d": "A"
},
{
    "element": "noir",
    "text": "Tu es :",
    "option_a": "Observateur",
    "option_b": "Rigoureux",
    "option_c": "Pratique",
    "option_d": "Original",
    "type_a": "I", "type_b": "C", "type_c": "R", "type_d": "A"
},
{
    "element": "noir",
    "text": "Mission :",
    "option_a": "Stratégie",
    "option_b": "Étapes",
    "option_c": "Action",
    "option_d": "Créatif",
    "type_a": "I", "type_b": "C", "type_c": "R", "type_d": "A"
},

# ⚪ BLANC
{
    "element": "blanc",
    "text": "Commencer :",
    "option_a": "Planifier",
    "option_b": "Comprendre",
    "option_c": "Aider",
    "option_d": "Créer",
    "type_a": "C", "type_b": "I", "type_c": "S", "type_d": "A"
},
{
    "element": "blanc",
    "text": "Réussir :",
    "option_a": "Consignes",
    "option_b": "Analyse",
    "option_c": "Équipe",
    "option_d": "Créatif",
    "type_a": "C", "type_b": "I", "type_c": "S", "type_d": "A"
},
{
    "element": "blanc",
    "text": "Préférence :",
    "option_a": "Organiser",
    "option_b": "Comprendre",
    "option_c": "Aider",
    "option_d": "Imaginer",
    "type_a": "C", "type_b": "I", "type_c": "S", "type_d": "A"
},
{
    "element": "blanc",
    "text": "Projet :",
    "option_a": "Vérifier",
    "option_b": "Analyser",
    "option_c": "Coopérer",
    "option_d": "Créer",
    "type_a": "C", "type_b": "I", "type_c": "S", "type_d": "A"
},
{
    "element": "blanc",
    "text": "Tu es :",
    "option_a": "Précis",
    "option_b": "Réfléchi",
    "option_c": "Sociable",
    "option_d": "Créatif",
    "type_a": "C", "type_b": "I", "type_c": "S", "type_d": "A"
},
        ]

        for q in questions:
            Question.objects.create(**q)

        self.stdout.write(self.style.SUCCESS("✅ 30 questions ajoutées !"))