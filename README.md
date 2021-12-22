# GoPiGo

Autojen uusin, sekä demossa käytetty ohjelma: [AutoV6](https://github.com/KasperiRosengren/GoPiGo/blob/main/Auto/autoV6.py)

Backendillä pyörivää main ohjelma, joka komentaa autoja, sekä seuraa firebase tietokantaa [Server](https://github.com/KasperiRosengren/GoPiGo/blob/main/backend/env/programs/firebaseServer.py)

Ohjelmassa hyödynettiin python virtual enviromenttia, jotta ohjelma oli helpompi, sekä nopeampi siirtää koneelta toiselle. Tarvittavat kirjastot löytyvät backend/env/[requirements.txt](https://github.com/KasperiRosengren/GoPiGo/blob/main/backend/env/requirements.txt). Ne voi helposti asentaa komennolla:
```
pip install -r requirements.txt
```
Tärkeimpinä kirjastoina ovat paho-mqtt autojen hallintaan, sekä firebase-admin (Hyödyntää muita kirjastoja toiminnassaan.) tietokannan lukemiseen, sekä päivittämiseen.

GoPiGo autot olivat osana suurempaa projektia koululla, johon osallistui meidän lisäksi neljä muuta ryhmää. Ideana oli tehdä kauppa, jossa Pepper niminen humanoidirobotti toimii asiakaspalvelijana. Asiakkaat voivat ennakkoon tilata tuotteita puhelinsovelluksella, ja saapuessaan kauppaan he voivat lukea Pepperin näytöltä qr-koodin noutaakseen tuotteet. Kun asiakas tulee noutamaan tuotteitaan, luodaan firebasessa uusi noudettava tilaus, jonka jälkeen meidän autojen backendin main ohjelma jakaa vapaita autoja paketeille. Pakettien tietoihin kytketään kuljettavan auton nimi, jotta käsivarsirobotti tietää nostaa paketin oikean auton katolle(Autojen katolla on qr-koodi id:t.), jonka jälkeen käsi vaihtaa paketin tilaa tietokannassa lastatuksi, jolloin auto lähtee ajamaan purku pisteelle. Kun kaikki paketit on saaatu vietyä perille, ilmoittaa käsivarsirobotti siittä Pepperiä, joka sen jälkeen ohjaa asiakkaan noutamaan tuotteensa.



Meidän ryhmän jäsenet:
- Kasperi Rosengren
- Antti-Matias Tuovinen
- Kai Kaarteenaho
