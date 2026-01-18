

# Create your views here.
from .models import Message
from django.shortcuts import render, redirect , get_object_or_404
from .forms import LoginForm, StudentProfilForm, EmployeeProfilForm ,EditStudentForm, EditEmployeeForm
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




def register(request):
    """
    Vue d'inscription : permet de choisir entre étudiant et employé
    puis affiche le formulaire correspondant
    
    Paramètre GET 'type' : 'student' ou 'employee'
    """
    
    # Récupérer le type d'utilisateur depuis l'URL (student ou employee)
    # Par défaut : student
    user_type = request.GET.get('type')
    
    # Vérifier si la requête est POST (formulaire soumis)
    if request.method == "POST":
        
        # Récupérer le type depuis le formulaire POST
        user_type = request.POST.get('user_type')
        
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
        




from django.shortcuts import render, redirect
from .forms import LoginForm, StudentProfilForm, EmployeeProfilForm, MessageForm
from .models import Person, Student, Employee, Message

# ... (vos autres vues login, register, logout)

def welcome(request):
    """
    Page d'accueil avec publication de messages
    """
    
    # 1. Récupérer l'utilisateur connecté
    logged_user = get_logged_user_from_request(request)
    
    # 2. Vérifier s'il est connecté
    if not logged_user:
        return redirect('/login/')
    
    # 3. Gérer la publication de message (POST)
    if request.method == "POST":
        form = MessageForm(request.POST)
        
        if form.is_valid():
            # Créer le message sans le sauvegarder encore
            message = form.save(commit=False)
            
            # Associer l'auteur (l'utilisateur connecté)
            message.auteur = logged_user
            
            # Sauvegarder en base de données
            message.save()
            
            # Rediriger vers welcome pour éviter la re-soumission
            return redirect('/welcome/')
        else:
            # Si le formulaire est invalide, afficher les erreurs
            members_same_faculty = (
                Person.objects.filter(faculty=logged_user.faculty)
                .exclude(id=logged_user.id)
                .exclude(id__in=logged_user.amis.all())
            )
            return render(request, 'welcome.html', {
                'logged_user': logged_user,
                'form': form,
                'messages': get_messages_for_user(logged_user),
                'members_same_faculty': members_same_faculty,
            })
    
    # 4. Afficher la page (GET)
    else:
        # Créer un formulaire vide
        form = MessageForm()
    
    # 5. Récupérer les messages à afficher
    messages_list = get_messages_for_user(logged_user)

    # 5bis. Récupérer les membres de la même faculté (hors soi-même)
    members_same_faculty = (
        Person.objects.filter(faculty=logged_user.faculty)
        .exclude(id=logged_user.id)
        .exclude(id__in=logged_user.amis.all())
    )
    
    # 6. Afficher le template
    return render(request, 'welcome.html', {
        'logged_user': logged_user,
        'form': form,
        'messages': messages_list,
        'members_same_faculty': members_same_faculty,
    })


def get_messages_for_user(user):
    """
    Récupère les messages de l'utilisateur et de ses amis
    """
    
    # Liste des auteurs : l'utilisateur + ses amis
    auteurs = [user] + list(user.amis.all())
    
    # Récupérer tous les messages de ces auteurs
    messages = Message.objects.filter(auteur__in=auteurs).order_by('-date_publication')
    
    return messages



def view_profile(request, user_id):
    """
    Affiche le profil d'un utilisateur (Student ou Employee)
    """
    
    # 1. Vérifier que l'utilisateur connecté existe
    logged_user = get_logged_user_from_request(request)
    
    if not logged_user:
        return redirect('/login/')
    
    # 2. Récupérer l'utilisateur dont on veut voir le profil
    # Chercher d'abord dans Student
    profile_user = None
    
    if Student.objects.filter(id=user_id).exists():
        profile_user = Student.objects.get(id=user_id)
    elif Employee.objects.filter(id=user_id).exists():
        profile_user = Employee.objects.get(id=user_id)
    else:
        # Si l'utilisateur n'existe pas, rediriger vers welcome
        return redirect('/welcome/')
    
    # 3. Récupérer les messages de cet utilisateur
    user_messages = Message.objects.filter(auteur=profile_user).order_by('-date_publication')
    
    # 4. Vérifier si c'est un ami
    is_friend = profile_user in logged_user.amis.all()
    
    # 5. Vérifier si c'est son propre profil
    is_own_profile = (logged_user.id == profile_user.id)
    
    # 6. Afficher le template
    return render(request, 'profile.html', {
        'logged_user': logged_user,
        'profile_user': profile_user,
        'user_messages': user_messages,
        'is_friend': is_friend,
        'is_own_profile': is_own_profile,
    })



def edit_profile(request):
    """
    Permet à l'utilisateur de modifier son profil
    """
    
    # 1. Récupérer l'utilisateur connecté
    logged_user = get_logged_user_from_request(request)
    
    if not logged_user:
        return redirect('/login/')
    
    # 2. Déterminer si c'est un Student ou Employee
    is_student = hasattr(logged_user, 'annee')
    
    # 3. Traiter la soumission du formulaire (POST)
    if request.method == "POST":
        if is_student:
            form = EditStudentForm(request.POST, instance=logged_user)
        else:
            form = EditEmployeeForm(request.POST, instance=logged_user)
        
        if form.is_valid():
            form.save()
            # Rediriger vers le profil après modification
            return redirect('/profile/' + str(logged_user.id) + '/')
        else:
            # Afficher les erreurs
            return render(request, 'edit_profile.html', {
                'logged_user': logged_user,
                'form': form,
                'is_student': is_student,
            })
    
    # 4. Afficher le formulaire (GET)
    else:
        if is_student:
            form = EditStudentForm(instance=logged_user)
        else:
            form = EditEmployeeForm(instance=logged_user)
        
        return render(request, 'edit_profile.html', {
            'logged_user': logged_user,
            'form': form,
            'is_student': is_student,
        })





def add_friend(request, user_id):
    """
    Ajouter un utilisateur comme ami
    """
    
    # 1. Récupérer l'utilisateur connecté
    logged_user = get_logged_user_from_request(request)
    
    if not logged_user:
        return redirect('/login/')
    
    # 2. Récupérer l'utilisateur à ajouter
    friend_to_add = None
    
    if Student.objects.filter(id=user_id).exists():
        friend_to_add = Student.objects.get(id=user_id)
    elif Employee.objects.filter(id=user_id).exists():
        friend_to_add = Employee.objects.get(id=user_id)
    else:
        # L'utilisateur n'existe pas
        return redirect('/welcome/')
    
    # 3. Vérifier qu'on n'ajoute pas soi-même
    if logged_user.id == friend_to_add.id:
        return redirect('/profile/' + str(user_id) + '/')
    
    # 4. Vérifier qu'ils ne sont pas déjà amis
    if friend_to_add not in logged_user.amis.all():
        # Ajouter l'ami dans les deux sens
        logged_user.amis.add(friend_to_add)
        friend_to_add.amis.add(logged_user)
    
    # 5. Rediriger vers le profil de l'ami
    return redirect('/profile/' + str(user_id) + '/')



def search_users(request):
    """
    Rechercher des utilisateurs
    """
    from django.db.models import Q
    
    # 1. Récupérer l'utilisateur connecté
    logged_user = get_logged_user_from_request(request)
    
    if not logged_user:
        return redirect('/login/')
    
    # 2. Récupérer le terme de recherche
    search_query = request.GET.get('q', '').strip()
    results = []
    
    if search_query:
        # Récupérer TOUS les utilisateurs (sauf soi-même)
        all_students = Student.objects.exclude(id=logged_user.id)
        all_employees = Employee.objects.exclude(id=logged_user.id)
        all_users = list(all_students) + list(all_employees)
        
        # Filtrer manuellement pour plus de flexibilité
        search_lower = search_query.lower()
        
        for user in all_users:
            # Créer une chaîne avec toutes les infos
            searchable_text = f"{user.prenom} {user.nom} {user.nom} {user.prenom} {user.email}".lower()
            
            # Vérifier si tous les mots de la recherche sont présents
            if all(word.lower() in searchable_text for word in search_query.split()):
                results.append(user)
        
        # Limiter à 20 résultats
        results = results[:20]
    
    # 3. IMPORTANT : Récupérer la liste des IDs des amis
    friend_ids = list(logged_user.amis.values_list('id', flat=True))
    
    print(f"DEBUG: logged_user = {logged_user.prenom} (ID {logged_user.id})")
    print(f"DEBUG: friend_ids = {friend_ids}")
    print(f"DEBUG: Résultats = {[(r.id, r.prenom, r.nom) for r in results]}")
    
    # 4. Afficher le template
    return render(request, 'search_users.html', {
        'logged_user': logged_user,
        'search_query': search_query,
        'results': results,
        'friend_ids': friend_ids,  # ← CRUCIAL
    })

from django.http import JsonResponse

def add_friend_ajax(request, user_id):
    """
    Ajouter un ami via AJAX (sans redirection)
    """
    print("=" * 50)
    print("DEBUG ADD_FRIEND_AJAX")
    print(f"Méthode: {request.method}")
    print(f"User ID à ajouter: {user_id}")
    
    if request.method != 'POST':
        print(" Erreur: Méthode non POST")
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})
    
    # Récupérer l'utilisateur connecté
    logged_user = get_logged_user_from_request(request)
    
    print(f"Utilisateur connecté: {logged_user}")
    
    if not logged_user:
        print(" Erreur: Pas d'utilisateur connecté")
        return JsonResponse({'success': False, 'error': 'Non connecté'})
    
    # Récupérer l'utilisateur à ajouter
    friend_to_add = None
    
    try:
        if Student.objects.filter(id=user_id).exists():
            friend_to_add = Student.objects.get(id=user_id)
            print(f" Trouvé Student: {friend_to_add.prenom} {friend_to_add.nom}")
        elif Employee.objects.filter(id=user_id).exists():
            friend_to_add = Employee.objects.get(id=user_id)
            print(f" Trouvé Employee: {friend_to_add.prenom} {friend_to_add.nom}")
        else:
            print(" Erreur: Utilisateur introuvable")
            return JsonResponse({'success': False, 'error': 'Utilisateur introuvable'})
    except Exception as e:
        print(f" Exception lors de la recherche: {e}")
        return JsonResponse({'success': False, 'error': str(e)})
    
    # Vérifier qu'on n'ajoute pas soi-même
    if logged_user.id == friend_to_add.id:
        print(" Erreur: Tentative d'ajout de soi-même")
        return JsonResponse({'success': False, 'error': 'Vous ne pouvez pas vous ajouter vous-même'})
    
    # Vérifier qu'ils ne sont pas déjà amis
    if friend_to_add in logged_user.amis.all():
        print(" Déjà amis")
        return JsonResponse({'success': False, 'error': 'Déjà ami'})
    
    # Ajouter l'ami dans les deux sens
    try:
        print(f" Ajout de {friend_to_add.prenom} dans les amis de {logged_user.prenom}...")
        logged_user.amis.add(friend_to_add)
        
        print(f" Ajout de {logged_user.prenom} dans les amis de {friend_to_add.prenom}...")
        friend_to_add.amis.add(logged_user)
        
        # IMPORTANT: Sauvegarder explicitement
        logged_user.save()
        friend_to_add.save()
        
        print(" Amis ajoutés avec succès")
        
        # Vérifier que ça a bien marché
        print(f"Vérification: {logged_user.prenom} a {logged_user.amis.count()} amis")
        print(f"Vérification: {friend_to_add.prenom} a {friend_to_add.amis.count()} amis")
        
        print("=" * 50)
        
        return JsonResponse({
            'success': True,
            'message': f'{friend_to_add.prenom} {friend_to_add.nom} a été ajouté à vos amis'
        })
    except Exception as e:
        print(f" Exception lors de l'ajout: {e}")
        print("=" * 50)
        return JsonResponse({'success': False, 'error': f'Erreur lors de l\'ajout: {str(e)}'})
# ===============================
# DÉCONNEXION
# ===============================
def logout(request):
    """
    Vue de déconnexion : supprime la session de l'utilisateur
    """
    
    # Supprimer l'ID de l'utilisateur de la session
    if 'logged_user_id' in request.session:
        del request.session['logged_user_id']
    
    # Vider complètement la session (optionnel mais recommandé)
    request.session.flush()
    
    # Rediriger vers la page de login
    return redirect('/login/')       



def same_faculty_users_view(request, person_id):
    # 1. On récupère l'utilisateur actuel
    logged_user = get_object_or_404(Person, id=person_id)
    
    # 2. On filtre les membres de la même faculté
    # On exclut l'utilisateur lui-même (.exclude(id=logged_user.id))
    # On exclut également ceux qui sont déjà dans la liste 'amis' (.exclude(id__in=...))

    members_same_faculty = (
    Person.objects.filter(faculty=logged_user.faculty)
    .exclude(id=logged_user.id)
    .exclude(id__in=logged_user.amis.all())
)
    # 3. On rend le template avec les résultats
    return render(request, 'welcome.html', {
        'logged_user': logged_user,
        'members_same_faculty': members_same_faculty
    })

