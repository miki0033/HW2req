#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Il tuo caro amico Pico de Paperis ti ha mandato un messaggio molto strano scarabocchiato su una cartolina.
Ê da tanto che non lo vedi e da sempre vi divertite a scrivervi in codice.
Per decodificare il suo messaggio vai a cercare nella tua biblioteca un libro un po' particolare,
il cifrario di Archimede Pitagorico. Il cifrario da applicare è la famosa "Cifra del Faraone".
La decifrazione col metodo del Faraone si basa su delle regole di sostituzione di sequenze di simboli nel testo.
Il motivo per cui si chiama "cifra del Faraone" è che in antico Egizio le sequenze formate da più geroglifici
potevano essere scritte in qualsiasi ordine, quindi ogni anagramma delle sequenze era valido.
Per rendere la cosa più strana, Pico de Paperis ha deciso di usare un cifrario che non è esattamente quello del
Faraone, ma una sua variante. Invece di usare gli anagrammi usa dei "quasi anagrammi", cioè anagrammi che nel testo
originale hanno un carattere spurio in più rispetto alla sequenza cercata.
Nel cifrario sono contenute coppie di sequenze che indicano come trasformare il testo.
Ad esempio la coppia 'shampoo' -> 'soap' corrisponde a cercare un punto del messaggio in cui appare la sequenza 'shampoo'
(o un suo anagramma) ma con un carattere in più (ad esempio 'pmQohaso') e sostituirla con la sequenza 'soap'.

La decodifica del messaggio può portare a più possibili messaggi finali, perchè possono esserci più sequenze nel testo
che possono essere trasformate in ogni momento e l'ordine delle trasformazioni influenza le trasformazioni successive.
Ad un certo punto succederà che nessun "quasi-anagramma" delle sequenze del cifrario è presente in nessun punto
della sequenza di simboli per cui non è più possibile fare trasformazioni.
Queste sequenze le chiamiamo sequenze finali.
Di tutte le possibili sequenze finali,ci interessa l'insieme delle più corte.

Per decodificare il messaggio di Pico de Paperis devi implementare la funzione
pharaohs_revenge(encrypted_text : str, pharaohs_cypher : dict[str,str]) -> set[str]:
che riceve come argomenti:
- il testo che ti ha mandato Pico de Paperis, come stringa di simboli (caratteri)
- il cifrario da applicare, un dizionario che ha come chiavi le sequenze di cui cercare nel testo un quasi-anagramma
   e come valore associato la stringa da sostituire al quasi-anagramma trovato.
la funzione deve tornare l'insieme dei più brevi testi ottenibili applicando ripetutamente
le trasformazioni fin quando non è più possibile applicarne nessuna.

Esempio:
encrypted_text  = 'astronaut-flying-cyrcus'
pharaohs_cypher = {'tuar': 'me', 'cniy': 'op', 'sorta': 'tur', 'fult': 'at', 'rycg': 'nc'}

Risultato: {'tmeopcus', 'metopcus', 'ameopcus', 'atmepcus'}
e tutte le trasformazioni applicate sono quelle contenute nel file example.txt
(in ordine alfabetico e senza ripetizioni)

NOTA: almeno una delle funzioni o metodi che realizzate deve essere ricorsiva
NOTA: la funzione/metodo ricorsivo/o deve essere definita a livello più esterno
      altrimenti fallirete il test di ricorsione.
"""

import tree


def pharaohs_revenge(encrypted_text: str, pharaohs_cypher: dict[str, str]) -> set[str]:
    root = tree.Tree(None)
    recursive_decypher(root, encrypted_text, pharaohs_cypher)
    leafsvalue = set()
    check_leaf_value(root, leafsvalue)
    minimum = float("inf")
    result = set()
    for value in leafsvalue:
        if value != None:
            if minimum > len(value):
                result.clear()
                minimum = min(minimum, len(value))
            if minimum == len(value):
                result.add(value)

    return result


def recursive_decypher(node, text, cypher):
    for key, value in cypher.items():
        letters_to_replace = [*key]

        for i in range(len(text)):
            sublen = len(letters_to_replace) + 1
            preText = text[:i]
            subtext = text[i : i + sublen]
            postText = text[i + sublen :]
            flagpos = [-1]
            flag = True
            for letter in letters_to_replace:
                subpos = subtext.find(letter)
                if subpos == -1:
                    flag = False
                elif flagpos[0] == -1:
                    flagpos[0] = subpos + i
                else:
                    flagpos.append(subpos + i)
            if flag:
                subtext = value
                modtext = preText + subtext + postText
                tree_node = tree.Tree(modtext)
                node.AddChild(tree_node)
                recursive_decypher(tree_node, modtext, cypher)


def check_leaf_value(node, leafsvalue):
    if node.isLeaf():
        leafsvalue.add(node.value)
    for child in node.children:
        check_leaf_value(child, leafsvalue)


if __name__ == "__main__":
    encrypted_text = "astronaut-flying-cyrcus"
    pharaohs_cypher = {
        "tuar": "me",
        "cniy": "op",
        "sorta": "tur",
        "fult": "at",
        "rycg": "nc",
    }
    result = pharaohs_revenge(encrypted_text, pharaohs_cypher)
    print(result == {"tmeopcus", "metopcus", "ameopcus", "atmepcus"})
    print(result)
