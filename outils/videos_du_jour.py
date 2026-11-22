"""Lit le flux PUBLIC de la chaîne YouTube de Diwéra et écrit partage/videos.json (vidéos des 4 derniers jours).
Lancé toutes les heures par GitHub (gratuit), pour la page partage/ de son iPhone. Aucune clé, aucun mot de passe."""
import json, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
CHAINE = "UCxNwUEMPxnXM4X2iXtn-Kjw"   # DIWÉRA - La Voix Du Coeur
ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015", "media": "http://search.yahoo.com/mrss/"}
xml = urllib.request.urlopen(f"https://www.youtube.com/feeds/videos.xml?channel_id={CHAINE}", timeout=30).read()
limite = datetime.now(timezone.utc) - timedelta(days=4)
videos = []
for e in ET.fromstring(xml).findall("a:entry", ns):
    pub = datetime.fromisoformat(e.find("a:published", ns).text)
    if pub < limite:
        continue
    vid = e.find("yt:videoId", ns).text
    lien = e.find("a:link", ns).get("href")
    desc = e.find("media:group/media:description", ns)
    videos.append({"id": vid, "titre": e.find("a:title", ns).text, "description": (desc.text or "") if desc is not None else "",
                   "sortie": pub.isoformat(), "lien": "https://youtube.com/shorts/" + vid if "/shorts/" in lien else "https://youtu.be/" + vid})
videos.sort(key=lambda v: v["sortie"], reverse=True)
json.dump({"maj": datetime.now(timezone.utc).isoformat(), "videos": videos}, open("partage/videos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(videos), "vidéo(s)")
