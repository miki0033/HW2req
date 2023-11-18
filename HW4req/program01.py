# #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajeje la bibliotecaria ha recentemente trovato una stanza nascosta
nella biblioteca di Keras (un posto fantastico situato in
Umkansa, il villaggio più grande delle Montagne Bianche).
Lì ha scoperto diversi libri contenenti
spartiti musicali di antiche canzoni Tarahumara e ha,
quindi, invitato un amico musicista a dare un'occhiata.
Il musicista le ha detto che è una scoperta sensazionale,
dato che gli spartiti sono scritti in notazione Tarahumara,
una popolazione ormai estinta, ma molto famosa per 
aver influenzato i musicisti della Sierra Nevada. Per poter
riprodurre i brani le suggerisce di farli tradurre in una
notazione familiare ai musicisti Umkansaniani, ultimi
discendenti dei Tarahumara, in modo che possano riprodurli.

I Tarahumara scrivevano le note usando numeri invece di lettere:
0 al posto di A, 1 al posto di B e così via, fino a 7 al posto di G. 
Le note bemolle (b) e diesis (#)
(vedi la nota 3 sotto, se non sai cosa sono bemolle e diesis)
erano seguite rispettivamente da un - e da un + 
(ad esempio, 0- significa A bemolle). 
Inoltre, ripetevano semplicemente lo stesso numero più volte 
per rappresentare la durata della nota. 
Ad esempio, 0000 significa che la nota A ha una lunghezza di 4, 
mentre 0-0-0-0- significa che la nota A bemolle ha una lunghezza di 4.

Le pause venivano scritte come spazi:
ad esempio, dodici spazi rappresentano una pausa lunga 12. 
Sia le note che le pause potevano estendersi su
diverse linee della partitura (ad esempio, iniziando dalla linea
x e continuando sulla riga x+1, x+2 e così via).
Infine, gli spartiti musicali erano scritti da destra
a sinistra e dall'alto verso il basso, mentre andare accapo 
non significava nulla in termini di partitura musicale.

Gli Umkansaniani, invece, sono soliti scrivere le note utilizzando lettere,
e ogni nota è seguita dalla sua durata (quindi, l'esempio
sopra verrebbe scritto come A4). 
Le note bemolle e diesis sono seguite rispettivamente 
da una 'b' o da una '#' (ad esempio, A bemolle è scritto Ab, 
quindi l'esempio sopra verrebbe scritto ad Ab4). 
Le pause vengono scritte utilizzando la lettera P, seguita dalla 
loro durata e non viene utilizzato alcuno spazio.
Infine, gli Umkansaniani sono abituati a leggere la musica da
sinistra a destra, scritta su una singola riga.

Poiché Ajeje sa che sei un abile programmatore, 
ti fornisce una cartella contenente la trascrizione
di tutte le canzoni di Tarahumara che ha trovato, 
organizzate in più sottocartelle e file (un brano per file).
Inoltre, ha preparato un file indice in cui ogni riga
contiene il titolo di una canzone Tarahumara (tra virgolette),
seguito da uno spazio e dal percorso del file contenente
quella canzone (tra virgolette, relativa alla cartella principale).
Vorrebbe tradurre tutte le canzoni elencate nell'indice e 
salvarle in nuovi file, ciascuno denominato con il titolo 
della canzone che contiene (con estensione .txt),
in una struttura di cartelle corrispondente a quella originale.
Inoltre, vorrebbe archiviare nella cartella principale della
struttura creata un file indice contenente su ogni riga
il titolo di una canzone (tra virgolette) e la corrispondente
lunghezza del brano, separati da uno spazio. 
Le canzoni nell'indice devono essere ordinate per lunghezza decrescente e, 
se la durata di alcuni brani è la stessa, in ordine alfabetico ascendente. 
La durata di una canzone è la somma delle durate
di tutte le note e delle pause di cui è composta.

Sarai capace di aiutare Ajeje nel tradurre le canzoni
Tarahumara in canzoni Umkansaniane?

Nota 0: di seguito viene fornita una funzione per
Umkansanizzare le canzoni di Tarahumara; 
dopo essere stata eseguita, deve restituire un dizionario 
in cui ogni chiave è il titolo di una canzone
ed il valore associato è la durata del brano.

Nota 1: l'indice delle canzoni da tradurre è il file 'index.txt'
che si trova nella directory passata nell'argomento source_root

Nota 2: l'indice delle canzoni tradotte è il file 'index.txt'
che deve essere creato nella directory passata nell'argomento target_root

Nota 3: le note bemolle e diesis sono solo versioni "alterate".
di note regolari; per esempio un A# ("A diesis") è la
versione alterata di un A, cioè una nota A che è un
mezzo tono più alto del A regolare; lo stesso vale per
note bemolle, che sono mezzo tono più basse delle note normali;
dal punto di vista dei compiti, note bemolle e diesis
devono essere trattate allo stesso modo delle note regolari 
(ad eccezione della loro notazione).

Nota 4: Usiamo la notazione inglese delle note A B C D E F G.

Nota 5: potete usare le funzioni della libreria 'os' per creare le directory necessarie
(ad esempio os.makedirs)
"""

import os


"""
0 1 2 3 4 5 6 - +
A B C D E F G b #


il file index contiene i percorsi
salvare le canzoni in nuovi file denominati per titoloDellaCanzone.txt
mantenere la struttura file
fare un file index con "titolo"+ +lughezza_del_brano
ordinare le canzoni per lunghezza decrescente, a pari durata ordine alfabetico
durata+=durate_note+pause

RETURN: un dizionario chiave="titoloCanzone" valore=durata


"""

# ERRORI NEI TEST:
# [test10, test02, test04, test05, test07, test08]
# =>hanno un alberatura divera, quindi non viene discesa correttamente
# GLOBAL VARIABLE DETECTED


def Umkansanize(source_root: str, target_root: str) -> dict[str, int]:
    paths = readPathTarahumara(source_root)
    titleconverter = readIndexFile(source_root)
    songlist = {}
    for filename in paths:
        current_dir = os.getcwd()
        mypath = f"{current_dir}/{source_root}/{filename}"
        charlist = readFileTarahumara(mypath)
        if filename != "index.txt":
            traduction = translator(charlist)
            titolo = titleconverter[filename]
            status = saveFileUmkansanian(target_root, titolo, traduction)
            # print(titolo + ": " + str(status))  # restituisce true se va a buon fine

            durata = 0
            for n in traduction:
                if type(n) == int:
                    durata += n

            songlist[titolo] = durata
    createIndexFile(songlist, target_root)

    return songlist


def translator(arr: list[str]) -> list[str]:
    """caratteri ripeturi indicano la durata=> la durata deve diventare un numero
    spazio=pausa=P"""
    """0 1 2 3 4 5 6 - +
    A B C D E F G b #"""
    umkansan = []
    translate = {
        "0": "A",
        "1": "B",
        "2": "C",
        "3": "D",
        "4": "E",
        "5": "F",
        "6": "G",
        "-": "b",
        "+": "#",
        " ": "P",
        "0-": "Ab",
        "1-": "Bb",
        "2-": "Cb",
        "3-": "Db",
        "4-": "Eb",
        "5-": "Fb",
        "6-": "Gb",
        "0+": "A#",
        "1+": "B#",
        "2+": "C#",
        "3+": "D#",
        "4+": "E#",
        "5+": "F#",
        "6+": "G#",
    }
    durata = 1
    notaprev = ""

    arr = aggregazione(arr)
    for i in range(len(arr)):
        try:
            if notaprev != arr[i]:  # caso cambio di nota
                notaprev = arr[i]
                umkansan.append(translate[arr[i]])
                umkansan.append(durata)

            elif arr[i] == notaprev:  # caso stessa nota
                umkansan[len(umkansan) - 1] = int(umkansan[len(umkansan) - 1]) + 1

        except IndexError:
            break

    return umkansan


def aggregazione(arr: list[str]) -> list[str]:
    """
    aggrega i + e i - con la nota precedente
    RETURN: lista con gli elementi aggregati
    """
    result = []

    if not arr:  # Check if the input list is empty
        return result

    for i in range(len(arr)):
        try:
            if arr[i] == "+":
                result[len(result) - 1] += arr[i]
            elif arr[i] == "-":
                result[len(result) - 1] += arr[i]
            else:
                result.append(arr[i])

        except IndexError:
            print("errore: IndexError")
    return result


def readPathTarahumara(folder):
    """
    Controlla la cartella test01 e
    legge tutti i path presenti nella cartella e
    ne restituisce la lista
    """
    from os import listdir
    from os.path import isfile, join

    filelist = []
    current_dir = os.getcwd()
    mypath = f"{current_dir}/{folder}/"
    isdir = os.path.isdir(mypath)
    # print(mypath + ":" + str(isdir))
    if isdir:
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        filelist = onlyfiles
    else:
        print("FILE NON TROVATO-> path: " + current_dir + "/" + folder)

    return filelist


def readIndexFile(path) -> dict:
    res = []
    result = {}
    current = os.getcwd()
    try:
        file = open(current + "/" + path + "/index.txt", "r")
        line = file.readline()
        while line != "":
            res = line.split('" "')

            for l in range(len(res)):
                res[l] = res[l].replace('"', "")
                res[l] = res[l].replace("\n", "")

            result[res[1]] = res[0]

            line = file.readline()

    except FileNotFoundError:
        print("FILE NON TROVATO-> path: " + current + "/" + path + "/index.txt")

    return result


def readFileTarahumara(path) -> list[str]:
    """
    Deve leggere il file dal path indicato e trasformarlo in una list[str]
    Considerare che:spartito scritto al contrario e dall'alto verso il basso
    idea: fare lo splice in base a \n e leggere l'array al contrario
    RESTITUISCE la lista dei caratteri nel file
    """
    result = []
    file = open(path, "r")
    line = file.readline()
    while line != "":  # in python EOF non è null, è ""
        line = line.replace("\n", "")
        linelist = [*line]
        linelist.reverse()  # invertire la linea
        for nota in linelist:
            result.append(nota)
        line = file.readline()
    file.close()
    return result


def saveFileUmkansanian(destination: str, titolo: str, translation: list[str]) -> bool:
    """
    Parametri:
    destination= cartella di destinazione
    translation= testo da scrivere sul file come array di caratteri
    titolo = nome da dare al file

    Deve scrivere il file,
    salvare le canzoni in nuovi file denominati per titoloDellaCanzone.txt
    mantenere la struttura file

    ritorna true se la creazione del file è andata a buon fine, altrimenti false
    """
    # create destination if not exist
    current = os.getcwd()
    listdir = os.listdir()
    exist = False
    for dir in listdir:
        if dir == destination:
            exist = True
    if not exist:
        os.makedirs(current + "\\" + destination)

    # creo il file con il nome titolo.txt
    filename = str(titolo) + ".txt"
    f = open(filename, "w")

    # scrivo sul file i caratteri
    text = ""
    for nt in translation:
        text += str(nt)

    f.write(text)
    f.close()
    # sposto il file nella sua cartella
    try:
        os.remove(current + "\\" + destination + "\\" + filename)
    except FileNotFoundError:
        pass
    os.rename(current + "\\" + filename, current + "\\" + destination + "\\" + filename)
    # ritorno true se andato a buon fine
    return True


def createIndexFile(songlist: dict, destination: str) -> bool:
    """
    Si deve occupare di creare il file di index
    ordinare le canzoni per lunghezza decrescente, a pari durata ordine alfabetico

    """
    # creare il file
    current = os.getcwd()
    listdir = os.listdir()
    exist = False
    for dir in listdir:
        if dir == destination:
            exist = True
    if not exist:
        os.makedirs(current + "\\" + destination)

    filename = "index.txt"
    f = open(filename, "w")

    # ordinare le canzoni per lunghezza decrescente, a pari durata ordine alfabetico
    dizionario_ordinato = dict(sorted(songlist.items(), key=custom_sort))
    """
    print(dizionario_ordinato)
    for row in dizionario_ordinato:
        print(row)
    """
    text = ""
    for key, value in dizionario_ordinato.items():
        row = f'"{key}" {value}\n'
        print(row)
        text += row

    f.write(text)
    f.close()
    # spostarlo nella directory giusta
    try:
        os.remove(current + "\\" + destination + "\\" + filename)
    except FileNotFoundError:
        pass
    os.rename(current + "\\" + filename, current + "\\" + destination + "\\" + filename)
    # ritorno true se andato a buon fine
    return True


def custom_sort(item):
    # Se i valori sono uguali, ordina per chiave in ordine alfabetico
    return (-item[1], item[0])


if __name__ == "__main__":
    # paths = readPathTarahumara()

    # Umkansanize("Tarahumara", "Umkansanian")
    # current = os.getcwd()
    # folder = "test01"
    # destination = f"{folder}.out"
    # Umkansanize(folder, destination)

    # index = readIndexFile(folder)
    # print(index)
    """
    arr = [
        "0",
        "0",
        "0",
        "1",
        "-",
        "1",
        "-",
        "1",
        "2",
        "4",
        "+",
        "4",
        "+",
        "4",
        "+",
        "4",
        "+",
    ]
    res = translator(arr)
    print(res)"""

"""
    # readFileTarahumara("./test01/0.txt")

    arr = readFileTarahumara(
        "D:/Computer/Pc/HW2/HWreq/HW4req/test01/0.txt"
    )  # => D:\Computer\Pc\HW2\HWreq\HW4req\test01.expected\The alluring eel hops vacuum..txt
    res = translator(arr)
    print(res)

    """
