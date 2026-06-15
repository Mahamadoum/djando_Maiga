from openai import OpenAI
from django.conf import settings

# Configuration du client DeepSeek (API compatible OpenAI)
client = OpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def get_deepseek_response(prompt):
    """
    Envoie un prompt à DeepSeek et retourne la réponse.
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Tu es un assistant RH spécialisé en gestion des salaires et des bulletins de paie."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erreur DeepSeek : {str(e)}"

def generer_description_poste(titre_poste, competences, experience):
    """
    Génère une description de poste avec DeepSeek.
    """
    prompt = f"""
    Rédige une description de poste détaillée pour le titre suivant : {titre_poste}

    Compétences requises : {competences}
    Expérience demandée : {experience} ans

    La description doit contenir :
    1. Un résumé du poste
    2. Les missions principales
    3. Les compétences requises (techniques et humaines)
    4. Les avantages du poste

    Sois professionnel, détaillé et concis.
    """
    return get_deepseek_response(prompt)

def chat_rh(question):
    """
    Chatbot RH pour répondre aux questions sur la gestion des salaires.
    """
    prompt = f"""
    Tu es un assistant RH spécialisé en gestion des salaires et des bulletins de paie.
    Réponds à la question suivante de manière professionnelle et précise :

    Question : {question}
    """
    return get_deepseek_response(prompt)