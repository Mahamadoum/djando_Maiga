from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from paie.forms import AddEmployeForm, UploadFileModelForm
from paie.models import Employe, Poste, Tag, UploadedFile

menu = [
    {'title': "Accueil", 'url_name': 'home'},
    {'title': "Employés", 'url_name': 'liste_employes'},
    {'title': "Contact", 'url_name': 'contact'},
]
postes_db = [
    {'id': 1, 'name': 'Бухгалтерия'},
    {'id': 2, 'name': 'Кадры'},
    {'id': 3, 'name': 'Разработка'},
    {'id': 4, 'name': 'Дирекция'},
]
def about(request):
    data = {
        'title': 'À propos',
        'menu': menu,
    }
    return render(request, 'paie/about.html', data)


@login_required
def liste_employes(request):
    """
    Affiche la liste des employés avec liens pour ajouter, modifier, supprimer
    """
    # Récupérer tous les employés (ou filtrer si nécessaire)
    employes = Employe.objects.all()

    # Filtrage par nom (optionnel)
    nom_filtre = request.GET.get('nom', '')
    if nom_filtre:
        employes = employes.filter(nom__icontains=nom_filtre)
        messages.info(request, f"Filtrage par nom : {nom_filtre}")

    context = {
        'title': 'Liste des employés',
        'menu': menu,
        'employes': employes,
        'nom_filtre': nom_filtre,
    }
    return render(request, 'paie/liste_employes.html', context)


@login_required
def ajouter_employe(request):
    """
    Ajouter un nouvel employé
    """
    if request.method == 'POST':
        form = AddEmployeForm(request.POST, request.FILES)
        if form.is_valid():
            employe = form.save(commit=False)
            # Générer le slug automatiquement si non fourni
            if not employe.slug:
                employe.slug = f"{employe.nom.lower()}-{employe.prenom.lower()}"
            employe.save()
            form.save_m2m()  # Pour les relations ManyToMany (tags)
            messages.success(request, f"Employé {employe.nom} {employe.prenom} ajouté avec succès !")
            return redirect('liste_employes')
        else:
            messages.error(request, "Erreur lors de l'ajout. Veuillez corriger les erreurs ci-dessous.")
    else:
        form = AddEmployeForm()

    context = {
        'title': 'Ajouter un employé',
        'menu': menu,
        'form': form,
    }
    return render(request, 'paie/ajouter_employe.html', context)


@login_required
def modifier_employe(request, pk):
    """
    Modifier un employé existant
    """
    employe = get_object_or_404(Employe, pk=pk)

    if request.method == 'POST':
        form = AddEmployeForm(request.POST, request.FILES, instance=employe)
        if form.is_valid():
            employe = form.save(commit=False)
            if not employe.slug:
                employe.slug = f"{employe.nom.lower()}-{employe.prenom.lower()}"
            employe.save()
            form.save_m2m()
            messages.success(request, f"Employé {employe.nom} {employe.prenom} modifié avec succès !")
            return redirect('liste_employes')
        else:
            messages.error(request, "Erreur lors de la modification.")
    else:
        form = AddEmployeForm(instance=employe)

    context = {
        'title': f'Modifier {employe.prenom} {employe.nom}',
        'menu': menu,
        'form': form,
        'employe': employe,
    }
    return render(request, 'paie/modifier_employe.html', context)


@login_required
def supprimer_employe(request, pk):
    """
    Supprimer un employé
    """
    employe = get_object_or_404(Employe, pk=pk)

    if request.method == 'POST':
        nom_complet = f"{employe.nom} {employe.prenom}"
        employe.delete()
        messages.success(request, f"Employé {nom_complet} supprimé avec succès !")
        return redirect('liste_employes')

    context = {
        'title': f'Supprimer {employe.prenom} {employe.nom}',
        'menu': menu,
        'employe': employe,
    }
    return render(request, 'paie/supprimer_employe.html', context)
def detail_employe(request, emp_slug):
    employe = get_object_or_404(Employe, pk=emp_slug)
    data = {
        'title': f"{employe.prenom} {employe.nom}",
        'employe': employe,
    }
    return render(request, 'paie/detail_employe.html', data)
def archive_bulletins_custom(request, year):
    return HttpResponse(f"<h1>Архивы конвертер ударов</h1><p>год : {year} (type: {type(year).__name__})</p>")
def detail_employe_slug(request, emp_slug):
    employe = get_object_or_404(Employe, slug=emp_slug)
    data = {
        'title': f"{employe.prenom} {employe.nom}",
        'employe': employe,
    }
    return render(request, 'paie/detail_employe.html', data)
def traiter_formulaire(request):
    if request.POST:
        print("Données POST reçues :", request.POST)
        return HttpResponse("Formulaire traité")
    return HttpResponse("Afficher formulaire")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page non trouvée</h1><p>L'URL demandée n'existe pas.</p>")
from django.shortcuts import redirect

def archive_bulletins_custom(request, year):
    if year > 2024:
        return redirect('/')   # Redirection vers l'accueil
    return HttpResponse(f"<h1>Archives</h1><p>Année : {year}</p>")
def archive_bulletins_custom301(request, year):
    if year > 2025:
        return redirect('/', permanent=True)
    return HttpResponse(f"<h1>Archives</h1><p>Année : {year}</p>")
from django.urls import reverse

def test_reverse(request):
    url = reverse('detail_employe', args=[5])
    return HttpResponse(f"URL générée : {url}")
class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

employes_db = [
    {'id': 1, 'nom': 'Жан Дюпон', 'poste': 'Бухгалтер', 'salaire': 2500, 'actif': True},
    {'id': 2, 'nom': 'Мари Мартен', 'poste': 'HR', 'salaire': 2800, 'actif': False},
    {'id': 3, 'nom': 'Пьер Дюран', 'poste': 'Разработчик', 'salaire': 3200, 'actif': True},
]

def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'employes': Employe.actifs.all(),
    }
    return render(request, 'paie/index.html', context=data)
def add_employe(request):
    return HttpResponse("Ajout d'un employé")

def contact(request):
    return HttpResponse("Page de contact")

def login(request):
    return HttpResponse("Page de connexion")
def postes(request, poste_id):
    data = {
        'title': f'Poste ID: {poste_id}',
        'menu': menu,
        'employes': employes_db,
        'postes_selected': poste_id,
    }
    return render(request, 'paie/index.html', data)


def show_poste(request, poste_slug):
    # Получение должности по слагу (или 404)
    poste = get_object_or_404(Poste, slug=poste_slug)

    # Получение активных сотрудников этой должности
    employes = Employe.actifs.filter(poste=poste)

    data = {
        'title': f'Должность: {poste.nom}',
        'menu': menu,
        'employes': employes,
        'poste_selected': poste.id,
    }
    return render(request, 'paie/index.html', context=data)


def index(request):
    employes = Employe.actifs.all()
    poste_selected = 0

    # Фильтрация по параметру GET
    poste_slug = request.GET.get('poste')
    if poste_slug:
        poste = get_object_or_404(Poste, slug=poste_slug)
        employes = employes.filter(poste=poste)
        poste_selected = poste.id

    data = {
        'title': 'Главная',
        'menu': menu,
        'employes': employes,
        'poste_selected': poste_selected,
    }
    return render(request, 'paie/index.html', data)


def show_tag_employes(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    employes = tag.employes.filter(actif=True)  # Использует related_name='employes'

    data = {
        'title': f'Навык: {tag.nom}',
        'menu': menu,
        'employes': employes,
        'tag_selected': tag.id,
    }
    return render(request, 'paie/index.html', data)


def show_tag_employes(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    employes = tag.employes.filter(actif=True)  # Использует related_name='employes'

    data = {
        'title': f'Навык: {tag.nom}',
        'menu': menu,
        'employes': employes,
        'poste_selected': None,
    }
    return render(request, 'paie/index.html', context=data)
def index(request):
    data = {
        'title': 'Главная',
        'menu': menu,
        'employes': Employe.actifs.all(),
        'poste_selected': 0,
    }
    return render(request, 'paie/index.html', context=data)


def add_employe(request):
    if request.method == 'POST':
        form = AddEmployeForm(request.POST)
        if form.is_valid():

            employe = form.save()
            return redirect('liste_employes')
    else:
        form = AddEmployeForm()

    return render(request, 'paie/add_employe.html', {'form': form})
def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    files = UploadedFile.objects.all()  # Afficher les fichiers déjà uploadés

    if request.method == 'POST':
        form = UploadFileModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Sauvegarde automatique du fichier et de la BDD
            messages.success(request, "Fichier uploadé avec succès !")
            return redirect('about')
    else:
        form = UploadFileModelForm()

    context = {
        'title': 'Gestion des fichiers',
        'menu': menu,
        'form': form,
        'files': files,
    }
    return render(request, 'paie/about.html', context)


@login_required
def liste_postes(request):
    """
    Отображает список должностей со ссылками для добавления, редактирования, удаления
    """
    postes = Poste.objects.all()

    context = {
        'title': 'Список должностей',
        'menu': menu,
        'postes': postes,
    }
    return render(request, 'paie/liste_postes.html', context)


@login_required
def ajouter_poste(request):
    """
    Добавление новой должности
    """
    if request.method == 'POST':
        nom = request.POST.get('nom')
        slug = request.POST.get('slug')

        if not slug:
            slug = nom.lower().replace(' ', '-')

        try:
            poste = Poste.objects.create(nom=nom, slug=slug)
            messages.success(request, f"Должность '{poste.nom}' успешно добавлена !")
            return redirect('liste_postes')
        except Exception as e:
            messages.error(request, f"Ошибка при добавлении : {e}")

    context = {
        'title': 'Добавление должности',
        'menu': menu,
    }
    return render(request, 'paie/ajouter_poste.html', context)


@login_required
def modifier_poste(request, pk):
    """
    Редактирование существующей должности
    """
    poste = get_object_or_404(Poste, pk=pk)

    if request.method == 'POST':
        nom = request.POST.get('nom')
        slug = request.POST.get('slug')

        if not slug:
            slug = nom.lower().replace(' ', '-')

        try:
            poste.nom = nom
            poste.slug = slug
            poste.save()
            messages.success(request, f"Должность '{poste.nom}' успешно изменена !")
            return redirect('liste_postes')
        except Exception as e:
            messages.error(request, f"Ошибка при изменении : {e}")

    context = {
        'title': f'Редактирование {poste.nom}',
        'menu': menu,
        'poste': poste,
    }
    return render(request, 'paie/modifier_poste.html', context)


@login_required
def supprimer_poste(request, pk):
    """
    Удаление должности
    """
    poste = get_object_or_404(Poste, pk=pk)

    # Проверка, есть ли сотрудники на этой должности
    employes_count = Employe.objects.filter(poste=poste).count()

    if request.method == 'POST':
        nom_poste = poste.nom
        if employes_count > 0:
            messages.error(request,
                           f"Невозможно удалить должность '{nom_poste}', так как она используется {employes_count} сотрудником(ами).")
            return redirect('liste_postes')

        poste.delete()
        messages.success(request, f"Должность '{nom_poste}' успешно удалена !")
        return redirect('liste_postes')

    context = {
        'title': f'Удаление {poste.nom}',
        'menu': menu,
        'poste': poste,
        'employes_count': employes_count,
    }
    return render(request, 'paie/supprimer_poste.html', context)


from django.shortcuts import render
from django.contrib import messages
from .gemini_utils import get_gemini_response, generer_description_poste, chat_rh, analyser_cv


def assistant_rh(request):
    """
    Assistant RH avec Gemini
    """
    reponse = None

    if request.method == 'POST':
        question = request.POST.get('question', '')
        action = request.POST.get('action', 'chat')

        if action == 'chat':
            reponse = chat_rh(question)
        elif action == 'description_poste':
            titre = request.POST.get('titre', '')
            competences = request.POST.get('competences', '')
            experience = request.POST.get('experience', 3)
            reponse = generer_description_poste(titre, competences, experience)
        else:
            reponse = get_gemini_response(question)

        messages.success(request, "Réponse générée avec succès !")

    data = {
        'title': 'Assistant RH - IA Gemini',
        'menu': menu,
        'reponse': reponse,
    }
    return render(request, 'paie/assistant_rh.html', data)


def analyser_cv_upload(request):
    """
    Analyse un CV uploadé avec Gemini
    """
    reponse = None

    if request.method == 'POST' and request.FILES.get('cv_file'):
        fichier = request.FILES['cv_file']
        contenu = fichier.read().decode('utf-8', errors='ignore')
        reponse = analyser_cv(contenu)
        messages.success(request, "CV analysé avec succès !")

    data = {
        'title': 'Analyse de CV',
        'menu': menu,
        'reponse': reponse,
    }
    return render(request, 'paie/analyser_cv.html', data)