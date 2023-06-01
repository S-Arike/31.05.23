"""
kirjuta funktsioon ,mis arvutab juhusliku aja etteantud
vahemikus. Vahemik on sekundites ja kaasa arvatud.Lõpp
tulemusena näitab lisaks sekundile ja tuhandikke. Näiteks:
Kui vahemik on 47-59 sekundit, siis juhuslik aeg on 52.432 sekundit.
siis juhuslik aeg on 52.432 sekundit.
Tee list viie eesnimega kes võistlevad. Genereeri igale ühele
kolm sektori aega vahemikus 23 kuni 26 k.a. Väljasta iga isiku järgi
kolm aega.

Näiteks:
Lewis 25.12 25.286 25.935
Valtteri 25.96 26.858 26.993

Väljasta ajad ühel joonel. Nime max pikkus on 10 märki. Näiteks:
Lewis      25.12 25.286 25.935
Valtteri   25.96 26.858 26.993

Kõige esimeseks tuleb kogu aeg ja siis s1,s2,s3.
Lewis     72.778  25.12 25.286 25.935
Valtteri  77.952  25.96 26.858 26.993

Kogu aeg vormindada kujule 00:00:00.000 ehk 77.987 => 00:01:17.987
Lewis    00:01:15.414  25.12 25.286 25.935
Valtteri 00:01:12.485  25.96 26.858 26.993

Kirjuta funktsioon, mis arvutab täisringi aja kasutades esimeses
punktis tehtud funktsiooni  uue funktsiooni sees! Aegade vahemik
sektorites on sama ,mis alguses(23 ja 26). Sektori aeg sel korral
meeles pidama ei pea. Ainult täisringi aeg.

Nüüd kui on peaaegu kogu vajalik info olemas tuleb teha "Võistlus"
Võistlus on 10 ringi .Meeles tuleb pidada igal ringil sõitja aega(ringi)
ja kogu aega (sisse sõidetud ringinde summa ).Kogu info peab olema listis (nimi ja sõidetud ringide summa )
Kogu info peab olema listis (nimi ja sõidetud ringide aegade summa ). Kui info olemas näita lõpus lõpp tulemust.
Ära unusta listi sorteerida aja järgi kasvavalt.

Valtteri    00:08:18.204
Lewis       00:08:27.252

Võistlusel on ikka nii ,et kõik ringid ei tule hästi välja. Seega
mõnel ringil võiks juhtuda äpardus. See tähendab, et sektori aeg
poleks enam 23 ja 26 sek., vahel vaid 30 ja 90 sek. vahel ka. Enne
ringi aja arvutamist tehke lihtne loogiline kontroll. Genereerige
juhuslik number vahemikus 1-10 või 0-9 ja kui see number on 2,
siis juhtus midagi ja arvutage sektori aeg nüüd vahemikus 30-90 k.a.
Lewis       00:09:11.433
Valtteri    00:12:36.756

Sõit ja kõik "koperdamised" pane listi - ringi number. Ja kui
väljastatakse sõitja info, siis näita ringi numbreid kasutaja järgi.
Valtteri  00:08:17.793
Lewis     00:10:10.002 7 10

VÕIss

Valtteri  00:08:17.793 []
Lewis     00:10:10.002 [7, 10]

Arvuta alates teisest sõitjast vahe esimesega. Aega näita
põhiaja järgi enne vigaseid ringide numbreid näiteks:
Evelin    00:08:17.793 []
Lewis     00:10:10.002  00:00:09.182[]
Sten      00:09:04.019  00:00:44.041[1]
Karl      00:09:38.634  00:01:18.656[3]
David     00:10:41.443  00:02:21.465[4, 5, 6]

Igal võidusõidul tuvastatakse ka kiirema ringi tegija (kolme sektori summa). Teie ülesandeks on tuvastada
kes on kiirema ringi teinud. Aega näita isiku järgi peale "koperdatud ringe".

Valtteri 00:12:23.430 [] 00:01:10.037
Lewis    00:14:51.852 00:02:28.422 [3]

Kiirema ringi teinud söitja ei pruugi olla köikides sektorites
kiirem. Ta ei pruugi üheski sektoris kiireim olla. Tuvastage
vöistluse kolme sektrori kiiremad ajad ja soitjad. Lisaks arvutage
lopus kokku klirema ringi aeg sektorite baasil ehk "unistuste ring"
Valtteri 00:12:24.200 [] 00:01:10.814
Lewis 00:16:12.296 00:03:48.096 [3, 10]

Sectors best
Sector 1 Nico       00:00:23.037
Sector 2 Lewis      00:00:23.007
Sector 3 Marko      00:00:23.068
Dream lap time: 00:01:09.112

Kogu võistluse info tuleb kirjutada txt (see on csv sisuga) faili.
Fail sisaldab allolevat infot ja fail peab sisaldama päist.
Ajad on sekundites. Failinimi on Result.txt

Ring;Nimi;Aeg:Sektor1;Sektor2;Sektor3;Viga
1;Lewis;72.778;23.746;24.639;24.393;Jah
2;Nico;72.778;23.746;24.639;24.393;Ei
"""

import random

racers = ["Evelin", "Karl", "Kreete", "Lewis", "David"]  # sõitjad list
laps = 10  # Võisatlus pikkus, ringide arv
filename = "Result.txt"
file_header = "Ring;Nimi;Aeg:;Sektor;Sektor1;Sektor2;Viga\n"  # Faili esimene rida
results = []  # Tühi list ehk kogu võistluse aeg
mini = 23  # väikseim sektori aeg k.a.
maxi = 26  # suurim sektori aeg k.a.
fastest_lap = ["Unknown", 999]  # kiirema ringi sõitja ja aeg
# kolme sektori kiiremad ajad eraldi
three_sectors = [["Unknown", 999], ["Unknown", 999], ["Unknown", 999]]
sectors_data = []  # Ühe ringi kolm sektorit (GLOBAALNE MUUTUJA)

def random_sector_time(mini, maxi):
    """Juhuslik sektori aeg ette antud vahemikus k.a."""
    thousandth = random.randint(0, 999) / 1000
    return random.randint(mini, maxi) + thousandth

def one_lap_time(mini, maxi, driver_name):
    """Ühele sõitjale  ühe ringi aeg (tagastatakse) s.h sektori ajad (globl.)"""
    this_total = 0  # Sektori  kokku liidetuna
    sectors_data.clear()  # Tühjenda sektori aegade massiiv. GLOBAALNE
    for z in range(3):  # Kolme sektori tegemiseks
        this_sector = random_sector_time(mini, maxi)  # Ühe sektori aeg
        if this_sector < three_sectors[z][1]:
            three_sectors[z][0] = driver_name  # sektori sõitja nimi
            three_sectors[z][1] = this_sector  # Uus sektori aeg
        this_total += this_sector  # Liidame sektori aja kogu ajale
        sectors_data.append(this_sector)  # Sektori kaupa listi
    return this_total  # Tagasta ringi aeg

def is_fastest_lap(driver_name , fastest_data):
    """Kas on kiireim ringi aeg ja sõitja. Väljastastuse juures vaja."""
    if driver_name == fastest_data[0]:
        return sec2time(fastest_data[1])  # Kiireima ringi vormindatud kujul
    else:
        return ""  # Pole kiireima ringi aeg

def sec2time(sec, n_msec=3):
    """ Convert seconds to 'D days, HH:MM:SS.FFF' """
    # https://stackoverflow.com/a/33504562
    if hasattr(sec, '__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec + 3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)


if __name__ == '__main__':
    f = open(filename, "w", encoding="utf-8")  # Ava fail üle kirjutamiseks
    f.write(file_header)  # Kirjuta faili päis
    for name in racers:  # Kõikide isikutega  tuleb teha allolev tegevus
        lap_times = 0  # Nullime isiku ringide arvuga
        errors = []  # Siia tulevad vigased/koperdamiste ringide numbrid
        for lap in range(laps):  # Hakkame sõitjale "ringe tegema"
            error = False  # Pole vigane/koperdatud ring
            if random.randint(0, 9) == 2:  # See on koperdatud ring
                # Ühe ringi aeg arvutatakse teisiti
                lap_times += one_lap_time(30, 90, "Unknown")
                errors.append(lap+1)  # Lisa ringi number listi
                error = True  # See on koperdatud ring
            else:  # See on tavaline ring
                this_lap = one_lap_time(mini, maxi, name)
                if this_lap < fastest_lap[1]:  # Kui ring on kiirem kui teadaolev
                    fastest_lap[0] = name  # Uue kiirema ringi sõitjha nimi
                    fastest_lap[1] = this_lap  # Uue ringi uus rekord
                lap_times += this_lap  # Liidame ringi aja kogu sõidu ajaga
            line = ';'.join([str(lap+1)] + [name] + [str(sum(sectors_data))] + [str(sectors_data[0])] +
                            [str(sectors_data[1])] + [str(sectors_data[2])] + [str(error)])
            f.write(line + "\n")  # KIrjuta rida faili reavahetusega
        results.append([name, lap_times, errors])  # Kirjuta vajalik info listi
    f.close()

    results = sorted(results, key=lambda  x: x[1])  # Sorteeri list aegade järgi
    print(results)  # Test sisu vaatamiseks

    # Näita info konsooli
    for idx, person in enumerate(results):
        if idx > 0:  # Alates teisest iskust
            difference = sec2time(person[1] - results[0][1])
            # Nimi, kogu sõidu aeg, erinevus esimesega, koperdatud ringid, kiireim ringi aeg, kui on
            print(person[0].ljust(10), sec2time(person[1], 3), difference, person[2], is_fastest_lap(person[0], fastest_lap))
        else:  # Ainult esimene isik
            # Nimi, kogu sõidu aeg, koperdatud ringid, kiireim ringi aeg, kui on
            print(person[0].ljust(10), sec2time(person[1], 3), person[2], is_fastest_lap(person[0], fastest_lap))

    print("Sektorite parimad")
    total = 0
    for idx, driver in enumerate(three_sectors):
        total += driver[1]  # Liida sektorite ajad kokku üheks ringiks
        # Näita sektori infot
        print("Sektor", (idx+1), driver[0].ljust(10), sec2time(driver[1]))
    print("Unelmate ring", sec2time(total))  # Unelmate ring