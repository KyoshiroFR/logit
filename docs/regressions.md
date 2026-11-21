# Comportements à ne pas casser

Ce fichier recense les comportements importants de LogIT et les tests qui les vérifient. Les tests sont dans `src/journal/tests.py`. Avant chaque commit, depuis `src/`, avec un PostgreSQL réel (variables dans `CLAUDE.md`) :

```bash
python manage.py test journal
```

Les comportements de la dernière section ne sont couverts par aucun test : à vérifier à la main quand on y touche.

## Traçabilité des fiches

| Comportement | Test |
|---|---|
| L'horodatage d'enregistrement est posé par le serveur ; une date envoyée par le navigateur est ignorée. | `InterventionTests.test_horodatage_serveur_ignore_les_valeurs_envoyees` |
| Motif, impact et retour arrière sont obligatoires, sauf en urgence : la fiche est alors « à compléter ». | `InterventionTests.test_champs_obligatoires_sauf_urgence` |
| Une date future n'est acceptée que pour une fiche planifiée. | `InterventionTests.test_date_future_reservee_aux_planifiees` |
| Au-delà de 15 minutes entre l'intervention et l'enregistrement, la fiche est signalée « saisie a posteriori ». | `InterventionTests.test_saisie_a_posteriori_signalee` |
| Une correction ajoute une version (auteur, motif obligatoire) et garde l'originale ; une correction de l'impact ou du retour arrière est signalée. | `InterventionTests.test_correction_cree_une_version_et_garde_l_originale` |
| Planifiée → réalisée → annulée : chaque étape est une nouvelle version ; une fiche annulée ne se corrige plus. | `InterventionTests.test_planifiee_puis_realisee_et_annulation` |
| Recherche plein texte et filtres (élément, période, catégorie). | `InterventionTests.test_recherche_et_filtres`, `InterfaceTests.test_filtrage_dynamique_renvoie_un_fragment` |
| Un retour arrière crée une fiche liée, préremplie (procédure, états inversés) ; il est refusé sur une fiche planifiée. | `RollbackTests.test_retour_arriere_lie_et_prerempli`, `RollbackTests.test_pas_de_retour_arriere_sur_une_planifiee` |
| « Depuis ta dernière visite » montre les versions des autres ; « marquer comme lu » ne saute pas celles arrivées entre-temps. | `SinceLastVisitTests` (2 tests) |

## Protection des traces

| Comportement | Test |
|---|---|
| PostgreSQL refuse UPDATE, DELETE et TRUNCATE sur les tables de traces. | `DatabaseProtectionTests.test_la_base_refuse_modification_et_suppression` |
| Le compte `logit_app` n'a que SELECT et INSERT sur les traces. | `DatabaseProtectionTests.test_le_compte_application_n_a_pas_les_droits` |
| La chaîne d'empreintes révèle une fiche falsifiée directement dans la base. | `DatabaseProtectionTests.test_la_chaine_revele_une_falsification` |
| Une capture est immuable ; une image remplacée dans la base est détectée. | `CaptureTests.test_capture_immuable_et_falsification_detectee` |
| Le calcul d'empreinte des fiches existantes ne change pas : une nouvelle clé n'est ajoutée que si elle est renseignée. | `CaptureTests.test_empreintes_2_0_inchangees_sans_capture_ni_retour`, `InterfaceTests.test_formulaire_elements_par_domaine_et_categorie_tracee` |
| La page Intégrité affiche le résultat et ce qui a été contrôlé (fiches, versions, captures, événements) ; chaque vérification est inscrite au journal. | `InterfaceTests.test_integrite_affiche_le_resultat_et_ce_qui_a_ete_verifie` |
| Le journal de sécurité reste intègre après la création de l'admin initial. | `AuthenticationTests.test_bootstrap_admin_et_journal_integre` |

## Captures

| Comportement | Test |
|---|---|
| Une capture est enregistrée, chaînée et servie dans un bac à sable (`sandbox`). | `CaptureTests.test_capture_enregistree_servie_et_chainee` |
| Seuls de vrais PNG, JPEG et WebP sont acceptés ; un faux fichier image est refusé. | `CaptureTests.test_fichier_qui_n_est_pas_une_image_refuse` |
| 10 captures au maximum par fiche. | `CaptureTests.test_limite_de_dix_captures_par_fiche` |
| Ajouter une capture seule est une correction (nouvelle version). | `CaptureTests.test_correction_par_simple_ajout_de_capture` |

## Comptes, rôles et sécurité

| Comportement | Test |
|---|---|
| Le lecteur consulte tout mais ne peut ni créer, ni corriger, ni annuler, ni administrer. | `InterventionTests.test_lecteur_consulte_sans_modifier` |
| Après trop d'échecs depuis une même IP (mot de passe, compte inconnu ou code TOTP), c'est l'IP qui est bloquée, jamais le compte : le même compte se connecte depuis une autre adresse. Blocage limité dans le temps et inscrit au journal. | `AuthenticationTests.test_verrouillage_de_l_ip_et_non_du_compte`, `AuthenticationTests.test_codes_totp_faux_bloquent_l_ip` |
| Chaque échec écrit une ligne pour fail2ban (date UTC, IP, motif fixe) sans aucun texte saisi : un identifiant forgé ne peut pas faire bannir une autre IP. | `AuthenticationTests.test_journal_fail2ban_sans_texte_saisi` |
| Mot de passe temporaire à changer, puis TOTP imposé ; 10 codes de secours à usage unique ; code TOTP rejoué refusé. | `AuthenticationTests.test_mot_de_passe_initial_puis_enrolement_totp_obligatoire` |
| Un admin crée un compte avec un mot de passe temporaire aléatoire, inscrit au journal. | `AuthenticationTests.test_creation_de_compte_par_admin` |
| Le dernier administrateur actif ne peut pas perdre son rôle. | `AuthenticationTests.test_dernier_admin_protege` |
| En-têtes de sécurité (CSP, `X-Frame-Options`), redirection HTTPS, `/sante/` accessible. | `AuthenticationTests.test_en_tetes_de_securite_et_sante` |
| CSP stricte : `script-src 'self'`, `style-src 'self'`, jamais `unsafe-inline`. | `InterfaceTests.test_csp_stricte_conservee` |
| Aucun style ni script en ligne dans les gabarits (attribut `style`, balise `<style>`, `<script>` sans `src`, gestionnaire `on…=`) : la CSP les bloquerait sans erreur visible. | `InterfaceTests.test_aucun_style_ni_script_en_ligne_dans_les_gabarits` |

## Registre et interface

| Comportement | Test |
|---|---|
| Bloc de fiche : état, « Impact à surveiller », résumé Cible / Avant / Après (première ligne), encart du retour arrière. | `InterfaceTests.test_bloc_resume_et_encart_rollback` |
| Un impact « Aucun » ne déclenche pas l'alerte ; un retour arrière manquant est signalé. | `InterfaceTests.test_aucun_impact_ne_declenche_pas_l_alerte_et_rollback_manquant_signale` |
| Le détail déployable est chargé à la demande (`/fiches/<n°>/apercu/`). | `InterfaceTests.test_detail_deploye_charge_a_la_demande` |
| États « Planifiée » et « En cours » selon la date prévue. | `InterfaceTests.test_etats` |
| « Absent jusqu'au » s'affiche sur les fiches de l'intervenant et disparaît une fois la date passée. | `InterfaceTests.test_absence_affichee_sur_les_fiches` |
| Saisie : éléments groupés par domaine ; la catégorie est tracée dans la version. | `InterfaceTests.test_formulaire_elements_par_domaine_et_categorie_tracee` |

## Signalement de bugs

| Comportement | Test |
|---|---|
| Signalement depuis la fenêtre (avec capture), inscrit au journal ; l'auteur voit sa capture. | `BugReportTests.test_signalement_en_direct_et_capture` |
| Un lecteur peut signaler, même sans JavaScript. | `BugReportTests.test_lecteur_peut_signaler_sans_javascript` |
| Erreurs renvoyées au formulaire ; faux fichier image refusé. | `BugReportTests.test_erreurs_renvoyees_et_fichier_piege_refuse` |
| Une page externe n'est pas enregistrée ; nombre de signalements limité par heure. | `BugReportTests.test_page_externe_ignoree_et_limite_horaire` |
| Suivi réservé aux admins ; un autre utilisateur ne voit pas la capture. | `BugReportTests.test_suivi_reserve_aux_admins` |
| L'issue GitHub préparée ne contient ni la capture ni la page concernée. | `BugReportTests.test_issue_github_sans_capture_ni_page_interne` |
| La fenêtre « Signaler un bug » est présente sur chaque page, sauf la page de signalement elle-même. | `BugReportTests.test_fenetre_presente_sur_chaque_page` |

## Non couverts par les tests

À vérifier à la main quand on modifie le code concerné.

- **Interactions JavaScript** (`logit.js`) : menu repliable de la barre du haut, indicateurs glissants, apparition progressive, compteurs des chiffres clés, filtrage sans rechargement, raccourci `/`, collage de capture avec Ctrl+V, fenêtre de signalement, état « Vérification… » de la page Intégrité. Tout doit aussi fonctionner sans JavaScript.
- **Code TOTP en 6 cases** : le vrai champ reste le seul à recevoir la saisie (collage, remplissage automatique) ; il redevient un champ normal pour un code de secours ; un code complet est envoyé seul, mais jamais au rechargement après un code refusé (sinon envoi en boucle et blocage de l'adresse IP).
- **`prefers-reduced-motion`** coupe toutes les animations (fin de `logit.css`).
- **Session de 8 heures**, fermée avec le navigateur ; mot de passe de 12 caractères minimum (`config/settings.py`).
- **Adresse IP du client** lue dans `X-Real-IP` (posé par le proxy de LogIT), sinon `REMOTE_ADDR` (`chain.py`). Chaque mode de proxy de l'installeur doit poser cet en-tête : sans lui, tous les utilisateurs partagent l'IP du proxy, et le blocage par IP bloquerait tout le monde.
- **Le mot de passe propriétaire PostgreSQL n'est jamais dans le conteneur `app`** : seul le service `migrate` le reçoit (`deploy/compose.yaml`).
- **Installation et mise à jour** (`install.sh`, `deploy/logit`) : aucun test automatique. Contrôles : `bash -n` et `shellcheck`, puis essai sur une Debian 12 ou 13. Points à préserver :
  - le code doit rester lisible par l'uid 10001 du conteneur (clonage en `umask 022`, `chmod -R go=rX /app` dans le Dockerfile) ;
  - le Caddy intégré garde `default_sni` (accès par IP sans SNI) ;
  - la ligne `listen [::]` de nginx n'est écrite que si IPv6 est actif ;
  - un site ajouté à nginx, Apache ou Caddy est retiré si le proxy refuse la configuration ;
  - une installation sans marqueur `.installed` est jugée vide et refaite ; avec le marqueur, elle n'est jamais effacée ;
  - une mise à jour fait une sauvegarde avant, refuse une version plus ancienne et revient automatiquement en arrière (code et base) si le démarrage échoue ;
  - sur une branche de test, `LOGIT_DEFAULT_REF` pointe sur la branche elle-même ;
  - pas de `docker compose up --wait` : `migrate` est à usage unique, on attend l'état « healthy » de `app` ;
  - fail2ban (`logit fail2ban`, appelé par l'installeur et après chaque mise à jour) : le filtre doit reconnaître les lignes de LogIT (`fail2ban-regex`) ; avec le Caddy intégré, le bannissement s'accroche au trafic « forward » (ports publiés par Docker), sinon à « input » ; une règle refusée par fail2ban est retirée ; un fichier fail2ban qui n'est pas à LogIT n'est jamais écrasé ; `/var/log/logit` appartient à l'uid 10001 et existe avant le démarrage du conteneur.
