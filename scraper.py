import asyncio
import json
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

BASE_URL = "https://anime-sama.fr/catalogue?page="
animes = []

async def fetch_html(page_number: int):
    url = f"{BASE_URL}{page_number}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state("networkidle")  # Attendre que tout soit chargé
        content = await page.content()  # Récupérer le HTML complet
        await browser.close()
    return content

def parse_animes(content: str):
    soup = BeautifulSoup(content, "html.parser")
    divs = soup.select("div.shrink-0.m-3.rounded.border-2.border-gray-400.border-opacity-50.shadow-2xl.shadow-black.hover\\:shadow-zinc-900.hover\\:opacity-80.bg-black.bg-opacity-40.transition-all.duration-200.cursor-pointer")

    found_anime = False
    page_animes = []

    for div in divs:
        if not div.find("p", string=lambda t: t and "Anime" in t):
            continue

        a_tag = div.find("a", class_="flex divide-x")
        if a_tag:
            lien = a_tag.get("href", "Lien non trouvé")
            h1_tag = a_tag.find("h1", class_="text-white font-bold uppercase text-md line-clamp-2")
            titre = h1_tag.text.strip() if h1_tag else "Titre inconnu"
            img_tag = a_tag.find("img", class_="imageCarteHorizontale object-cover transition-all duration-200 cursor-pointer")
            image = img_tag.get("src", "Image non trouvée")

            page_animes.append({"titre": titre, "lien": lien, "image": image})
            found_anime = True

    return page_animes, found_anime

async def scrape():
    page = 1

    while True:
        print(f"Scraping la page {page}...")
        content = await fetch_html(page)
        page_animes, found_anime = parse_animes(content)

        if not found_anime:
            print(f"Aucune donnée trouvée sur la page {page}. Arrêt du scraping.")
            break

        animes.extend(page_animes)
        page += 1

    # Sauvegarder les résultats dans un fichier JSON
    with open("animes.json", "w", encoding="utf-8") as f:
        json.dump(animes, f, ensure_ascii=False, indent=4)
    print(f"Scraping terminé. {len(animes)} animes récupérés.")

if __name__ == "__main__":
    asyncio.run(scrape())
