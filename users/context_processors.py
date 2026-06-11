from paie.views import menu

def get_paie_context(request):
    return {'mainmenu': menu}