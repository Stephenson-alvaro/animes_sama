import requests
from bs4 import BeautifulSoup
import json

# URL de base du site (modifie si nécessaire)
BASE_URL = "https://anime-sama.fr/catalogue?page="

# Liste pour stocker les résultats
animes = []

# Définir le numéro de la première page
page = 1

while True:
    url = f"{BASE_URL}{page}"
    print(f"Scraping page {page}...")  # Affichage de progression

    # Récupération du contenu HTML
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Fin du scraping à la page {page - 1}.")
        break  # Arrêter si la page n'existe pas

    soup = BeautifulSoup(response.text, "html.parser")

    # Recherche des divs contenant les animes
    found_anime = False  # Vérification pour arrêter quand il n'y a plus d'animes

    for div in soup.find_all("div", class_="shrink-0 m-3 rounded border-2 border-gray-400 border-opacity-50 shadow-2xl shadow-black hover:shadow-zinc-900 hover:opacity-80 bg-black bg-opacity-40 transition-all duration-200 cursor-pointer"):
        a_tag = div.find("a", class_="flex divide-x")

        if a_tag:
            lien = a_tag["href"]  # Récupération du lien

            h1_tag = a_tag.find("h1", class_="text-white font-bold uppercase text-md line-clamp-2")
            titre = h1_tag.text.strip() if h1_tag else "Titre inconnu"

            img_tag = a_tag.find("img", class_="imageCarteHorizontale object-cover transition-all duration-200 cursor-pointer")
            image = img_tag["src"] if img_tag else "Image non trouvée"

            animes.append({"titre": titre, "lien": lien, "image": image})
            found_anime = True

    if not found_anime:  # Si aucune anime n'est trouvé, arrêter
        print(f"Aucune donnée trouvée sur la page {page}. Arrêt du scraping.")
        break

    page += 1  # Passer à la page suivante

# Sauvegarde des résultats dans un fichier JSON
with open("animes.json", "w", encoding="utf-8") as f:
    json.dump(animes, f, ensure_ascii=False, indent=4)

print(f"Scraping terminé ! {len(animes)} animes enregistrés dans animes.json.")
