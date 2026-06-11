from django.contrib import admin
from django.utils.html import mark_safe
from .models import Employe, Poste, Tag


# Filtre personnalisé pour la tranche de salaire
class SalaireFilter(admin.SimpleListFilter):
    title = "Диапазон зарплаты"
    parameter_name = "salaire_range"

    def lookups(self, request, model_admin):
        return [
            ('bas', 'Менее 2000 €'),
            ('moyen', '2000 € - 3000 €'),
            ('eleve', 'Более 3000 €'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'bas':
            return queryset.filter(salaire__lt=2000)
        if self.value() == 'moyen':
            return queryset.filter(salaire__gte=2000, salaire__lte=3000)
        if self.value() == 'eleve':
            return queryset.filter(salaire__gt=3000)
        return queryset


# Admin pour le modèle Employe (UN SEUL)
@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'poste', 'salaire', 'actif', 'info_salaire', 'photo_preview')
    list_display_links = ('nom',)
    list_editable = ('actif',)
    list_filter = [SalaireFilter, 'actif', 'poste']
    search_fields = ['nom', 'prenom', 'poste__nom', 'email']
    list_per_page = 10

    fields = ['nom', 'prenom', 'email', 'salaire', 'poste', 'tags', 'actif', 'photo', 'photo_preview']
    readonly_fields = ['photo_preview']
    save_on_top = True

    @admin.display(description="Зарплата (€)")
    def info_salaire(self, employe: Employe):
        return f"{employe.salaire} €"

    @admin.display(description="Предпросмотр фото")
    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" style="border-radius: 5px;" />')
        return "Нет фото"


# Admin pour le modèle Poste
@admin.register(Poste)
class PosteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    list_display_links = ('id', 'nom')
    search_fields = ['nom']


# Admin pour le modèle Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    list_display_links = ('id', 'nom')
    search_fields = ['nom']