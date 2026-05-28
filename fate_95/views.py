from django.shortcuts import render, redirect
from .models import Question, Answer


element_riasec = {
    "feu": "E",        # Entreprenant
    "eau": "S",        # Social
    "vent": "A",       # Artistique
    "terre": "C",      # Conventionnel
    "ombre": "R",      # Réaliste
    "lumiere": "I"     # Investigateur
}

ELEMENT_THEMES = {
    "feu": {
        "name": "Feu",
        "body_class": "theme-feu",
        "title": "🔥 Royaume du Feu",
    },
    "eau": {
        "name": "Eau",
        "body_class": "theme-eau",
        "title": "💧 Royaume de l’Eau",
    },
    "vent": {
        "name": "Vent",
        "body_class": "theme-vent",
        "title": "🌪 Royaume du Vent",
    },
    "terre": {
        "name": "Terre",
        "body_class": "theme-terre",
        "title": "🌿 Royaume de la Terre",
    },
    "ombre": {
        "name": "Ombre",
        "body_class": "theme-ombre",
        "title": "🌑 Royaume de l’Ombre",
    },
    "lumiere": {
        "name": "Lumière",
        "body_class": "theme-lumiere",
        "title": "✨ Royaume de la Lumière",
    },
}

COLOR_THEMES = {
    "bleu": {
        "name": "Bleu",
        "body_class": "theme-bleu",
        "title": "🔵 Monde Bleu",
    },
    "jaune": {
        "name": "Jaune",
        "body_class": "theme-jaune",
        "title": "🟡 Monde Jaune",
    },
    "rouge": {
        "name": "Rouge",
        "body_class": "theme-rouge",
        "title": "🔴 Monde Rouge",
    },
    "noir": {
        "name": "Noir",
        "body_class": "theme-noir",
        "title": "⚫ Monde Noir",
    },
    "blanc": {
        "name": "Blanc",
        "body_class": "theme-blanc",
        "title": "⚪ Monde Blanc",
    },
}

SHAPE_THEMES = {
    "carre": {
        "name": "Carré",
        "body_class": "theme-carre",
        "title": "◼️ Monde du Carré",
    },
    "triangle": {
        "name": "Triangle",
        "body_class": "theme-triangle",
        "title": "🔺 Monde du Triangle",
    },
    "rectangle": {
        "name": "Rectangle",
        "body_class": "theme-rectangle",
        "title": "▭ Monde du Rectangle",
    },
    "cercle": {
        "name": "Cercle",
        "body_class": "theme-cercle",
        "title": "⚪ Monde du Cercle",
    },
    "losange": {
        "name": "Losange",
        "body_class": "theme-losange",
        "title": "🔷 Monde du Losange",
    },
    "parallelogramme": {
        "name": "Parallélogramme",
        "body_class": "theme-parallelogramme",
        "title": "▱ Monde du Parallélogramme",
    },
}
def get_element_theme(request):
    quest = request.session.get("quest")

    if quest == "painter":
        color = request.session.get("color")
        if color in COLOR_THEMES:
            return COLOR_THEMES[color]
        return COLOR_THEMES["bleu"]

    elif quest == "geometer":
        shape = request.session.get("shape")
        if shape in SHAPE_THEMES:
            return SHAPE_THEMES[shape]
        return SHAPE_THEMES["carre"]

    else:
        element = request.session.get("element")
        if element in ELEMENT_THEMES:
            return ELEMENT_THEMES[element]
        return ELEMENT_THEMES["lumiere"]
def ensure_session(request):
    if not request.session.session_key:
        request.session.create()

def home(request):
    theme = get_element_theme(request)
    return render(request, "home.html", {
        "theme": theme
    })


def quest_choice_view(request):
    theme = get_element_theme(request)
    return render(request, "quest_choice.html", {
        "theme": theme
    })


def gender_view(request):
    theme = get_element_theme(request)

    if request.method == "POST":
        request.session["gender"] = request.POST.get("gender")
        return redirect("register")

    return render(request, "gender.html", {
        "theme": theme
    })


def register_view(request):
    theme = get_element_theme(request)

    if request.method == "POST":
        request.session["firstname"] = request.POST.get("firstname")
        request.session["school_class"] = request.POST.get("school_class")
        request.session["password"] = request.POST.get("password")

        return redirect("quests")

    return render(request, "register.html", {
        "theme": theme
    })


def elemental_view(request):
    if request.method == "POST":

        if request.session.session_key:
            Answer.objects.filter(session_id=request.session.session_key).delete()

        request.session["quest"] = "elemental"
        request.session["element"] = request.POST.get("element")

        return redirect('element_intro')

    return render(request, "elemental.html")

def element_intro_view(request):
    element = request.session.get("element")
    theme = get_element_theme(request)

    element_data = {
        "feu": {
            "title": "🔥 Maître du Feu",
            "description": "Tu es puissant, déterminé et prêt à diriger.",
        },
        "eau": {
            "title": "💧 Esprit de l'Eau",
            "description": "Tu es calme, empathique et à l’écoute.",
        },
        "vent": {
            "title": "🌪️ Voyageur du Vent",
            "description": "Tu es libre, créatif et imprévisible.",
        },
        "terre": {
            "title": "🌱 Gardien de la Terre",
            "description": "Tu es stable, fiable et organisé.",
        },
        "ombre": {
            "title": "🌑 Maître de l'Ombre",
            "description": "Tu es mystérieux et stratégique.",
        },
        "lumiere": {
            "title": "💡 Porteur de Lumière",
            "description": "Tu es intelligent et guidé par la connaissance.",
        },
    }

    data = element_data.get(element)

    if not data:
        return redirect("elemental")

    return render(request, "element_intro.html", {
        "data": data,
        "theme": theme,
        "element": element,
    })

def game_view(request):
    ensure_session(request)

    theme = get_element_theme(request)
    quest = request.session.get("quest")

    if quest == "painter":
        color = request.session.get("color")

        if not color:
            return redirect("painter")

        questions = Question.objects.filter(element=color).order_by("id")
        quest_label = "Quête du Peintre"

    elif quest == "geometer":
        shape = request.session.get("shape")

        if not shape:
            return redirect("geometer")

        questions = Question.objects.filter(element=shape).order_by("id")
        quest_label = "Quête du Géomètre"

    else:
        element = request.session.get("element")

        if not element:
            return redirect("elemental")

        questions = Question.objects.filter(element=element).order_by("id")
        quest_label = "Quête Élémentaliste"

    if not questions.exists():
        return render(request, "fate_95.html", {
            "question": None,
            "theme": theme,
            "quest_label": quest_label,
            "message": "Aucune question n'est disponible pour cette quête."
        })

    answered_count = Answer.objects.filter(
        session_id=request.session.session_key
    ).count()

    if answered_count >= questions.count():
        return redirect("result")

    question = questions[answered_count]

    if request.method == "POST":
        selected_option = request.POST.get("choice")

        option_to_type = {
            "A": question.type_a,
            "B": question.type_b,
            "C": question.type_c,
            "D": question.type_d,
        }

        if selected_option in option_to_type:
            Answer.objects.create(
                session_id=request.session.session_key,
                question=question,
                selected_option=selected_option,
                riasec_type=option_to_type[selected_option]
            )

            return redirect("game")

    progress = int((answered_count / questions.count()) * 100)

    return render(request, "fate_95.html", {
        "question": question,
        "theme": theme,
        "quest_label": quest_label,
        "progress": progress,
        "current_index": answered_count + 1,
        "total_questions": questions.count(),
    })
    
def result_view(request):
    theme = get_element_theme(request)

    answers = Answer.objects.filter(session_id=request.session.session_key)

    scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}

    for answer in answers:
        scores[answer.riasec_type] += 1

    dominant = max(scores, key=scores.get) if answers.exists() else None

    descriptions = {
        "R": "Tu aimes le concret, l’action et les situations pratiques.",
        "I": "Tu aimes comprendre, analyser et résoudre des problèmes.",
        "A": "Tu aimes créer, imaginer et t’exprimer.",
        "S": "Tu aimes aider, écouter et travailler avec les autres.",
        "E": "Tu aimes diriger, convaincre et entreprendre.",
        "C": "Tu aimes organiser, structurer et travailler avec précision."
    }

    jobs = {
        "R": ["Mécanicien", "Technicien", "Artisan", "Électricien"],
        "I": ["Ingénieur", "Chercheur", "Scientifique", "Data analyst"],
        "A": ["Graphiste", "Designer", "Musicien", "Réalisateur"],
        "S": ["Professeur", "Infirmier", "Psychologue", "Éducateur"],
        "E": ["Entrepreneur", "Commercial", "Manager", "Chef de projet"],
        "C": ["Comptable", "Assistant administratif", "Gestionnaire", "Secrétaire"],
    }

    firstname = request.session.get("firstname", "")

    return render(request, "result.html", {
        "scores": scores,
        "dominant": dominant,
        "descriptions": descriptions,
        "jobs": jobs,
        "firstname": firstname,
        "theme": theme,
    })
    
def reset_game(request):
    if request.session.session_key:
        Answer.objects.filter(session_id=request.session.session_key).delete()

    for key in ["element", "color", "shape", "quest"]:
        if key in request.session:
            del request.session[key]

    return redirect("quests")

def painter_view(request):
    theme = get_element_theme(request)

    if request.method == "POST":
        if request.session.session_key:
            Answer.objects.filter(session_id=request.session.session_key).delete()

        request.session["quest"] = "painter"
        request.session["color"] = request.POST.get("color")

        if "element" in request.session:
            del request.session["element"]

        return redirect("painter_intro")

    return render(request, "painter.html", {
        "theme": theme
    })

def painter_intro_view(request):
    color = request.session.get("color")

    color_data = {
        "bleu": {
            "title": "🔵 Peintre du Bleu",
            "description": "Tu es calme, réfléchi et attiré par la compréhension."
        },
        "jaune": {
            "title": "🟡 Peintre du Jaune",
            "description": "Tu es curieux, lumineux et plein d’idées."
        },
        "rouge": {
            "title": "🔴 Peintre du Rouge",
            "description": "Tu es énergique, audacieux et prêt à agir."
        },
        "noir": {
            "title": "⚫ Peintre du Noir",
            "description": "Tu es stratégique, observateur et concentré."
        },
        "blanc": {
            "title": "⚪ Peintre du Blanc",
            "description": "Tu es organisé, précis et attentif aux détails."
        },
    }

    data = color_data.get(color)

    if not data:
        return redirect("painter")

    return render(request, "painter_intro.html", {
        "data": data,
        "color": color,
        "theme": get_element_theme(request),
    })
    
def geometer_view(request):
    theme = get_element_theme(request)

    if request.method == "POST":
        if request.session.session_key:
            Answer.objects.filter(session_id=request.session.session_key).delete()

        request.session["quest"] = "geometer"
        request.session["shape"] = request.POST.get("shape")

        if "element" in request.session:
            del request.session["element"]

        if "color" in request.session:
            del request.session["color"]

        return redirect("geometer_intro")

    return render(request, "geometer.html", {
        "theme": theme
    })


def geometer_intro_view(request):
    shape = request.session.get("shape")
    theme = get_element_theme(request)

    shape_data = {
        "carre": {
            "title": "◼️ Gardien du Carré",
            "description": "Tu recherches la stabilité, l’organisation et les repères clairs."
        },
        "triangle": {
            "title": "🔺 Esprit du Triangle",
            "description": "Tu es dynamique, ambitieux et tourné vers l’action."
        },
        "rectangle": {
            "title": "▭ Architecte du Rectangle",
            "description": "Tu aimes structurer, planifier et construire avec méthode."
        },
        "cercle": {
            "title": "⚪ Voyageur du Cercle",
            "description": "Tu valorises l’harmonie, les relations et l’équilibre."
        },
        "losange": {
            "title": "🔷 Créateur du Losange",
            "description": "Tu es original, créatif et tu aimes voir les choses autrement."
        },
        "parallelogramme": {
            "title": "▱ Stratège du Parallélogramme",
            "description": "Tu sais t’adapter, analyser et trouver des chemins différents."
        },
    }

    data = shape_data.get(shape)

    if not data:
        return redirect("geometer")

    return render(request, "geometer_intro.html", {
        "data": data,
        "shape": shape,
        "theme": theme,
    })