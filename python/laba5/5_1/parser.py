import argparse
import csv
import os
import time
import re
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org/wiki/"


def clean_text(text: str):
    if not text:
        return ""

    text = re.sub(r"\d+°\d+.*", "", text)

    text = re.sub(r"\[[^\]]+\]", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

def extract_number(text: str):
    if not text:
        return ""

    text = text.replace(",", "")
    nums = re.findall(r"\d+", text)

    return nums[0] if nums else ""


def load_page(country, cache_dir):
    filename = os.path.join(cache_dir, f"{country}.html")

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    url = BASE_URL + country.replace(" ", "_")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)

        time.sleep(1)
        return response.text

    except Exception as e:
        print(f"Ошибка загрузки {country}: {e}")
        return None



def parse_infobox(html):
    soup = BeautifulSoup(html, "lxml")
    info = {"city": "", "area": "", "population": ""}

    infobox = soup.find("table", class_="infobox")
    if not infobox:
        return info

    capital_keys = [
        "Capital",
        "Capital city",
        "Capital and largest city",
        "Seat"
    ]

    for th in infobox.find_all("th"):
        text = th.get_text(" ", strip=True)
        if any(key in text for key in capital_keys):
            td = th.find_next("td")
            if td:
                raw = td.get_text(" ", strip=True)
                info["city"] = clean_text(raw)
                break

    for th in infobox.find_all("th"):
        text = th.get_text(" ", strip=True)
        if "Area" in text:
            td = th.find_next("td")
            if td:
                raw = td.get_text(" ", strip=True)
                info["area"] = extract_number(raw)
                break

    for th in infobox.find_all("th"):
        text = th.get_text(" ", strip=True)
        if "Population" in text:
            td = th.find_next("td")
            if td:
                raw = td.get_text(" ", strip=True)
                info["population"] = extract_number(raw)
                break

    return info



def main():
    parser = argparse.ArgumentParser(description="Wikipedia country parser")
    parser.add_argument("-i", "--input", required=True, help="Input countries.txt")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file")

    args = parser.parse_args()

    cache_dir = "cache"
    os.makedirs(cache_dir, exist_ok=True)

    with open(args.input, "r", encoding="utf-8") as f:
        countries = [line.strip() for line in f if line.strip()]

    with open(args.output, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["country", "city", "area", "population"])

        for country in countries:
            print(f"Обработка: {country}")

            html = load_page(country, cache_dir)
            if not html:
                writer.writerow([country, "", "", ""])
                continue

            data = parse_infobox(html)

            writer.writerow([
                country,
                data["city"],
                data["area"],
                data["population"]
            ])

    print(f"Готово! Данные сохранены в {args.output}")


if __name__ == "__main__":
    main()
