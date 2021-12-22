# GoPiGo

Autojen uusin, sekä demossa käytetty ohjelma: [AutoV6](https://github.com/KasperiRosengren/GoPiGo/blob/main/Auto/autoV6.py)

Backendillä pyörivää main ohjelma, joka komentaa autoja, sekä seuraa firebase tietokantaa [Server](https://github.com/KasperiRosengren/GoPiGo/blob/main/backend/env/programs/firebaseServer.py)

Ohjelmassa hyödynettiin python virtual enviromenttia, jotta ohjelma oli helpompi, sekä nopeampi siirtää koneelta toiselle. Tarvittavat kirjastot löytyvät backend/env/[requirements.txt](https://github.com/KasperiRosengren/GoPiGo/blob/main/backend/env/requirements.txt). Ne voi helposti asentaa komennolla:
```
pip install -r requirements.txt
```
Tärkeimpinä kirjastoina ovat paho-mqtt autojen hallintaan, sekä firebase-admin (Hyödyntää muita kirjastoja toiminnassaan.) tietokannan lukemiseen, sekä päivittämiseen.
