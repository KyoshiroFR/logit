# Feuille de route

Chemin jusqu'à la mise en production (`v1.0.0`). Chaque point se discute avant d'être codé ; les propositions non encore validées sont marquées *à valider*.

## v0.2.0 — Première version publiée

- Tag `v0.2.0`, `LOGIT_DEFAULT_REF` sur le tag puis `LOGIT_DEFAULT_COMMIT` sur `main`.
- Installation réelle vérifiée sur Debian 12 et 13, amd64 et arm64, avec Docker puis podman.
- Mise à jour vérifiée depuis cette version, retour automatique compris.

## v0.3.0 — Usage par l'équipe

Quelques semaines d'usage réel. Les retours passent par les signalements intégrés et décident du contenu des versions suivantes.

## v0.4.0 — Preuves pour l'audit NIS2 *(à valider)*

- Export d'une période ou d'une sélection de fiches (PDF lisible et CSV), avec l'historique des versions et le résultat du contrôle d'intégrité.
- Export du journal de sécurité sur une période.

## v0.5.0 — Sauvegardes hors du serveur *(à valider)*

- Copie de la sauvegarde nocturne vers une autre machine (rsync/SSH ou S3), chiffrée.
- Ancrage externe de la chaîne d'empreintes : publier régulièrement la dernière empreinte hors de LogIT, pour qu'une base entièrement réécrite reste détectable.

## v0.6.0 — Prévenir l'équipe *(à valider)*

- Courriel facultatif (SMTP configuré dans `.env`) : fiche urgente à compléter, intervention planifiée qui approche, échec de sauvegarde ou d'intégrité.

## v0.7.0 — Carte des impacts

Calculer automatiquement les dépendances entre équipements et services, pour montrer ce qu'une intervention peut toucher au-delà des éléments cochés dans la fiche.

## v1.0.0 — Mise en production

- Aucune régression ouverte, `docs/regressions.md` à jour.
- Revue de sécurité complète (CSP, authentification, droits PostgreSQL, scripts d'installation).
- Documentation d'exploitation : installation, mise à jour, restauration testée.

## Plus tard *(à valider)*

- Connexion par l'annuaire de l'entreprise (LDAP ou OIDC).
- API en lecture seule pour relier LogIT à la supervision.
