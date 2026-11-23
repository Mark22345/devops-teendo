# Elevator Pitch – vázlat (kb. 2–3 perc)

## Diák / jelenetek

| # | Mit mutatsz | Kb. idő |
|---|---|---|
| 1 | Cím: „Teendőlista – egy push, és élesben van” | 10 mp |
| 2 | A probléma: kézi build/teszt/telepítés lassú és hibázásra hajlamos | 20 mp |
| 3 | Architektúra ábra (DOKUMENTACIO.md 3. fejezet) | 30 mp |
| 4 | **Élő demó:** kis módosítás → `git push` → Actions fül | 60 mp |
| 5 | A zöld deploy job füstteszt kimenete + Summary | 20 mp |
| 6 | Eredmény és továbbfejlesztés | 20 mp |

## Szövegjavaslat

> **(1–2)** Sziasztok! A projektem célja az volt, hogy egy alkalmazás a fejlesztő
> gépéről emberi beavatkozás nélkül, ellenőrzötten jusson el a futó környezetig. A kézi
> buildelés, tesztelés és telepítés lassú, és minden lépésnél hibázhatunk – ezt
> automatizáltam.
>
> **(3)** Az üzleti alkalmazás egy egyszerű teendőlista Pythonban: REST API és egy webes
> felület. A lényeg a pipeline: GitHub Actions-ben három lépés fut egymás után. Először
> lint és automatikus tesztek, lefedettség-küszöbbel. Utána a Docker image buildelése,
> ami egyben a telepíthető artifact – ezt konténerként rögtön ki is próbálom, és
> feltöltöm a GitHub Container Registry-be. Végül a pipeline létrehoz egy valódi
> Kubernetes sandbox clustert, telepíti oda az alkalmazást, és megvárja, hogy elinduljon.
>
> **(4)** Nézzük élőben: átírok egy szöveget, commit, push… és az Actions fülön már fut is
> a pipeline. Teszt, build, deploy.
>
> **(5)** A végén egy füstteszt a telepített alkalmazáson végigpróbálja az üzleti
> funkciókat: létrehoz, listáz, késznek jelöl, töröl egy teendőt, és ellenőrzi a
> hibakezelést. Ha ez zöld, a Definition of Done teljesült: az artifact fut a
> célkörnyezetben, és a funkciói elérhetők.
>
> **(6)** Az eredmény: egyetlen `git push`, és pár perc múlva ellenőrzött, verziózott
> kiadás fut Kubernetesen. Továbbfejlesztésként adatbázist, image-szkennelést és
> többlépcsős staging/production környezetet tervezek. Köszönöm a figyelmet!

## Videó felvételi tippek

- Képernyőfelvétel: Windows + G (Xbox Game Bar) vagy OBS Studio.
- A pipeline futása kb. 3–4 perc – a videóban vágd ki a várakozást, vagy előre futtatott
  eredményt mutass.
- Demóhoz jó módosítás: az `app/templates/index.html` címsorának átírása, majd a deploy
  után a füstteszt kimenetében a megváltozott verzió (`/health` → commit SHA).
