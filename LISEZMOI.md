# Outils de test LogIT

Branche à part, jamais fusionnée dans LogIT.

`fiches-fictives.py` crée quelques fiches marquées « [FICTIF] » sur une installation de test, par le vrai code de LogIT
(versions chaînées, capture, journal), pour vérifier qu'une mise à jour ne perd rien. En root sur le serveur de test :

    curl -fsSL https://raw.githubusercontent.com/KyoshiroFR/logit/outils-test/fiches-fictives.py | docker exec -i logit-app-1 logit-entrypoint shell
