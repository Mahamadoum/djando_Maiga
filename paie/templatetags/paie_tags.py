from django import template

from paie.models import Poste, Tag

register = template.Library()

# Données des postes (définies directement dans le tag)
@register.simple_tag()
def get_postes():
    postes_db = [
        {'id': 1, 'name': 'Comptabilité'},
        {'id': 2, 'name': 'Ressources Humaines'},
        {'id': 3, 'name': 'Développement'},
        {'id': 4, 'name': 'Direction'},
    ]
    return postes_db
@register.inclusion_tag('paie/includes/list_postes.html')
def show_postes(poste_selected_id=0):
    postes = Poste.objects.all()
    return {"postes": postes, "poste_selected": poste_selected_id}
@register.inclusion_tag('paie/includes/list_tags.html')
def show_tags(tag_selected_id=0):
    tags = Tag.objects.all()
    return {"tags": tags, "tag_selected": tag_selected_id}
@register.inclusion_tag('paie/includes/list_tags.html')

def show_all_tags():
    return {"tags": Tag.objects.all()}
