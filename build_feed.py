import json

import re

import urllib.parse

import urllib.request

import xml.etree.ElementTree as ET

from datetime import datetime, timezone, timedelta

from email.utils import parsedate_to_datetime

from pathlib import Path

from html import unescape

# LE RADAR V3 — quatre veilles quotidiennes

QUERIES = {

    "tech": [

        "OpenAI OR Anthropic OR Mistral AI OR intelligence artificielle",

        "IA générative OR LLM OR ChatGPT OR Claude OR Gemini",

        "Microsoft AI OR Google Cloud OR AWS OR cloud computing",

        "cybersécurité OR data engineering OR big data",

        "logiciel entreprise OR SaaS OR marché IT OR ESN",

    ],

    "finance": [

        "Bourse marchés financiers CAC 40",

        "Wall Street OR Nasdaq OR S&P 500 OR Dow Jones",

        "actions entreprises cotées résultats financiers",

        "banques centrales OR BCE OR Federal Reserve OR taux intérêt",

        "inflation OR croissance économique OR PIB OR chômage",

        "obligations OR dette souveraine OR taux obligataires",

        "euro dollar OR devises OR marché des changes",

        "or OR pétrole OR matières premières OR énergie",

        "cryptomonnaies OR Bitcoin OR Ethereum réglementation",

        "banques OR assurance OR gestion actifs OR fonds investissement",

        "Engie OR TotalEnergies OR Veolia OR EDF",

        "Amundi OR Société Générale OR BNP Paribas OR Crédit Agricole",

    ],

    "politique": [

        "politique française gouvernement actualité",

        "Assemblée nationale OR Sénat OR Parlement français",

        "loi France OR décret gouvernement OR réforme politique",

        "élections France OR sondage politique France",

        "Union européenne politique Commission européenne",

        "actualité politique internationale diplomatie",

        "conflit géopolitique OR relations internationales",

        "politique publique France OR collectivités territoriales",

    ],

    "feminisme": [

        "droits des femmes actualité France",

        "égalité femmes hommes égalité salariale",

        "violences faites aux femmes féminicides",

        "santé des femmes santé reproductive",

        "féminisme loi femmes justice France",

        "droits des femmes Europe législation",

        "droits des femmes actualité internationale",

        "parité femmes entreprises politique",

        "harcèlement sexuel violences sexuelles justice",

    ],

}

LABELS = {

    "tech": "TECH & IA",

    "finance": "FINANCE & ÉCONOMIE",

    "politique": "POLITIQUE",

    "feminisme": "FÉMINISME",

}

def clean(value):

    value = unescape(re.sub(r"<[^>]+>", " ", value or ""))

    return re.sub(r"\s+", " ", value).strip()

def fetch(query):

    url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({

        "q": query + " when:7d",

        "hl": "fr",

        "gl": "FR",

        "ceid": "FR:fr",

    })

    request = urllib.request.Request(

        url,

        headers={"User-Agent": "LE-RADAR/3.0"}

    )

    with urllib.request.urlopen(request, timeout=30) as response:

        return ET.fromstring(response.read())

def parse_date(value):

    try:

        date = parsedate_to_datetime(value)

        if date.tzinfo is None:

            date = date.replace(tzinfo=timezone.utc)

        return date.astimezone(timezone.utc).isoformat()

    except Exception:

        return ""

def make_summary(description):

    description = clean(description)

    if not description:

        return "Extrait non disponible. Consulte l'article original pour les détails."

    if len(description) > 420:

        description = description[:417].rsplit(" ", 1)[0] + "..."

    return description

def main():

    articles = []

    seen = set()

    cutoff = datetime.now(timezone.utc) - timedelta(days=8)

    for category, queries in QUERIES.items():

        for query in queries:

            try:

                root = fetch(query)

                for node in root.findall(".//item"):

                    title = clean(node.findtext("title"))

                    url = (node.findtext("link") or "").strip()

                    published = parse_date(node.findtext("pubDate") or "")

                    if not title or not url:

                        continue

                    if url in seen:

                        continue

                    try:

                        date = datetime.fromisoformat(

                            published.replace("Z", "+00:00")

                        )

                        if date < cutoff:

                            continue

                    except Exception:

                        continue

                    source = clean(node.findtext("source") or "Source RSS")

                    description = clean(node.findtext("description") or "")

                    articles.append({

                        "category": category,

                        "topic": LABELS[category],

                        "title": title,

                        "url": url,

                        "published": published,

                        "source": source,

                        "summary": make_summary(description),

                    })

                    seen.add(url)

            except Exception as error:

                print("Flux indisponible :", query, repr(error))

    articles.sort(

        key=lambda article: article["published"],

        reverse=True

    )

    # Jusqu'à 30 articles par rubrique

    counts = {category: 0 for category in QUERIES}

    selected = []

    for article in articles:

        category = article["category"]

        if counts[category] < 30:

            selected.append(article)

            counts[category] += 1

    output = {

        "generated_at": datetime.now(timezone.utc).isoformat(),

        "articles": selected,

        "counts": counts,

        "note": (

            "Articles issus de flux RSS publics. "

            "Les résumés reprennent les extraits fournis par les sources. "

            "Consulter les articles originaux pour vérifier les informations."

        ),

    }

    Path("data").mkdir(exist_ok=True)

    Path("data/veille.json").write_text(

        json.dumps(output, ensure_ascii=False, indent=2),

        encoding="utf-8"

    )

    print("LE RADAR V3 :", len(selected), "articles collectés")

    print("Répartition :", counts)

if __name__ == "__main__":

    main()