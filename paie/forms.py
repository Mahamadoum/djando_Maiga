from django import forms
from django.core.exceptions import ValidationError
from .models import Employe, Poste, Tag


class AddEmployeForm(forms.ModelForm):
    # Настройка полей связи
    poste = forms.ModelChoiceField(
        queryset=Poste.objects.all(),
        empty_label="-- Выберите должность --",
        label="Должность"
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label="Навыки",
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'})
    )

    class Meta:
        model = Employe
        fields = ['nom', 'prenom', 'email', 'salaire', 'poste', 'tags', 'actif']

        labels = {
            'nom': 'Фамилия',
            'prenom': 'Имя',
            'email': 'Email',
            'salaire': 'Зарплата (€)',
            'actif': 'Активен',
        }

        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите фамилию'}),
            'prenom': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'exemple@email.com'}),
            'salaire': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    # Пользовательская валидация
    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if len(nom) < 2:
            raise ValidationError('Фамилия должна содержать минимум 2 символа')
        return nom

    def clean_salaire(self):
        salaire = self.cleaned_data.get('salaire')
        if salaire and salaire < 0:
            raise ValidationError('Зарплата не может быть отрицательной')
        return salaire
from .models import UploadedFile
class UploadFileModelForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file', 'description']