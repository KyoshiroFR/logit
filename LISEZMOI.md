# Outils de test LogIT

Branche à part, jamais fusionnée dans LogIT.

`fiches-fictives.py` crée quelques fiches marquées « [FICTIF] » sur une installation de test, par le vrai code de LogIT
(versions chaînées, capture, journal), pour vérifier qu'une mise à jour ne perd rien. En root sur le serveur de test :

    docker exec logit-app-1 logit-entrypoint shell -c "$(curl -fsSL https://raw.githubusercontent.com/KyoshiroFR/logit/outils-test/fiches-fictives.py)"

(Le script est passé en argument : envoyé par un tube, Django peut démarrer en mode interactif avant de le recevoir.)
