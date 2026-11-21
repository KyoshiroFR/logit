# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Règles de travail

- Si quelque chose est ambigu, pose la question au lieu de supposer.
- Fais la solution la plus simple qui marche, pas de fonctionnalité non demandée.
- Ne modifie que le code nécessaire à la demande, ne touche pas au reste.
- Lance `python manage.py test` avant chaque commit (voir « Tests » ci-dessous) et respecte `docs/regressions.md`.
- Écris en français : code, commentaires, messages de commit, interface.
- Utilise uniquement des données fictives dans les tests et les captures d'écran.
- Design : garde le thème actuel (sombre, accent violet `#7c6cff`, variables de `src/journal/static/journal/logit.css`). Interfaces modernes et vivantes, avec des micro-animations de 150 à 350 ms, courbes douces, animant uniquement `transform` et `opacity`. Respecte toujours `prefers-reduced-motion`. Tout doit rester utilisable au clavier et sur mobile.
- Les 6 rubriques de la barre du haut (Registre, Nouvelle fiche, Comptes, Éléments, Journal de sécurité, Intégrité) sont figées ; les nouveautés vont dans la zone utilisateur, à droite.
- Les idées futures vont dans `docs/roadmap.md`.

## Le projet

LogIT est le registre des interventions d'infrastructure et de sécurité d'une petite équipe : qui a changé quoi, quand, pourquoi, avec quel impact, et comment revenir en arrière. Il sert la traçabilité NIS2. Django 5.2, PostgreSQL 17, gunicorn, whitenoise, Caddy ; pages rendues côté serveur, JavaScript sans framework. Cible : Debian 12 et 13 (amd64, arm64).

Numérotation `v0.MINEUR.CORRECTIF` jusqu'à la mise en production (`v1.0.0`) : une fonction ajoutée incrémente le mineur, une correction le correctif.

## Tests

Les tests exigent un PostgreSQL réel (ils vérifient les protections de la base). Depuis `src/` :

```bash
LOGIT_SECRET_KEY=dev LOGIT_TESTING=1 LOGIT_DB_HOST=127.0.0.1 \
LOGIT_DB_AS_OWNER=1 LOGIT_DB_OWNER_USER=logit_owner LOGIT_DB_OWNER_PASSWORD=… \
LOGIT_DB_APP_USER=logit_app LOGIT_DB_APP_PASSWORD=… python manage.py test journal
```

Un seul test : `python manage.py test journal.tests.InterventionTests.test_…` (mêmes variables).

- Utiliser `TestCase`, jamais `TransactionTestCase` : son TRUNCATE est refusé par les déclencheurs.
- Avant un `ALTER TABLE … DISABLE TRIGGER` dans un test : `SET CONSTRAINTS ALL IMMEDIATE`.

Scripts shell : `bash -n` et `shellcheck` sur `install.sh` et `deploy/logit`.

La CI GitHub (`.github/workflows/ci.yml`) relance ces contrôles à chaque envoi, plus la validation des fichiers compose et la construction de l'image.

## Architecture

- `src/config/` : réglages. Tout ce qui dépend de l'installation vient de l'environnement (`LOGIT_*`, fichier `/opt/logit/.env`).
- `src/journal/` : l'application unique.
  - `models.py` : une fiche (`Intervention`) est une suite de `Version`. Corriger, marquer réalisée ou annuler ajoute une version (auteur, date serveur, motif obligatoire). Deux dates : `occurred_at` (déclarée) et `recorded_at` (serveur, non modifiable).
  - `chain.py` : chaîne d'empreintes SHA-256 sur les versions et le journal de sécurité (`AuditEvent`), vérifiée par `manage.py verify_chain` / `logit verify` / page Intégrité.
  - `permissions.py` : rôles admin (`is_superuser`), groupes « Contributeur » et « Lecteur ».
  - `security.py` : CSP stricte, verrouillage, TOTP. `bugs.py` : signalements (`BugReport`, table modifiable, pas une trace).
  - `management/commands/` : `secure_db` (droits PostgreSQL), `verify_chain`, `audit_event`, `bootstrap_admin`.
- `deploy/` : `compose.yaml` (db, migrate à usage unique, app), `compose.caddy.yaml` (Caddy intégré) ou `compose.port.yaml` (derrière le proxy du serveur), `entrypoint.sh`, et `logit` (commande d'exploitation installée dans `/usr/local/bin`).
- `install.sh` : installe, ou met à jour si LogIT tourne déjà (il lance alors `logit update` de la version cible). Installation neuve : 1. automatisée (aucune question, HTTPS sur le port 6720) ou 2. manuelle (adresses, port, ou proxy du serveur).

## Invariants à ne jamais casser

- **Rien ne se modifie ni ne se supprime dans les traces.** Déclencheurs `logit_refuse_change` (migrations 0002, 0003) sur `journal_intervention`, `journal_version`, `journal_version_elements`, `journal_attachment`, `journal_auditevent` ; le compte `logit_app` n'a que SELECT et INSERT. Une fiche s'annule, un élément s'archive, un compte se désactive.
- **Toute nouvelle table de traces** reçoit les déclencheurs (migration `RunSQL`) **et** figure dans `APPEND_ONLY` de `secure_db.py`. Une migration ajoute des colonnes, elle ne réécrit pas les lignes des tables de traces.
- **Ne jamais changer le calcul d'empreinte des champs existants** (`Version.payload`, `AuditEvent.payload`). Une nouvelle clé s'ajoute seulement si elle est renseignée (comme `attachments`, `category`, `rollback_of`), sinon toutes les fiches existantes deviennent « altérées ».
- **Le mot de passe propriétaire PostgreSQL n'est jamais dans le conteneur `app`** : seul le service `migrate` le reçoit.
- **CSP** : aucun script ni style en ligne, aucun attribut `style=""` dans les gabarits (vérifié par `test_aucun_style_ni_script_en_ligne_dans_les_gabarits`). Icônes en SVG dans la page.
- **Une mise à jour ne perd jamais de données** : sauvegarde avant, retour automatique (code, `.env`, base) en cas d'échec.
- `install.sh` : `LOGIT_DEFAULT_REF` pointe sur la branche elle-même pendant les tests, sur le tag à la publication ; `LOGIT_DEFAULT_COMMIT` reçoit l'empreinte du commit du tag dans un commit suivant sur `main`.
