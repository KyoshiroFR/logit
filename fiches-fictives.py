# Fiches fictives pour tester une mise à jour : créées par le vrai code de LogIT (versions chaînées, captures, journal).
from datetime import timedelta
from io import BytesIO
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.utils import timezone
from PIL import Image
from journal.chain import verify
from journal.models import Element, Intervention

auteur = get_user_model().objects.filter(is_superuser=True, is_active=True).order_by("pk").first()
c = Client(HTTP_HOST="127.0.0.1")
c.force_login(auteur)
s = c.session; s["logit_otp_ok"] = True; s.save()
E = {n: Element.objects.get_or_create(name=n, defaults={"kind": k, "group": g})[0].pk for n, k, g in [
    ("[FICTIF] DC-TEST", "equipment", "ad"), ("[FICTIF] FW-TEST", "equipment", "network"),
    ("[FICTIF] VPN-TEST", "service", "network"), ("[FICTIF] SQL-TEST", "equipment", "database")]}
FMT = "%Y-%m-%dT%H:%M"
def quand(h): return (timezone.localtime() - timedelta(hours=h)).strftime(FMT)
def capture():
    b = BytesIO(); Image.new("RGB", (320, 180), (124, 108, 255)).save(b, "PNG")
    return SimpleUploadedFile("capture-fictive.png", b.getvalue(), content_type="image/png")
def envoyer(url, data):
    r = c.post(url, data, secure=True)
    if r.status_code != 302:
        raise SystemExit(f"Échec sur {url} (code {r.status_code}) : rien de plus n'est créé.")
    return Intervention.objects.order_by("-pk").first().pk
def fiche(**o):
    d = {"kind": "normal", "category": "config", "occurred_at": quand(1), "reason": "Test de mise à jour (fiche fictive)",
         "impact": "Aucun", "verification": "", "rollback": "", "before_state": "", "after_state": ""}
    d.update(o); return d

n1 = envoyer("/fiches/nouvelle/", fiche(title="[FICTIF] Blocage NTLMv1 par GPO", category="security", elements=[E["[FICTIF] DC-TEST"]],
     change="GPO de test liée à l'OU de test", impact="Vieilles applications NTLM à surveiller", rollback="Délier la GPO de test",
     before_state="NTLM autorisé", after_state="Kerberos uniquement", attachments=[capture()], occurred_at=quand(30)))
envoyer(f"/fiches/{n1}/corriger/", fiche(title="[FICTIF] Blocage NTLMv1 par GPO", category="security", elements=[E["[FICTIF] DC-TEST"]],
     change="GPO de test liée à l'OU de test", impact="Vieilles applications NTLM à surveiller",
     rollback="Délier la GPO de test puis gpupdate /force", before_state="NTLM autorisé", after_state="Kerberos uniquement",
     occurred_at=quand(30), note="Procédure de retour arrière précisée"))
n2 = envoyer("/fiches/nouvelle/", fiche(title="[FICTIF] Ouverture du port 443 de test", elements=[E["[FICTIF] FW-TEST"]],
     change="Règle de test 42", rollback="Supprimer la règle de test 42", occurred_at=quand(20)))
envoyer(f"/fiches/{n2}/retour-arriere/", fiche(title="[FICTIF] Retour arrière : port 443 de test", elements=[E["[FICTIF] FW-TEST"]],
     change="Suppression de la règle de test 42", rollback="Recréer la règle de test 42", occurred_at=quand(18)))
envoyer("/fiches/nouvelle/", fiche(kind="urgent", title="[FICTIF] Redémarrage d'urgence de SQL-TEST", category="fix",
     elements=[E["[FICTIF] SQL-TEST"]], change="Redémarrage du service de test", reason="", impact="", occurred_at=quand(2)))
envoyer("/fiches/nouvelle/", fiche(kind="planned", title="[FICTIF] Mise à jour planifiée du VPN de test", category="maintenance",
     elements=[E["[FICTIF] VPN-TEST"]], change="Firmware de test", rollback="Partition de secours",
     occurred_at=(timezone.localtime() + timedelta(days=2)).strftime(FMT)))
anomalies = verify()
print(f"Fiches fictives créées par {auteur.username}. Fiches au total : {Intervention.objects.count()}. "
      f"Intégrité : {'aucune anomalie' if not anomalies else anomalies}")
