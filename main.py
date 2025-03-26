import feedparser
from lxml import etree
from datetime import datetime
import pytz
import requests
import re

RSS_FEEDS = [
    "https://www.mundodeportivo.com/rss/elotromundo.xml",
    "https://www.mundodeportivo.com/rss/actualidad.xml"
]
OUTPUT_FILE = "rss-showcase.xml"
TITLE_LIMIT = 84
SUMMARY_LIMIT = 60
MAX_ENTRIES = 20

def truncate(text, max_length):
    if not text:
        return ""
    return text if len(text) <= max_length else text[:max_length].rsplit(" ", 1)[0] + "…"

def extract_section_from_url(url):
    parts = url.split("/")
    for section in ["gente", "television", "lifestyle", "mascotas", "actualidad"]:
        if section in parts:
            return section
    return "actualidad"

def generate_bullet_list(title, section):
    bullets = []

    # Conversacional según sección
    if section == "gente":
        bullets.append(f"¿Qué ha pasado con {title.split()[0]}? Aquí te lo contamos")
        bullets.append("Si te gusta el mundo del corazón, esto te va")
        bullets.append("No te pierdas la última de los famosos")
    elif section == "television":
        bullets.append("¿Te va la tele? Esto no te lo puedes perder")
        bullets.append("Lo último que ha dado que hablar en la pantalla")
        bullets.append("Así está el panorama televisivo ahora mismo")
    elif section == "lifestyle":
        bullets.append("Tendencias, eventos y mucho más, aquí")
        bullets.append("Esto está dando que hablar y no es para menos")
        bullets.append("¿Te mola el rollo lifestyle? Mira esto")
    elif section == "mascotas":
        bullets.append("¿Amante de los animales? Esto te va a gustar")
        bullets.append("Una historia que derrite a cualquiera")
        bullets.append("No todo el mundo tiene un perro así…")
    else:  # actualidad u otros
        bullets.append("¿Te interesa lo que pasa hoy? Esto te toca")
        bullets.append("Lo último en clave de actualidad")
        bullets.append("Esto está marcando el día en la calle")

    return bullets

def build_atom_feed(entries):
    NSMAP = {
        None: "http://www.w3.org/2005/Atom",
        "g": "http://schemas.google.com/pcn/2020",
        "media": "http://search.yahoo.com/mrss/"
    }

    feed = etree.Element("feed", nsmap=NSMAP)
    etree.SubElement(feed, "title").text = "Mundo Deportivo - Showcase"
    etree.SubElement(feed, "id").text = "urn:uuid:feed-md-elotromundo-actualidad"
    etree.SubElement(feed, "updated").text = datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat()
    etree.SubElement(feed, "link", rel="self", href="https://www.mundodeportivo.com/rss-showcase.xml")

    for i, entry in enumerate(entries[:MAX_ENTRIES]):
        e = etree.SubElement(feed, "entry")
        etree.SubElement(e, "{http://schemas.google.com/pcn/2020}panel", type="SINGLE_STORY").text = f"Panel {i+1}"
        etree.SubElement(e, "id").text = f"urn:uuid:{entry['link']}"
        pub_date = datetime(*entry.published_parsed[:6], tzinfo=pytz.UTC)
        etree.SubElement(e, "published").text = pub_date.isoformat()
        etree.SubElement(e, "updated").text = pub_date.isoformat()
        etree.SubElement(e, "title").text = truncate(entry.title, TITLE_LIMIT)
        etree.SubElement(e, "author").append(etree.Element("name"))
        e.find("author/name").text = "Autor Redacción"
        etree.SubElement(e, "summary").text = truncate(entry.get("summary", ""), SUMMARY_LIMIT)
        etree.SubElement(e, "link", href=entry.link)
        if "media_content" in entry and entry.media_content:
            etree.SubElement(e, "{http://search.yahoo.com/mrss/}content", url=entry.media_content[0]['url'])

        section = extract_section_from_url(entry.link)
        bullets = generate_bullet_list(entry.title, section)
        bl = etree.SubElement(e, "{http://schemas.google.com/pcn/2020}bullet_list")
        for item in bullets:
            etree.SubElement(bl, "{http://schemas.google.com/pcn/2020}list_item").text = item

    return etree.ElementTree(feed)

def fetch_and_merge_feeds():
    all_entries = []
    for url in RSS_FEEDS:
        d = feedparser.parse(requests.get(url).content)
        all_entries.extend(d.entries)
    all_entries.sort(key=lambda x: x.published_parsed, reverse=True)
    return all_entries

if __name__ == "__main__":
    entries = fetch_and_merge_feeds()
    tree = build_atom_feed(entries)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True, pretty_print=True)