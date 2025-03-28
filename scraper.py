import requests
from bs4 import BeautifulSoup
import json

# URL de base du site
BASE_URL = "https://anime-sama.fr/catalogue?page="

# Liste pour stocker les résultats
animes = []
page = 1

while True:
    url = f"{BASE_URL}{page}"
    print(f"Scraping page {page}...")
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
    "DNT": "1",  # Ne pas me pister (certains sites l'ignorent)
}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response.status_code)
        print(f"Fin du scraping à la page {page - 1}.")
        break

    soup = BeautifulSoup(response.text, "html.parser")

    # Utilisation d'un sélecteur CSS pour trouver les divs
    # Remarquez que les classes avec ":" nécessitent d'être échappées avec "\\"
    divs = soup.select("div.shrink-0.m-3.rounded.border-2.border-gray-400.border-opacity-50.shadow-2xl.shadow-black.hover\\:shadow-zinc-900.hover\\:opacity-80.bg-black.bg-opacity-40.transition-all.duration-200.cursor-pointer")

    found_anime = False

    for div in divs:
        # Vérification si la balise <p> contenant "Anime" existe dans la div
        if not div.find("p", string=lambda t: t and "Anime" in t):
            continue

        a_tag = div.find("a", class_="flex divide-x")
        if a_tag:
            lien = a_tag.get("href", "Lien non trouvé")
            h1_tag = a_tag.find("h1", class_="text-white font-bold uppercase text-md line-clamp-2")
            titre = h1_tag.text.strip() if h1_tag else "Titre inconnu"
            img_tag = a_tag.find("img", class_="imageCarteHorizontale object-cover transition-all duration-200 cursor-pointer")
            image = img_tag.get("src", "Image non trouvée")

            animes.append({"titre": titre, "lien": lien, "image": image})
            found_anime = True

    if not found_anime:
        print(f"Aucune donnée trouvée sur la page {page}. Arrêt du scraping.")
        break

    page += 1

# Sauvegarde des résultats dans un fichier JSON
with open("animes.json", "w", encoding="utf-8") as f:
    json.dump(animes, f, ensure_ascii=False, indent=4)

print(f"Scraping terminé ! {len(animes)} animes enregistrés dans animes.json.")
