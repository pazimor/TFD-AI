import re
import requests

languages = ["fr", "ko", "en", "de", "ja", "zh-CN", "zh-TW", "it", "pl", "pt", "ru", "es"]
languages_bdd = ["fr", "ko", "en", "de", "ja", "zh_cn", "zh_tw", "it", "pl", "pt", "ru", "es"] ## matching laguage BDD

BASE_URL = "https://open.api.nexon.com/static/tfd/meta"

def get_fixed_lang(lang):
    """Return the fixed language"""
    ## TODO: refactor and move this
    ##       language should be able to be supperpose both
    return re.sub(r'_([a-z]{2})', lambda m: '-' + m.group(1).upper(), lang)

def fetch_url(url):
    """Récupère les données depuis l'URL spécifiée."""
    try:
        response = requests.get(f"{url}")
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération : {e}")
        return []

def get_fixed_lang(lang):
    """Return the fixed language code: use the original if French, else reformat."""
    return lang if lang == "fr" else re.sub(r'_([a-z]{2})', lambda m: '-' + m.group(1).upper(), lang)

def fetch_multy_lang(target_url):
    """Récupère les données pour tous les langages pour l'URL cible."""
    all_data = {}
    for lang in languages:
        url = f"{BASE_URL}/{lang}/{target_url}"
        data = fetch_url(url)
        if data is not None:
            all_data[lang] = data
    return all_data
