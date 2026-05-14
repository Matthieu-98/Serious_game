import json
import math
import secrets
import urllib.request
import urllib.error

from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import (
    AdminAccount, AdminConfig, Answer, GameResult, GameSession,
    OrientationAdvice, Question,
)

ELEMENT_THEMES = {
    "feu":    {"name": "Feu",     "body_class": "theme-feu",    "title": "🔥 Royaume du Feu"},
    "eau":    {"name": "Eau",     "body_class": "theme-eau",    "title": "💧 Royaume de l'Eau"},
    "vent":   {"name": "Vent",    "body_class": "theme-vent",   "title": "🌪 Royaume du Vent"},
    "terre":  {"name": "Terre",   "body_class": "theme-terre",  "title": "🌿 Royaume de la Terre"},
    "ombre":  {"name": "Ombre",   "body_class": "theme-ombre",  "title": "🌑 Royaume de l'Ombre"},
    "lumiere":{"name": "Lumière", "body_class": "theme-lumiere","title": "✨ Royaume de la Lumière"},
}

COLOR_THEMES = {
    "bleu":  {"name": "Bleu",  "body_class": "theme-bleu",  "title": "🔵 Monde Bleu"},
    "jaune": {"name": "Jaune", "body_class": "theme-jaune", "title": "🟡 Monde Jaune"},
    "rouge": {"name": "Rouge", "body_class": "theme-rouge", "title": "🔴 Monde Rouge"},
    "noir":  {"name": "Noir",  "body_class": "theme-noir",  "title": "⚫ Monde Noir"},
    "blanc": {"name": "Blanc", "body_class": "theme-blanc", "title": "⚪ Monde Blanc"},
}

RIASEC_NAMES = {
    "R": "Réaliste", "I": "Investigateur", "A": "Artistique",
    "S": "Social", "E": "Entreprenant", "C": "Conventionnel",
}

ELEMENT_CHOICES = [
    ("feu","Feu"),("eau","Eau"),("vent","Vent"),("terre","Terre"),("ombre","Ombre"),("lumiere","Lumière"),
    ("bleu","Bleu"),("jaune","Jaune"),("rouge","Rouge"),("noir","Noir"),("blanc","Blanc"),
]

OPENAI_MODELS = ['gpt-4.1', 'gpt-4.1-mini', 'gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo']

DEFAULT_CHATBOT_PROMPT = (
    "Propose toujours au moins une formation concrète (BTS, BUT, licence, école spécialisée) "
    "adaptée au profil RIASEC de l'élève. "
    "Si sa demande est vague, pose-lui une question de relance pour mieux cerner ses aspirations. "
    "Commence par valoriser un point fort de son profil dominant avant de suggérer des pistes. "
    "Reste positif, concret et adapté au niveau lycéen."
)


# ── KNN / MiniLM ─────────────────────────────────────────────────────────────

_embedder = None


def _get_embedder():
    global _embedder
    if _embedder is None:
        try:
            from sentence_transformers import SentenceTransformer
            _embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        except Exception:
            _embedder = False
    return _embedder if _embedder is not False else None


def _embed(text):
    model = _get_embedder()
    if model is None:
        return None
    return model.encode([text])[0].tolist()


def _cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


def _knn_advice(query, k=3):
    advices = list(OrientationAdvice.objects.all())
    if not advices:
        return []
    query_emb = _embed(query)
    if query_emb is None:
        return [a.text for a in advices[:k]]
    scored = []
    for adv in advices:
        if adv.embedding:
            try:
                emb = json.loads(adv.embedding)
                if emb:
                    scored.append((_cosine(query_emb, emb), adv.text))
            except (json.JSONDecodeError, TypeError):
                pass
    scored.sort(key=lambda x: -x[0])
    return [text for _, text in scored[:k]]


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_element_theme(request):
    quest = request.session.get("quest")
    if quest == "painter":
        color = request.session.get("color", "bleu")
        return COLOR_THEMES.get(color, COLOR_THEMES["bleu"])
    element = request.session.get("element", "lumiere")
    return ELEMENT_THEMES.get(element, ELEMENT_THEMES["lumiere"])


def ensure_session(request):
    if not request.session.session_key:
        request.session.create()


# ── Landing (code de session) ─────────────────────────────────────────────────

def landing_view(request):
    error = None
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        if code:
            try:
                gs = GameSession.objects.get(code=code, is_open=True)
                request.session['game_session_code'] = gs.code
                return redirect('home')
            except GameSession.DoesNotExist:
                error = "Code invalide ou session non ouverte."
        else:
            return redirect('home')
    return render(request, 'landing.html', {'error': error})


# ── Jeu ──────────────────────────────────────────────────────────────────────

def home(request):
    return render(request, "home.html", {"theme": get_element_theme(request)})


def quest_choice_view(request):
    return render(request, "quest_choice.html", {"theme": get_element_theme(request)})


def gender_view(request):
    theme = get_element_theme(request)
    if request.method == "POST":
        request.session["gender"] = request.POST.get("gender")
        return redirect("register")
    return render(request, "gender.html", {"theme": theme})


def register_view(request):
    theme = get_element_theme(request)
    if request.method == "POST":
        request.session["firstname"] = request.POST.get("firstname")
        request.session["school_class"] = request.POST.get("school_class")
        request.session["password"] = request.POST.get("password")
        return redirect("quests")
    return render(request, "register.html", {"theme": theme})


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
        "feu":    {"title": "🔥 Maître du Feu",      "description": "Tu es puissant, déterminé et prêt à diriger."},
        "eau":    {"title": "💧 Esprit de l'Eau",     "description": "Tu es calme, empathique et à l'écoute."},
        "vent":   {"title": "🌪️ Voyageur du Vent",   "description": "Tu es libre, créatif et imprévisible."},
        "terre":  {"title": "🌱 Gardien de la Terre", "description": "Tu es stable, fiable et organisé."},
        "ombre":  {"title": "🌑 Maître de l'Ombre",  "description": "Tu es mystérieux et stratégique."},
        "lumiere":{"title": "💡 Porteur de Lumière",  "description": "Tu es intelligent et guidé par la connaissance."},
    }
    data = element_data.get(element)
    if not data:
        return redirect("elemental")
    return render(request, "element_intro.html", {"data": data, "theme": theme, "element": element})


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
    else:
        element = request.session.get("element")
        if not element:
            return redirect("elemental")
        questions = Question.objects.filter(element=element).order_by("id")
        quest_label = "Quête Élémentaliste"

    if not questions.exists():
        return render(request, "fate_95.html", {
            "question": None, "theme": theme, "quest_label": quest_label,
            "message": "Aucune question n'est disponible pour cette quête."
        })

    answered_count = Answer.objects.filter(session_id=request.session.session_key).count()
    if answered_count >= questions.count():
        return redirect("result")

    question = questions[answered_count]

    if request.method == "POST":
        selected_option = request.POST.get("choice")
        option_to_type = {
            "A": question.type_a, "B": question.type_b,
            "C": question.type_c, "D": question.type_d,
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
        "question": question, "theme": theme, "quest_label": quest_label,
        "progress": progress, "current_index": answered_count + 1,
        "total_questions": questions.count(),
    })


def result_view(request):
    theme = get_element_theme(request)
    answers = Answer.objects.filter(session_id=request.session.session_key)

    scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    for answer in answers:
        if answer.riasec_type in scores:
            scores[answer.riasec_type] += 1

    dominant = max(scores, key=scores.get) if answers.exists() else None

    descriptions = {
        "R": "Tu aimes le concret, l'action et les situations pratiques.",
        "I": "Tu aimes comprendre, analyser et résoudre des problèmes.",
        "A": "Tu aimes créer, imaginer et t'exprimer.",
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

    if request.session.session_key and dominant:
        gs = None
        code = request.session.get('game_session_code')
        if code:
            gs = GameSession.objects.filter(code=code).first()
        if not gs:
            gs = GameSession.objects.filter(is_open=True).order_by('-created_at').first()

        GameResult.objects.update_or_create(
            session_id=request.session.session_key,
            defaults={
                'game_session': gs,
                'firstname': firstname,
                'school_class': request.session.get('school_class', ''),
                'element': request.session.get('element') or request.session.get('color', ''),
                'quest': request.session.get('quest', ''),
                'dominant': dominant,
                'score_r': scores['R'], 'score_i': scores['I'], 'score_a': scores['A'],
                'score_s': scores['S'], 'score_e': scores['E'], 'score_c': scores['C'],
            }
        )

    return render(request, "result.html", {
        "scores": scores, "dominant": dominant, "descriptions": descriptions,
        "jobs": jobs, "firstname": firstname, "theme": theme,
    })


def reset_game(request):
    if request.session.session_key:
        Answer.objects.filter(session_id=request.session.session_key).delete()
    for key in ["element"]:
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
    return render(request, "painter.html", {"theme": theme})


def painter_intro_view(request):
    color = request.session.get("color")
    color_data = {
        "bleu":  {"title": "🔵 Peintre du Bleu",  "description": "Tu es calme, réfléchi et attiré par la compréhension."},
        "jaune": {"title": "🟡 Peintre du Jaune", "description": "Tu es curieux, lumineux et plein d'idées."},
        "rouge": {"title": "🔴 Peintre du Rouge", "description": "Tu es énergique, audacieux et prêt à agir."},
        "noir":  {"title": "⚫ Peintre du Noir",  "description": "Tu es stratégique, observateur et concentré."},
        "blanc": {"title": "⚪ Peintre du Blanc", "description": "Tu es organisé, précis et attentif aux détails."},
    }
    data = color_data.get(color)
    if not data:
        return redirect("painter")
    return render(request, "painter_intro.html", {"data": data, "color": color, "theme": get_element_theme(request)})


# ── Chatbot ──────────────────────────────────────────────────────────────────

@require_POST
def chatbot_view(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if not user_message:
        return JsonResponse({'error': 'Empty message'}, status=400)

    config = AdminConfig.objects.first()
    api_key = config.openai_api_key.strip() if config else ''

    if not api_key:
        return JsonResponse({'reply': "Le chatbot n'est pas encore configuré (clef API manquante)."})

    # RIASEC context from session
    answers = Answer.objects.filter(session_id=request.session.session_key)
    scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    for answer in answers:
        if answer.riasec_type in scores:
            scores[answer.riasec_type] += 1
    dominant = max(scores, key=scores.get) if answers.exists() else "inconnu"

    firstname    = request.session.get('firstname', '')
    school_class = request.session.get('school_class', '')
    quest        = request.session.get('quest', '')
    element      = request.session.get('element') or request.session.get('color', '')

    scores_str = ", ".join(f"{RIASEC_NAMES[k]}={v}" for k, v in scores.items())

    # KNN : conseils pertinents
    relevant = _knn_advice(user_message, k=3)
    advice_block = ""
    if relevant:
        advice_block = "\n\nConseils d'orientation à utiliser si pertinents :\n" + "\n".join(f"- {t}" for t in relevant)

    # Custom prompt suffix
    extra = config.chatbot_prompt.strip() if config and config.chatbot_prompt else ""

    system_prompt = (
        f"Tu es un conseiller d'orientation bienveillant pour lycéens. "
        f"L'élève vient de terminer le serious game FATE_95. Voici son profil :\n"
        f"- Type RIASEC dominant : {dominant} ({RIASEC_NAMES.get(dominant, '')})\n"
        f"- Scores : {scores_str}\n"
        f"- Quête choisie : {quest} / {element}\n"
        + (f"- Prénom : {firstname}\n" if firstname else "")
        + (f"- Classe : {school_class}\n" if school_class else "")
        + f"\nAide l'élève à s'orienter en te basant sur ces données. "
        f"Sois concis (2-3 phrases max), encourageant, réponds uniquement en français."
        + advice_block
        + (f"\n\nInstructions supplémentaires : {extra}" if extra else "")
    )

    model = config.openai_model.strip() if config and config.openai_model else 'gpt-4.1'

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        "max_tokens": 300,
        "temperature": 0.7,
    }).encode('utf-8')

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return JsonResponse({'reply': result['choices'][0]['message']['content']})
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode('utf-8'))
            msg = body.get('error', {}).get('message', f'HTTP {e.code}')
        except Exception:
            msg = f'HTTP {e.code}'
        return JsonResponse({'reply': f"Erreur OpenAI : {msg}"})
    except Exception as e:
        return JsonResponse({'reply': f"Erreur de connexion : {e}"})


# ── Admin helpers ─────────────────────────────────────────────────────────────

def _ensure_default_admin():
    if not AdminAccount.objects.exists():
        AdminAccount.objects.create(username='admin', password=make_password('password'))


def _admin_required(view_fn):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_logged_in') or not request.session.get('admin_username'):
            return redirect('admin_login')
        return view_fn(request, *args, **kwargs)
    wrapper.__name__ = view_fn.__name__
    return wrapper


def admin_login_view(request):
    _ensure_default_admin()
    if request.session.get('admin_logged_in') and request.session.get('admin_username'):
        return redirect('admin_panel')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not username or not password:
            error = "Identifiant et mot de passe requis."
        else:
            try:
                account = AdminAccount.objects.get(username=username)
                if check_password(password, account.password):
                    request.session['admin_logged_in'] = True
                    request.session['admin_username'] = account.username
                    return redirect('admin_panel')
                else:
                    error = "Identifiants incorrects."
            except AdminAccount.DoesNotExist:
                error = "Identifiants incorrects."
    return render(request, 'admin_login.html', {'error': error})


def admin_logout_view(request):
    request.session.pop('admin_logged_in', None)
    request.session.pop('admin_username', None)
    return redirect('admin_login')


# ── Admin — Dashboard ─────────────────────────────────────────────────────────

@_admin_required
def admin_panel_view(request):
    config, _ = AdminConfig.objects.get_or_create(id=1, defaults={'chatbot_prompt': DEFAULT_CHATBOT_PROMPT})
    message = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_apikey':
            new_key = request.POST.get('api_key', '').strip()
            if new_key:
                config.openai_api_key = new_key
                config.save()
                message = "Clef API mise à jour."
            else:
                message = "Champ vide — clef inchangée."

        elif action == 'update_model':
            new_model = request.POST.get('model', '').strip()
            if new_model:
                config.openai_model = new_model
                config.save()
                message = f"Modèle mis à jour : {new_model}"

        elif action == 'test_api':
            api_key = config.openai_api_key.strip()
            model = config.openai_model.strip() or 'gpt-4.1'
            if not api_key:
                message = "⚠ Aucune clef API configurée."
            else:
                payload = json.dumps({
                    "model": model,
                    "messages": [{"role": "user", "content": "dis juste OK"}],
                    "max_tokens": 5,
                }).encode('utf-8')
                req = urllib.request.Request(
                    "https://api.openai.com/v1/chat/completions",
                    data=payload,
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                    method="POST",
                )
                try:
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        json.loads(resp.read().decode('utf-8'))
                        message = f"✓ Clef et modèle ({model}) fonctionnels !"
                except urllib.error.HTTPError as e:
                    try:
                        body = json.loads(e.read().decode('utf-8'))
                        msg = body.get('error', {}).get('message', f'HTTP {e.code}')
                    except Exception:
                        msg = f'HTTP {e.code}'
                    message = f"✗ Erreur OpenAI : {msg}"
                except Exception as e:
                    message = f"✗ Erreur réseau : {e}"

        elif action == 'new_session':
            label = request.POST.get('label', '').strip()
            code = secrets.token_hex(3).upper()
            GameSession.objects.create(code=code, label=label, is_open=True)
            message = f"Session créée — code : {code}"

        elif action == 'toggle_session':
            sid = request.POST.get('session_id')
            try:
                gs = GameSession.objects.get(id=sid)
                gs.is_open = not gs.is_open
                gs.save()
                message = f"Session {gs.code} {'ouverte' if gs.is_open else 'fermée'}."
            except GameSession.DoesNotExist:
                pass

        elif action == 'delete_session':
            sid = request.POST.get('session_id')
            try:
                GameSession.objects.get(id=sid).delete()
                message = "Session supprimée."
            except GameSession.DoesNotExist:
                pass

        elif action == 'add_admin':
            username = request.POST.get('new_username', '').strip()
            password = request.POST.get('new_password', '')
            if username and len(password) >= 4:
                if AdminAccount.objects.filter(username=username).exists():
                    message = f"Le compte « {username} » existe déjà."
                else:
                    AdminAccount.objects.create(username=username, password=make_password(password))
                    message = f"Compte « {username} » créé."
            else:
                message = "Nom d'utilisateur et mot de passe (4 car. min) requis."

        elif action == 'delete_admin':
            aid = request.POST.get('admin_id')
            current = request.session.get('admin_username')
            try:
                acc = AdminAccount.objects.get(id=aid)
                if acc.username == current:
                    message = "Vous ne pouvez pas supprimer votre propre compte."
                elif AdminAccount.objects.count() <= 1:
                    message = "Impossible de supprimer le dernier compte admin."
                else:
                    acc.delete()
                    message = "Compte supprimé."
            except AdminAccount.DoesNotExist:
                pass

    sessions = GameSession.objects.all()
    admins = AdminAccount.objects.all()

    return render(request, 'admin.html', {
        'config': config,
        'sessions': sessions,
        'admins': admins,
        'message': message,
        'current_user': request.session.get('admin_username'),
        'openai_models': OPENAI_MODELS,
        'active_tab': 'dashboard',
    })


# ── Admin — Conseils ──────────────────────────────────────────────────────────

@_admin_required
def admin_conseils_view(request):
    config, _ = AdminConfig.objects.get_or_create(id=1, defaults={'chatbot_prompt': DEFAULT_CHATBOT_PROMPT})
    message = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_advice':
            text = request.POST.get('text', '').strip()
            if text:
                adv = OrientationAdvice.objects.create(text=text)
                emb = _embed(text)
                if emb is not None:
                    adv.embedding = json.dumps(emb)
                    adv.save()
                message = "Conseil ajouté."
            else:
                message = "Texte vide."

        elif action == 'edit_advice':
            aid = request.POST.get('advice_id')
            text = request.POST.get('text', '').strip()
            if text:
                try:
                    adv = OrientationAdvice.objects.get(id=aid)
                    adv.text = text
                    emb = _embed(text)
                    if emb is not None:
                        adv.embedding = json.dumps(emb)
                    adv.save()
                    message = "Conseil mis à jour."
                except OrientationAdvice.DoesNotExist:
                    message = "Conseil introuvable."
            else:
                message = "Texte vide."

        elif action == 'delete_advice':
            aid = request.POST.get('advice_id')
            OrientationAdvice.objects.filter(id=aid).delete()
            message = "Conseil supprimé."

        elif action == 'reembed_all':
            count = 0
            for adv in OrientationAdvice.objects.all():
                emb = _embed(adv.text)
                if emb is not None:
                    adv.embedding = json.dumps(emb)
                    adv.save()
                    count += 1
            if count > 0:
                message = f"Embeddings recalculés pour {count} conseils."
            else:
                message = "⚠ Modèle MiniLM non disponible (installe sentence-transformers)."

        elif action == 'update_prompt':
            config.chatbot_prompt = request.POST.get('prompt', '').strip()
            config.save()
            message = "Prompt mis à jour."

    advices = OrientationAdvice.objects.all()
    embedder_ok = _get_embedder() is not None

    return render(request, 'admin_conseils.html', {
        'advices': advices,
        'config': config,
        'message': message,
        'embedder_ok': embedder_ok,
        'current_user': request.session.get('admin_username'),
        'active_tab': 'conseils',
    })


# ── Admin — Questions RIASEC ──────────────────────────────────────────────────

@_admin_required
def admin_questions_view(request):
    message = None
    element_filter = request.GET.get('element', '')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            element = request.POST.get('element', '').strip()
            text = request.POST.get('text', '').strip()
            opts = [request.POST.get(f'option_{x}', '').strip() for x in 'abcd']
            types = [request.POST.get(f'type_{x}', '').strip().upper() for x in 'abcd']
            if element and text and all(opts) and all(t in 'RIASEC' for t in types):
                Question.objects.create(
                    element=element, text=text,
                    option_a=opts[0], option_b=opts[1], option_c=opts[2], option_d=opts[3],
                    type_a=types[0], type_b=types[1], type_c=types[2], type_d=types[3],
                )
                message = "Question ajoutée."
            else:
                message = "Données invalides (types doivent être parmi R,I,A,S,E,C)."

        elif action == 'delete':
            qid = request.POST.get('question_id')
            Question.objects.filter(id=qid).delete()
            message = "Question supprimée."

        elif action == 'edit':
            qid = request.POST.get('question_id')
            try:
                q = Question.objects.get(id=qid)
                q.text = request.POST.get('text', q.text).strip()
                for x, attr in zip('abcd', ['a','b','c','d']):
                    opt = request.POST.get(f'option_{x}', '').strip()
                    typ = request.POST.get(f'type_{x}', '').strip().upper()
                    if opt:
                        setattr(q, f'option_{attr}', opt)
                    if typ in 'RIASEC':
                        setattr(q, f'type_{attr}', typ)
                q.save()
                message = "Question mise à jour."
            except Question.DoesNotExist:
                message = "Question introuvable."

    questions = Question.objects.order_by('element', 'id')
    if element_filter:
        questions = questions.filter(element=element_filter)

    # Attach opts_list to each question for the template
    questions = list(questions)
    for q in questions:
        q.opts_list = [
            ('A', q.option_a, q.type_a),
            ('B', q.option_b, q.type_b),
            ('C', q.option_c, q.type_c),
            ('D', q.option_d, q.type_d),
        ]

    return render(request, 'admin_questions.html', {
        'questions': questions,
        'message': message,
        'element_choices': ELEMENT_CHOICES,
        'element_filter': element_filter,
        'riasec_types': list('RIASEC'),
        'opts_meta': [('a','A'), ('b','B'), ('c','C'), ('d','D')],
        'current_user': request.session.get('admin_username'),
        'active_tab': 'questions',
    })


# ── Admin — Session detail ────────────────────────────────────────────────────

@_admin_required
def admin_session_detail_view(request, code):
    session = get_object_or_404(GameSession, code=code)
    results = session.results.order_by('-created_at')
    n = results.count()

    dom_counts = {t: 0 for t in 'RIASEC'}
    score_sums = {k: 0 for k in 'RIASEC'}

    for r in results:
        if r.dominant in dom_counts:
            dom_counts[r.dominant] += 1
        score_sums['R'] += r.score_r
        score_sums['I'] += r.score_i
        score_sums['A'] += r.score_a
        score_sums['S'] += r.score_s
        score_sums['E'] += r.score_e
        score_sums['C'] += r.score_c

    avg_scores = {k: round(v / n, 1) if n > 0 else 0 for k, v in score_sums.items()}

    return render(request, 'admin_session.html', {
        'session': session,
        'results': results,
        'n': n,
        'dom_counts': dom_counts,
        'avg_scores': avg_scores,
        'riasec_names': RIASEC_NAMES,
        'current_user': request.session.get('admin_username'),
        'active_tab': 'dashboard',
    })


# ── Session publique ──────────────────────────────────────────────────────────

def session_view(request):
    error = None

    if request.method == 'POST' and 'code' in request.POST:
        code = request.POST.get('code', '').strip().upper()
        if not code:
            error = "Entrez un code de session."
        else:
            try:
                gs = GameSession.objects.get(code=code, is_open=True)
                request.session['session_code_valid'] = gs.code
                return redirect('session')
            except GameSession.DoesNotExist:
                error = "Code invalide ou session non ouverte."

    code_valid = request.session.get('session_code_valid')
    if code_valid:
        try:
            gs = GameSession.objects.get(code=code_valid)
            results = gs.results.order_by('-created_at')
            class_filter = request.GET.get('classe', '').strip()
            classes = sorted(set(r.school_class for r in results if r.school_class))
            if class_filter:
                results = results.filter(school_class=class_filter)
            return render(request, 'session.html', {
                'mode': 'results', 'session': gs, 'results': results,
                'riasec_names': RIASEC_NAMES, 'classes': classes, 'class_filter': class_filter,
            })
        except GameSession.DoesNotExist:
            del request.session['session_code_valid']

    return render(request, 'session.html', {'mode': 'login', 'error': error})
