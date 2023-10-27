#   #! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Consideriamo la codifica posizionale di un numero in base B.
Date le N cifre:      a_{N-1} .... a_1 a_0
Il valore del numero si ottiene sommando, per ogni indice i
da 0 ad N-1, i valori a_i*B^i .

Esempio: se la base B=6  e il numero è     (52103)_6
Il suo valore sarà    5*6^4 + 2*6^3 + 1*6^2 + 0*6^1 + 3*6^0 = (6951)_10

Generalizziamo questa notazione per usare basi diverse per ciascuna
posizione: avremo quindi una lista "bases" formata da N basi e un
numero formato da N cifre contenute in una lista di nome "digits".
Per l'esempio sopra avremo: bases = [6, 6, 6, 6, 6] digits = [5, 2, 1,
0, 3]. Le cifre sono tali che ciascuna sia minore della base nella
stessa posizione.  Il valore del numero in base 10 si ottiene come
nella conversione iniziale, usando per la potenza i-esima la base
i-esima della lista.

NOTA: per comodità useremo nel codice delle liste di cifre e di basi
in cui l'esponente della potenza corrisponde all'indice nelle liste.
Quindi ciascuna lista conterrà basi e cifre a partire dalle unita'.

NOTA: Il numero di basi N e' maggiore stretto di 1. I valori delle
basi anche esse sono maggiori di 1.

In base a quanto detto, data in ingresso una lista "bases",
un obiettivo dell'HW e' genera la lista di tutte le possibili
combinazioni valide di cifre rappresentabili con quelle basi.

Esempio: se in ingresso bases vale [2, 5], tutte le combinazioni sono:
[[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4]]

infatti:
- nella prima cifra ci sono solo valori fra [0, 1] perche' la base e' 2
- nella seconda cifra ci sono solo valori fra [0, 4] perche' la base e' 5.

Ciascuna combinazione rappresenta un intero che va convertito da lista
a intero secondo la base specificata in "bases". Una volta che tutte
le possibili combinazioni sono state convertite in un intero e'
necessario trovare quali interi hanno piu di una rappresentazione
nelle basi date.

Esempio: Se in ingresso bases vale [4, 3, 2] allora gli interi che 
ammetto piu di una rappresentazione sono {3, 4, 5, 6, 7, 8, 9, 10}

Infatti, ad esempio il numero 10 con queste basi ha le due rappresentazioni 
    [3, 1, 1] -> 3*4^0 + 1*3^1 + 1*2^2 = 10
    [0, 2, 1] -> 0*4^0 + 2*3^1 + 1*2^2 = 10

Il problema e' gia' stato diviso in sottoproblemi e dovete realizzate
quindi le funzioni che seguono:
 - decode_digits, e' la funzione piu semplice e basilare che riceve
   una lista di basi e una lista di digits e la converte in intero.
 - generate_digits, e' la funzione che fa la maggior parte del lavoro
   che data una lista di basi, calcola tutte le combinazioni.
 - find_doubles, e' l'ultima funzione che date le combinazioni trova i
   corrispettivi interi che hanno piu di una rappresentazione.

Il Timeout applicato è 0.5 secondi.

ATTENZIONE: è vietato importare altre librerie oltre quelle già presenti.
"""

from typing import List, Set


def decode_digits(digits: List[int], bases: List[int]) -> int:
    """
    Riceve una lista di cifre ed una lista di basi della stessa lunghezza.
    Calcola il valore intero che corrisponde come spiegato prima.
    Parameters
    digits : List[int]    lista di cifre da convertire
    bases   : List[int]    lista di basi della stessa lunghezza
    Returns
    int                    il valore intero corrispondente

    Esempio: decode_digits( [1, 1, 2], [2, 3, 4] ) -> 36
        infatti   1*2^0 + 1*3^1 + 2*4^2 = 36
    """
    # SCRIVI QUI IL TUO CODICE
    sum = 0
    for i in range(len(digits)):
        sum += digits[i] * (bases[i] ** i)

    return sum


def generate_digits(bases: List[int]) -> List[List[int]]:
    """
    Data una lista di basi, genera la lista di tutte le possibili
    combinazioni di cifre compatibili con le basi date.  Ciascuna
    combinazione è una lista di cifre compatibili.  Ovvero per
    ciascuna posizione che corrisponde a una base B contiene una delle
    possibili cifre in [0..B-1]

    Esempio:  generate_digits([2, 5]) produce la lista
    [ [0, 0], [1, 0], [0, 1], [1, 1], [0, 2], [1, 2], [0, 3], [1, 3], [0, 4], [1, 4] ]

    Nota: l'ordine nella lista finale non conta e anche
    [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4]]
    è una soluzione valida.
    """
    # SCRIVI QUI IL TUO CODICE
    compatible_digits = []

    able_digits = []
    for b in bases:
        base_digits = []
        for i in range(b):
            base_digits.append(i)
        able_digits.append(base_digits)
    # permutazioni di n(len(basis))  liste
    perm = 0
    for i in range(len(able_digits)):
        for c in range(len(able_digits[1])):
            perm += 1
    compatible_digits = able_digits[0]
    if len(able_digits) > 1:
        for i in range(1, len(able_digits)):
            compatible_digits = permutation(compatible_digits, able_digits[i])

    return compatible_digits


def permutation(list_a: List[int], list_b: List[int]) -> List[List[int]]:
    # dati 2 array fare le permutazioni
    lst = []
    for i in range(len(list_a)):
        for j in range(len(list_b)):
            if isinstance(list_a[i], list):
                temp = []
                # devo instanziare un nuovo array per non modificare quello iniziale
                for z in list_a[i]:
                    temp.append(z)
                temp.append(list_b[j])
                lst.append(temp)
            else:
                lst.append([list_a[i], list_b[j]])
    return lst


def find_doubles(bases: List[int]) -> Set[int]:
    """
    Data una lista di basi, genera la lista di tutte le possibili
    combinazioni valide di cifre rappresentabili con quelle basi,
    converte ciascuna combinazione nell'intero corrispondente e cerca
    quali interi appaiono più volte.

    Ritorna l'insieme di valori interi che hanno più di una
    rappresentazione nelle basi date.

    Esempio: find_doubles([4, 3, 2]) -> {3, 4, 5, 6, 7, 8, 9, 10}
    Infatti, ad esempio il numero 10 con queste basi ha le due rappresentazioni
    [3, 1, 1] -> 3*4^0 + 1*3^1 + 1*2^2 = 10
    [0, 2, 1] -> 0*4^0 + 2*3^1 + 1*2^2 = 10
    """
    # SCRIVI QUI IL TUO CODICE
    set1 = []
    # genera la lista di tutte le possibili combinazioni valide di cifre rappresentabili con quelle basi
    combination_list = generate_digits(bases)
    # converte ciascuna combinazione nell'intero corrispondente
    decoded_list = []
    for i in range(len(combination_list)):
        decoded_list.append(decode_digits(combination_list[i], bases))
    print("decoded:")
    print(decoded_list)
    # cerca quali interi appaiono più volte
    for d in range(len(decoded_list)):
        for j in range(d, len(decoded_list)):
            if d != j:  # caso in cui gli indici si equagliano, da evitare
                if decoded_list[d] == decoded_list[j]:
                    flag = True
                    for s in range(len(set1)):  # controlla se il numero è già presente
                        if decoded_list[d] == set1[s]:
                            flag = False
                    if flag:
                        set1.append(decoded_list[d])

    # insieme di valori interi che hanno più di una rappresentazione nelle basi date
    set1.sort()

    return set(set1)


###################################################################################
if __name__ == "__main__":
    # inserisci qui i tuoi test
    # se vuoi provare il tuo codice su piccoli dati
    # nota per eseguire questo main devi usare program.py
    # come cliente e non come modulo ossia con python program.py

    dd = decode_digits([1, 1, 2], [2, 3, 4])  # -> 36
    #  1*2^0 + 1*3^1 + 2*4^2 = 36
    if dd == 36:
        print("TEST1")

    print(generate_digits([2, 5]))

    print(find_doubles([4, 3, 2]))  # {3, 4, 5, 6, 7, 8, 9, 10}
