from django.urls import path, register_converter
from django.conf.urls.static import static
from django.conf import settings
from . import converters, views

# Enregistrement du convertisseur personnalisé
register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    # Pages principales
    path('', views.index, name='home'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Gestion des employés (CRUD)
    path('employes/', views.liste_employes, name='liste_employes'),
    path('employes/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('employes/modifier/<int:pk>/', views.modifier_employe, name='modifier_employe'),
    path('employes/supprimer/<int:pk>/', views.supprimer_employe, name='supprimer_employe'),
    path('employes/<slug:emp_slug>/', views.detail_employe_slug, name='detail_employe_slug'),

    # Gestion des postes (CRUD)
    path('postes/', views.liste_postes, name='liste_postes'),
    path('postes/ajouter/', views.ajouter_poste, name='ajouter_poste'),
    path('postes/modifier/<int:pk>/', views.modifier_poste, name='modifier_poste'),
    path('postes/supprimer/<int:pk>/', views.supprimer_poste, name='supprimer_poste'),
    path('postes/<slug:poste_slug>/', views.show_poste, name='postes_detail'),

    # Tags
    path('assistant-rh/', views.assistant_rh, name='assistant_rh'),
    path('tag/<slug:tag_slug>/', views.show_tag_employes, name='tag_detail'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)