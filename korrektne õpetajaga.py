import random

names = ["Evelin", "Karl", "Kreete", "Lewis", "David"]  # sõitjad list
laps = 10  # Võisatlus pikkus, ringide arv
filename = "Result.txt"
file_header = "Ring;Nimi;Aeg:;Sektor;Sektor1;Sektor2;Viga\n"  # Faili esimene rida
results = []  # Tühi list ehk kogu võistluse aeg
minimum = 23  # väikseim sektori aeg k.a.
maximum = 26  # suurim sektori aeg k.a.
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
    for name in names:  # Kõikide isikutega  tuleb teha allolev tegevus
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
                this_lap = one_lap_time(minimum, maximum, name)
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