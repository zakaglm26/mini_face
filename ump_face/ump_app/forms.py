from django import forms
from .models import Person, Student, Employee

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput
    )

    # Validation personnalisée
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            result = Person.objects.filter(email=email, password=password)
            if len(result) != 1:
                raise forms.ValidationError("Email ou mot de passe incorrect")

        return cleaned_data









# ============================================
# FORMULAIRE DE LOGIN (déjà existant)
# ============================================
class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre email'
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre mot de passe'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        
        if email and password:
            result = Person.objects.filter(password=password, email=email)
            if len(result) != 1:
                raise forms.ValidationError("Adresse email ou mot de passe incorrects.")
        
        return cleaned_data


# ============================================
# FORMULAIRE D'INSCRIPTION ÉTUDIANT
# ============================================
class StudentProfilForm(forms.ModelForm):
    """
    Formulaire d'inscription pour les étudiants
    Basé sur le modèle Student (ModelForm)
    """
    
    # Redéfinir le champ password pour qu'il soit masqué
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choisissez un mot de passe'
        }),
        help_text='Minimum 4 caractères'
    )
    
    # Champ de confirmation du mot de passe
    confirm_password = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe'
        })
    )
    
    class Meta:
        model = Student
        # Exclure le champ 'amis' car il sera vide lors de l'inscription
        exclude = ('amis',)
        
        # Personnaliser les widgets pour un meilleur affichage
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom de famille'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre prénom'
            }),
            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre.email@example.com'
            }),
            'tlf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0612345678'
            }),
            'faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'annee': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Année d\'étude (1, 2, 3...)',
                'min': '1',
                'max': '5'
            }),
            'cursus': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        
        # Labels en français
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'date_naissance': 'Date de naissance',
            'email': 'Email',
            'tlf': 'Téléphone',
            'faculty': 'Faculté',
            'annee': 'Année d\'étude',
            'cursus': 'Cursus',
        }
        
        # Textes d'aide
        help_texts = {
            'email': 'Utilisez votre email universitaire de préférence',
            'annee': 'Votre année d\'étude actuelle',
        }
    
    def clean(self):
        """
        Validation personnalisée : vérifier que les deux mots de passe correspondent
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        # Vérifier que les deux mots de passe sont identiques
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Les mots de passe ne correspondent pas.")
            
            # Vérifier la longueur minimale
            if len(password) < 4:
                raise forms.ValidationError("Le mot de passe doit contenir au moins 4 caractères.")
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Sauvegarder l'étudiant avec le mot de passe
        """
        student = super().save(commit=False)
        # Assigner le mot de passe (en production, il faudrait le hasher)
        student.password = self.cleaned_data['password']
        
        if commit:
            student.save()
        
        return student
    


# ============================================
# FORMULAIRE D'INSCRIPTION EMPLOYÉ
# ============================================
class EmployeeProfilForm(forms.ModelForm):
    """
    Formulaire d'inscription pour les employés
    Basé sur le modèle Employee (ModelForm)
    """
    
    # Redéfinir le champ password pour qu'il soit masqué
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choisissez un mot de passe'
        }),
        help_text='Minimum 4 caractères'
    )
    
    # Champ de confirmation du mot de passe
    confirm_password = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe'
        })
    )
    
    class Meta:
        model = Employee
        # Exclure le champ 'amis' car il sera vide lors de l'inscription
        exclude = ('amis',)
        
        # Personnaliser les widgets pour un meilleur affichage
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom de famille'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre prénom'
            }),
            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre.email@example.com'
            }),
            'tlf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0612345678'
            }),
            'faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'office': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de bureau (ex: B201)'
            }),
            'campus': forms.Select(attrs={
                'class': 'form-control'
            }),
            'job': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        
        # Labels en français
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'date_naissance': 'Date de naissance',
            'email': 'Email',
            'tlf': 'Téléphone',
            'faculty': 'Faculté',
            'office': 'Bureau',
            'campus': 'Campus',
            'job': 'Poste',
        }
        
        # Textes d'aide
        help_texts = {
            'email': 'Utilisez votre email professionnel',
            'office': 'Numéro ou nom de votre bureau',
        }
    
    def clean(self):
        """
        Validation personnalisée : vérifier que les deux mots de passe correspondent
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        # Vérifier que les deux mots de passe sont identiques
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Les mots de passe ne correspondent pas.")
            
            # Vérifier la longueur minimale
            if len(password) < 4:
                raise forms.ValidationError("Le mot de passe doit contenir au moins 4 caractères.")
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Sauvegarder l'employé avec le mot de passe
        """
        employee = super().save(commit=False)
        # Assigner le mot de passe (en production, il faudrait le hasher)
        employee.password = self.cleaned_data['password']
        
        if commit:
            employee.save()
        
        return employee