import google.generativeai as genai
from django.conf import settings

# Configuration de l'API
genai.configure(api_key=settings.GEMINI_API_KEY)


def get_gemini_response(prompt, model_name="gemini-1.5-flash"):
    """
    Envoie un prompt à Gemini et retourne la réponse.
    """
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erreur : {str(e)}"


def generer_description_poste(titre_poste, competences, experience):
    """
    Génère une description de poste avec Gemini.
    """
    prompt = f"""
    Tu es un expert en ressources humaines.
    Rédige une description de poste pour le titre suivant : {titre_poste}.

    Compétences requises : {competences}
    Expérience demandée : {experience} ans

    La description doit contenir :
    1. Un résumé du poste
    2. Les missions principales
    3. Les compétences requises
    4. Les avantages du poste

    Sois professionnel et concis.
    """
    return get_gemini_response(prompt)


def analyser_cv(texte_cv):
    """
    Analyse un CV et extrait les informations clés.
    """
    prompt = f"""
    Analyse le CV suivant et extrait :
    - Nom du candidat
    - Compétences principales (liste)
    - Années d'expérience
    - Niveau d'études

    CV :
    {texte_cv[:3000]}
    """
    return get_gemini_response(prompt)


def chat_rh(question):
    """
    Chatbot RH pour répondre aux questions sur la gestion des salaires.
    """
    prompt = f"""
    Tu es un assistant RH spécialisé en gestion des salaires et des bulletins de paie.
    Réponds à la question suivante de manière professionnelle et précise :

    Question : {question}
    """
    return get_gemini_response(prompt)