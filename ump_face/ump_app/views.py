

# Create your views here.
from django.shortcuts import render, redirect
from .forms import LoginForm, StudentProfilForm, EmployeeProfilForm  # ← Ajoutez EmployeeProfilForm
from .models import Person ,Student, Employee

def login(request):
    """
    Vue de connexion : gère l'authentification des utilisateurs
    """
    
    # Vérifier si la requête est de type POST (formulaire soumis)
    if request.method == "POST":
        
        # Créer une instance du formulaire avec les données soumises
        form = LoginForm(request.POST)
        
        # Valider le formulaire (vérification email/mot de passe)
        if form.is_valid():
            
            # Récupérer l'email validé depuis le formulaire
            email = form.cleaned_data['email']
            
            # Rechercher l'utilisateur dans la base de données par son email
            logged_user = Person.objects.get(email=email)

            # === CRÉATION DE LA SESSION ===
            # Stocker l'ID de l'utilisateur dans la session pour le garder connecté
            # Cette information sera conservée entre les différentes pages
            request.session['logged_user_id'] = logged_user.id

            # Rediriger vers la page d'accueil après connexion réussie
            return redirect('/welcome/')
        else:
            # Si le formulaire n'est pas valide (erreurs de validation)
            # Réafficher la page de login avec le formulaire et les erreurs
            return render(request, 'login.html', {'form': form})

    else:
        # Si la requête est de type GET (première visite de la page)
        # Créer un formulaire vide pour l'afficher
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def welcome(request):
    """
    Vue de la page d'accueil : accessible uniquement aux utilisateurs connectés
    """
    
    # Récupérer l'utilisateur connecté depuis la session
    logged_user = get_logged_user_from_request(request)

    # Vérifier si un utilisateur est bien connecté
    if logged_user:
        # Si oui : afficher la page d'accueil avec les infos de l'utilisateur
        return render(request, 'welcome.html', {'logged_user': logged_user})
    else:
        # Si non : rediriger vers la page de connexion
        # (protection contre les accès non autorisés)
        return redirect('/login/')


from .models import Student, Employee

def get_logged_user_from_request(request):
    """
    Fonction utilitaire : récupère l'utilisateur connecté depuis la session
    Retourne un objet Student ou Employee selon le type d'utilisateur
    Retourne None si aucun utilisateur n'est connecté
    """
    
    # Vérifier si l'ID de l'utilisateur existe dans la session
    if 'logged_user_id' in request.session:
        
        # Récupérer l'ID stocké dans la session
        user_id = request.session['logged_user_id']

        # === VÉRIFICATION DU TYPE D'UTILISATEUR ===
        
        # Vérifier si l'utilisateur est un étudiant
        if Student.objects.filter(id=user_id).exists():
            # Si oui : retourner l'objet Student complet
            return Student.objects.get(id=user_id)

        # Vérifier si l'utilisateur est un employé
        if Employee.objects.filter(id=user_id).exists():
            # Si oui : retourner l'objet Employee complet
            return Employee.objects.get(id=user_id)

    # Si l'utilisateur n'est pas dans la session OU n'existe pas en base
    # Retourner None (utilisateur non connecté)
    return None




def register(request):
    """
    Vue d'inscription : permet de choisir entre étudiant et employé
    puis affiche le formulaire correspondant
    
    Paramètre GET 'type' : 'student' ou 'employee'
    """
    
    # Récupérer le type d'utilisateur depuis l'URL (student ou employee)
    # Par défaut : student
    user_type = request.GET.get('type', 'student')
    
    # Vérifier si la requête est POST (formulaire soumis)
    if request.method == "POST":
        
        # Récupérer le type depuis le formulaire POST
        user_type = request.POST.get('user_type', 'student')
        
        # === INSCRIPTION ÉTUDIANT ===
        if user_type == 'student':
            # Créer le formulaire étudiant avec les données soumises
            form = StudentProfilForm(request.POST)
            
            # Valider le formulaire
            if form.is_valid():
                # Sauvegarder l'étudiant dans la base de données
                new_student = form.save()
                
                # Rediriger vers la page de login après inscription réussie
                return redirect('/login/')
            else:
                # Si erreurs : réafficher le formulaire avec les erreurs
                return render(request, 'register.html', {
                    'form': form,
                    'user_type': 'student',
                    'errors': form.errors
                })
        
        # === INSCRIPTION EMPLOYÉ ===
        elif user_type == 'employee':
            # Créer le formulaire employé avec les données soumises
            form = EmployeeProfilForm(request.POST)
            
            # Valider le formulaire
            if form.is_valid():
                # Sauvegarder l'employé dans la base de données
                new_employee = form.save()
                
                # Rediriger vers la page de login après inscription réussie
                return redirect('/login/')
            else:
                # Si erreurs : réafficher le formulaire avec les erreurs
                return render(request, 'register.html', {
                    'form': form,
                    'user_type': 'employee',
                    'errors': form.errors
                })
    
    else:
        # === REQUÊTE GET : Afficher le formulaire vide ===
        
        if user_type == 'student':
            # Créer un formulaire étudiant vide
            form = StudentProfilForm()
            return render(request, 'register.html', {
                'form': form,
                'user_type': 'student'
            })
        
        elif user_type == 'employee':
            # Créer un formulaire employé vide
            form = EmployeeProfilForm()
            return render(request, 'register.html', {
                'form': form,
                'user_type': 'employee'
            })
        
        else:
            # Par défaut, afficher le formulaire étudiant
            form = StudentProfilForm()
            return render(request, 'register.html', {
                'form': form,
                'user_type': 'student'
            })