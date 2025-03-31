import cssutils, os, bs4, json

def get_html():
    with open("index.html", encoding="utf-8") as f: #HTML fájl beolvasása
        return bs4.BeautifulSoup(f, 'html.parser') #Visszadobás egyben
    
def get_css():
    with open("style.css", encoding="utf-8") as f: #CSS fájl beolvasása
        css = cssutils.parseString(f.read())
        return [x for x in css.cssRules if x.type == x.STYLE_RULE]#Visszadobás egyben

def test_file_structure():
    expected = ["index.html",
                "style.css", 
                "szoveg.txt", 
                "hetfo_csirkecomb.jpg", 
                "kedd_makosteszta.jpg", 
                "szerda_halaszle.jpg", 
                "csutortok_rantotthus.jpg",
                "pentek_borsofozelek.jpg"] #Az elvárt fájlstruktúra
    
    files = os.listdir("./") #Helyi fájlok listája
    for f in expected:
        assert files.__contains__(f), f"A hiányzik a(z) {f} fájl!" #Az elvárt és jelenlegi struktúra összehasonlítása, ha hiányzik a jelenlegiből akkor AssertionError

#Fájlok beolvasása/átalakítása
html_soup = get_html() #bs4 html oldal
css_list = get_css() #cssutils lista

#Megjegyzések:
#Ha CSS-t kell ellenőrizni, a GetPropertyValue függvényt csináltam hozzá.
#Egyszerű a használata: Az első paramétere a css selector, a második a tulajdonság,
#és ha mind a kettő létezik, akkor visszadobja az értéket, amit lehet assert-el ellenőrizni.

#Ha HTML-t kell ellenőrizni, akkor a html_soup.find-al lehet
#elementet keresni, első paramétere az element típusa.
#A második paramétere lehet class, id, stb.
#A class-okat (és gondolom az id-kat is) listaként dobja vissza,
#szóval az első elemre kell ellenőrizni, ha csak egy class van megadva.
#A .name tulajdonság az element típusát adja vissza.
#Az elementek pozícióját személy szerint én az előző/következő elementekkel ellenőrzöm,
#és ha kell akkor a parent/children-el is.

def GetPropertyValue(selector: str, propName: str):
    assert any(x for x in css_list if x.selectorText == selector), f"Nincs {selector} osztály!" #Osztály létezés ellenőrzés
    assert next(x for x in css_list if x.selectorText == selector).style.getPropertyValue(propName), f"Nincs {propName} tulajdonság!" #Tulajdonság ellenőrzés az osztályban
    return next(x for x in css_list if x.selectorText == selector).style.getPropertyValue(propName) #Tulajdonság értékének visszadobása

#Feladatok
def test_feladat_1():
    assert GetPropertyValue("body", "color") == "#006", "Helytelen az oldal betűszíne!"
    assert GetPropertyValue("body", "background-color") == "#EF6", "Helytelen a beállított háttérszín!"

def test_feladat_2():
    assert GetPropertyValue("body", "font-style") == "italic", "Nincs dőlt beállítás az oldalon!"

def test_feladat_3():
    assert GetPropertyValue("body", "width") == "50%", "Helytelen az oldal szélessége!"
    assert GetPropertyValue("body", "margin") == "auto", "Nincs középre igazítva az oldal!" 

def test_feladat_4():
    assert html_soup.find("h1") != None, "Nem létezik egyes szintű fejezetcím!"
    assert html_soup.find("h1").text == "Heti étlap", "Helytelen a cím szövege!"
    #Meg kell nézni, hogy hol van pontosan a h1, ebben az esetben a body-nak 
    #konkrét leszármazottja, és az első. (Mindkettőt tudja a bs4)

def test_feladat_5():
    assert html_soup.find(class_="hetek") != None, "Nem létezik hetek osztály az oldalon!"
    assert html_soup.find(class_="hetek").name == "div", "A hetek osztályú elem nem div!"

def test_feladat_6():
    elems = [("a", "Előző hét"),
             ("span", "Aktuális hét"),
             ("a", "Következő hét")]
    
    target = html_soup.find(class_="hetek")
    assert isinstance(target, bs4.Tag), "Nincs hetek osztályú elem!"
    
    for tag, text in elems:
        assert target.find(name=tag) != None, f"Nem létezik {tag} típusú elem a .hetek div-ben!"
        assert target.find(name="span") != None, f"Nem létezik olyan elem a .hetek div-ben, aminek a szövege '{text}' lenne!"

def test_feladat_7():
    assert GetPropertyValue(".hetek", "display") == "flex", "Nincs flex rendezés a .hetek kiválasztón!"
    assert GetPropertyValue(".hetek", "justify-content") == "space-evenly", "Helytelen a rendezés módja!"

def test_feladat_8():
    assert GetPropertyValue("hr", "background-color") == "red", "Helytelen/hiányzik a háttérszín beállítás!"
    assert GetPropertyValue("hr", "border-color") == "red", "Helytelen/hiányzik a szegélyszín beállítás!"

def test_feladat_9():
    prev_sibl = None #Előző element
    target = None #Keresett element
    next_sibl = None #Következő element
    
    target = html_soup.find("hr")

    assert isinstance(target, bs4.Tag), "Nem található hr elem az oldalon!"

    prev_sibl = target.find_previous_sibling()
    next_sibl = target.find_next_sibling()

    assert prev_sibl.get("class")[0] == "hetek", "Helytelen a hr elem elhelyezése!"
    assert next_sibl.name == "hr", "Hiányzik a második hr elem!"

def test_feladat_10():
    target = None

    target = html_soup.find(class_="egynap")

    assert isinstance(target, bs4.Tag), "Nincs egynap osztályú elem!"

    children = target.findChild("div")

    assert target.name == "div", "Az egynap osztályú elem nem div típusú!"
    assert target.find_previous_siblings()[0].name == "hr", "Helytelen az egynap elem elhelyezése!"
    assert target.find_previous_siblings()[1].name == "hr", "Helytelen az egynap elem elhelyezése!"

    assert children.name == "div", "Nem div az egynap elem első eleme!"
    assert children.find_next_sibling().name == "img", "Nem img az egynap elem második eleme!"

def test_feladat_11():
    target = None
    
    target = html_soup.find(class_="egynap")
    assert isinstance(target, bs4.Tag), "Nincs egynap osztályú elem!"

    assert GetPropertyValue("egynap", "justify-content") == "space-between", "Helytelen az elrendezés módja, nem CSAK az elemek között van hely!"

def test_feladat_12():
    target = None #Keresett elem
    prev_sibl = None #Keresett elem előbbi testvéreleme
    next_sibl = None #Keresett elem utóbbi testvéreleme

    #Összes egynap osztályú div elem keresése
    assert len(html_soup.find_all(name="div", class_="egynap")) == 5, "Helytelen számú 'egynap' osztályú div van az oldalon!"
    
    haystack = html_soup.find_all(name="div", class_="egynap") #Összes egynap div

    for div_count in range(5): #5 db div-nek kell lennie
        target = haystack[div_count] #Jelen egynap elem
            
        if (div_count == 4): #Utolsó egynap div
            prev_sibl = target.find_previous_sibling() #Előző testvérelem
            next_sibl = target.find_next_sibling() #Következő tetvérelem

            assert prev_sibl.name == "hr", f"Nem jó helyen van az utolsó egynap div!" #Az előtte lévő elem hr kell, hogy legyen
            assert next_sibl == None, f"Nem jó helyen van az utolsó egynap div!" #Utána nem lehet semmi
        else: #Ha nem az utolsó egynap-ot keressük, akkor előtte és utána is hr elemnek kell lennie
            prev_sibl = target.find_previous_sibling() #Előző testvérelem
            next_sibl = target.find_next_sibling() #Következő tetvérelem

            #Ha előtte ÉS utána is hr van, csak akkor jó
            assert prev_sibl.name == "hr", f"Helytelen az egynap div-ek elrendezése!" 
            assert next_sibl.name == "hr", f"Helytelen az egynap div-ek elrendezése!"

def test_feladat_13():
    #egynap div-ben kép szélesség ellenőrzés
    assert GetPropertyValue("egynap img", "width") == "230px", "Nem megfelelő az egynap div-ben lévő kép szélessége!"

def test_feladat_14():
    #Jobb és baloldali margó ellenőrzése
    assert GetPropertyValue("egynap", "margin-left") == "15%", "Nem megfelelő a bal oldali margó értéke!" 
    assert GetPropertyValue("egynap", "margin-right") == "15%", "Nem megfelelő a jobb oldali margó értéke!"

def test_feladat_15():
    menu = [
    ("hétfő", "Újházi tyúkhúsleves", "Sült csirkecomb, rizi-bizi", "Túró rudi"),
    ("kedd", "Babgulyás", "Mákos tészta", "Alma"),
    ("szerda", "Ponty halászlé", "Rakott burgonya", "Szőlő"),
    ("csütörtök", "Csontleves", "Bécsi szelet, sült burgonya", "Uborkasaláta"),
    ("péntek", "Tojásleves", "Borsófőzelék, sült virsli", "Kókuszgolyó")]


#Tesztek futtatása és kiértékelése
tests = [
    {"name": "1. feladat", "func": test_feladat_1, "points": 1},
    {"name": "2. feladat", "func": test_feladat_2, "points": 1},
    {"name": "3. feladat", "func": test_feladat_3, "points": 1},
    {"name": "4. feladat", "func": test_feladat_4, "points": 2},
    {"name": "5. feladat", "func": test_feladat_5, "points": 2},
    {"name": "6. feladat", "func": test_feladat_6, "points": 2},
    {"name": "7. feladat", "func": test_feladat_7, "points": 1},
    {"name": "8. feladat", "func": test_feladat_8, "points": 1},
    {"name": "9. feladat", "func": test_feladat_9, "points": 1},
    {"name": "10. feladat", "func": test_feladat_10, "points": 2},
    {"name": "11. feladat", "func": test_feladat_11, "points": 1},
    {"name": "12. feladat", "func": test_feladat_12, "points": 2},
    {"name": "13. feladat", "func": test_feladat_13, "points": 1},
    {"name": "14. feladat", "func": test_feladat_14, "points": 1}
]

test_results = []
total_score = 0

for test in tests:
    try: #Ha sikeres, megkapja a pontokat
        test["func"]()  #Függvény lefuttatása
        status = "passed" #'passed' státusz sikeres futásnál 
        total_score += test["points"] #Elért pontszám növelése a feladat pontszámával
    except AssertionError: #Ha a feladat hibás
        status = "failed" #'failed' státusz

    test_results.append({
        "name": test["name"],
        "status": status,
        "score": test["points"] if status == "passed" else 0,
        "max_score": test["points"]
    }) #A kiírásra kerülő listához adás


# JSON-ba írás
with open("results.json", "w", encoding='utf-8') as f:
    json.dump(test_results, f, ensure_ascii=True)