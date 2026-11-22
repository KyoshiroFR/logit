# Feuille de route

Chemin jusqu'à la mise en production (`v1.0.0`), par objectifs. Chaque version a un but et un critère d'atteinte ; les pistes ne sont qu'une manière possible d'y arriver et se discutent avant d'être codées. Les objectifs non encore validés sont marqués *à valider*.

## v0.2.0 — On peut installer LogIT en confiance

**Objectif** : n'importe qui installe une version figée de LogIT sur un serveur neuf et la met à jour sans risque.

**Atteint quand** :
- une installation neuve aboutit sur Debian 12 et 13, amd64 et arm64, avec Docker puis avec podman ;
- une mise à jour depuis cette version réussit, et un échec provoqué revient seul à l'état d'avant sans perte de données.

**Pistes** : tag `v0.2.0`, `LOGIT_DEFAULT_REF` sur le tag puis `LOGIT_DEFAULT_COMMIT` sur `main`.

## v0.3.0 — L'équipe consigne tout dans LogIT

**Objectif** : LogIT devient le seul endroit où l'équipe note ses interventions.

**Atteint quand** :
- pendant quatre semaines, chaque intervention de l'équipe a sa fiche ;
- les signalements reçus sont triés, et les gênes les plus citées corrigées ou inscrites ici.

## v0.4.0 — Un audit NIS2 se prépare en quelques minutes *(à valider)*

**Objectif** : fournir à un auditeur, sans aide, la preuve de ce qui a été fait sur une période.

**Atteint quand** : en moins de 5 minutes, un administrateur obtient pour une période donnée un document lisible des fiches (avec leurs versions) et du journal de sécurité, accompagné du résultat du contrôle d'intégrité.

**Pistes** : export PDF et CSV des fiches et du journal de sécurité.

## v0.5.0 — Les traces survivent à la perte du serveur *(à valider)*

**Objectif** : ni une panne, ni une compromission du serveur ne font disparaître ou réécrire les traces sans que cela se voie.

**Atteint quand** :
- après la destruction du serveur, LogIT est restauré ailleurs avec au plus un jour de traces perdu ;
- une base entièrement réécrite, chaîne d'empreintes recalculée comprise, est détectée.

**Pistes** : copie chiffrée de la sauvegarde nocturne vers une autre machine (rsync/SSH ou S3) ; dernière empreinte de la chaîne publiée régulièrement hors de LogIT.

## v0.6.0 — Rien d'important ne passe inaperçu *(à valider)*

**Objectif** : l'équipe est prévenue sans avoir à ouvrir LogIT.

**Atteint quand** : une fiche urgente restée à compléter, une intervention planifiée qui approche, ou un échec de sauvegarde ou d'intégrité déclenche une alerte reçue par les personnes concernées.

**Pistes** : courriel facultatif (SMTP configuré dans `.env`).

## v0.7.0 — On sait ce qu'une intervention peut casser

**Objectif** : avant d'intervenir, voir tout ce qui peut être touché, au-delà des éléments cochés dans la fiche.

**Atteint quand** : la fiche montre les équipements et services qui dépendent de ses éléments, calculés automatiquement.

**Pistes** : carte des impacts, à partir des dépendances entre équipements et services.

## v1.0.0 — LogIT est prêt pour la production

**Objectif** : LogIT peut servir de registre officiel de l'équipe.

**Atteint quand** :
- aucune régression n'est ouverte et `docs/regressions.md` est à jour ;
- une revue de sécurité complète (CSP, authentification, droits PostgreSQL, scripts d'installation) ne laisse aucun point bloquant ;
- une restauration complète a été faite en suivant uniquement la documentation.

## Plus tard *(à valider)*

- **Un seul compte pour tout** : se connecter avec l'annuaire de l'entreprise (LDAP ou OIDC).
- **LogIT parle à la supervision** : API en lecture seule.
