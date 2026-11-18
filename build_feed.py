import json, re, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from html import unescape

QUERIES = {
 "tech": [
  "OpenAI OR Anthropic OR Mistral AI OR intelligence artificielle",
  "Microsoft AI OR Google Cloud OR AWS OR cloud computing OR cybersécurité",
  "ESN OR marché IT OR data engineering OR logiciel entreprise"
 ],
 "finance": [
  "Engie OR TotalEnergies OR Veolia OR EDF actualité",
  "Amundi OR Société Générale résultats stratégie",
  "économie France OR marchés financiers OR taux BCE OR énergie"
 ]
}
def clean(s):
 s=unescape(re.sub(r"<[^>]+>", " ", s or ""))
 return re.sub(r"\s+", " ", s).strip()
def fetch(query):
 url="https://news.google.com/rss/search?"+urllib.parse.urlencode({"q":query+" when:7d","hl":"fr","gl":"FR","ceid":"FR:fr"})
 req=urllib.request.Request(url,headers={"User-Agent":"LE-RADAR/1.0 (personal news reader)"})
 with urllib.request.urlopen(req,timeout=25) as r: return ET.fromstring(r.read())
def parse_date(s):
 try:
  d=parsedate_to_datetime(s)
  if d.tzinfo is None:d=d.replace(tzinfo=timezone.utc)
  return d.astimezone(timezone.utc).isoformat()
 except:return ""
def main():
 items=[]; seen=set(); cutoff=datetime.now(timezone.utc)-timedelta(days=8)
 for category,queries in QUERIES.items():
  for q in queries:
   try:
    root=fetch(q)
    for node in root.findall(".//item"):
     title=clean(node.findtext("title")); link=node.findtext("link") or ""
     pub=parse_date(node.findtext("pubDate") or "")
     if not title or not link or link in seen:continue
     try:
      dt=datetime.fromisoformat(pub.replace("Z","+00:00"))
      if dt<cutoff:continue
     except:pass
     seen.add(link)
     source=clean(node.findtext("source") or "Google Actualités")
     desc=clean(node.findtext("description") or "")
     # Keep excerpts short; the source link is the authoritative article.
     items.append({"category":category,"topic":"TECH & IA" if category=="tech" else "ÉCONOMIE","title":title,"url":link,"published":pub,"source":source,"summary":desc[:420]})
   except Exception as e:
    print("Feed unavailable:",q,repr(e))
 items.sort(key=lambda x:x.get("published",""),reverse=True)
 # Cap each desk so the app stays quick and readable.
 counts={"tech":0,"finance":0}; selected=[]
 for x in items:
  c=x["category"]
  if counts[c]<18:selected.append(x);counts[c]+=1
 out={"generated_at":datetime.now(timezone.utc).isoformat(),"articles":selected,"note":"Titres et extraits issus des flux Google Actualités RSS. Vérifier les informations dans l'article source."}
 Path("data/veille.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
 print("Wrote",len(selected),"articles")
if __name__=="__main__":main()
