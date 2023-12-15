# #!/usr/bin/env python3
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

"""
    TODO:
    1)Ricavare tutte le possibili combinazioni da una parola togliendo una lettera
      e vedere se una di queste combinazioni corrisponde
    2)Se l'anagramma non è traducibile si ha una sequenza finale
    3)Ricavare l'insieme delle sequenze finali e prendere le più corte
"""
import tree


def pharaohs_revenge(encrypted_text: str, pharaohs_cypher: dict[str, str]) -> set[str]:
    root = tree.Tree(None)  # inizializzo un albero
    recursive_decypher(root, encrypted_text, pharaohs_cypher)
    # cercare nelle foglie dell'albero la sequenza con lunghezza minima
    leafsvalue = set()
    check_leaf_value(root, leafsvalue)
    minimum = float("inf")
    result = set()
    # print(root.__repr__())
    # print(leafsvalue)
    for value in leafsvalue:
        if value != None:
            if minimum > len(value):
                result.clear()
                minimum = min(minimum, len(value))
            if minimum == len(value):
                result.add(value)

    return result


def recursive_decypher(node, text, cypher):
    for key, value in cypher.items():  # gira tutte le possibili decodifiche
        letters_to_replace = [*key]

        for i in range(len(text)):
            # cerca l'anagramma in una sotto sequenza di caratteri
            sublen = len(letters_to_replace) + 1
            preText = text[:i]
            subtext = text[i : i + sublen]
            postText = text[i + sublen :]
            flagpos = [-1]
            flag = True
            for letter in letters_to_replace:
                # controllo se trovo tutte le lettere da rimpiazzare
                subpos = subtext.find(letter)
                if subpos == -1:
                    flag = False
                elif flagpos[0] == -1:
                    flagpos[0] = subpos + i
                else:
                    flagpos.append(subpos + i)
            if flag:  # se le ha trovate tutte effettua la sostituzione
                subtext = value
                modtext = preText + subtext + postText
                tree_node = tree.Tree(modtext)
                node.AddChild(tree_node)
                recursive_decypher(tree_node, modtext, cypher)


def check_leaf_value(node, leafsvalue):
    # Controlla se il nodo è una foglia
    if node.isLeaf():
        # Se è una foglia, si salva il value
        leafsvalue.add(node.value)
    # Chiamata ricorsiva per ogni figlio del nodo
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

    encrypted_text = "aaabaaac"
    pharaohs_cypher = {"aa": "bc", "bb": "c", "cc": "d"}
    expected = {"d"}
    res = pharaohs_revenge(encrypted_text, pharaohs_cypher)
    print(res == expected)
    print(res)

    encrypted_text = "\ud80c\udf50\ud80c\ude7e\ud80c\uddd3\ud80c\udfa5\ud80c\udd68\ud80c\udef7\ud80c\uddd8\ud80c\udc6d&\ud80c\udf7d\ud80c\ude89D\ud80c\udef6k\ud80c\udfac\ud80c\udde4\ud80c\udd18q\ud80c\udeedNb\ud80c\udf2b\ud80c\ude50\ud80c\udfe00\ud80c\udf00\ud80d\udc12\ud80c\udc1a\ud80c\udfc4q\ud80c\uddc7\ud80c\udf60\ud80d\udc17\ud80c\udd4ay\ud80c\udcf6m\ud80c\ude20e\ud80c\udc69\ud80c\udde2\ud80c\uddd1"
    pharaohs_cypher = {
        "\ud80c\udfacD\ud80c\uddd8\ud80c\udd18\ud80c\ude89\ud80c\udc6d\ud80c\udf7d\ud80c\udde4q\ud80c\udd68\ud80c\udef6\ud80c\udef7k\ud80c\udfa5": "S\ud80c\ude13\ud80c\udd72A\ud80c\udd81*g\ud80c\udfacV\ud80c\udf65\ud80c\ude20",
        "\ud80c\udd72\ud80c\ude7e\ud80c\uddd3\ud80c\udfac\ud80c\udf50\ud80c\udd35A\ud80c\ude13\ud80c\udd81gS": "The amuc",
        "\ud80c\udeed\ud80c\udf00\ud80c\udfc4\ud80c\udc1abV\ud80c\udfe0\ud80c\udf2b\ud80d\udc12\ud80c\udf65\ud80c\ude20\ud80c\ude50N": "\ud80c\udd35ny cent e",
        "on\ud80c\udfc4\ud80d\udc12\ud80c\ude50iN\ud80c\udf65\ud80c\udeed ": "\ud80c\udfc4\ud80c\udf2b\ud80c\udfe0\ud80d\udc12N k",
        "q\ud80c\udc6dSDkg\ud80c\ude20\ud80c\uddd8\ud80c\udf7d\ud80c\udde4\ud80c\udef6": "k\ud80c\udde4\ud80c\udef6\ud80c\udfa5\ud80c\udfac*\ud80c\uddd8\ud80c\udf7d",
        "\ud80c\udf60a \ud80c\uddc7\ud80c\udc69\ud80c\ude20\ud80d\udc17me": "\ud80c\uddc7e\ud80c\udd4ayn\ud80c\udde2",
        "\ud80c\udde4\ud80c\udf7d\ud80c\uddd8\ud80c\ude20\ud80c\udf65\ud80c\udd68*D\ud80c\ude89\ud80c\udfa5\ud80c\udef6": "q\ud80c\udd81\ud80c\udd72\ud80c\udde4\ud80c\udd68\ud80c\ude13A\ud80c\udfac",
        "\ud80c\ude89\ud80c\udfacq\ud80c\uddd8k\ud80c\udfa5\ud80c\udef6\ud80c\udd68D\ud80c\udde4\ud80c\udc6d\ud80c\udf7d\ud80c\udef7\ud80c\udd18": "S\ud80c\ude13\ud80c\udd72A\ud80c\udd81*g\ud80c\udfacV\ud80c\udf65\ud80c\ude20",
        "\ud80c\udde2\ud80c\udf60\ud80d\udc17\ud80c\udcf6\ud80c\uddd1m\ud80c\udd4a\ud80c\uddc7\ud80c\ude20ye\ud80c\udc69": "rns tank.",
        "\ud80d\udc12\ud80c\udf00\ud80c\udf65\ud80c\udfe0\ud80c\udfc4V\ud80c\ude50\ud80c\udc1aN\ud80c\ude20b\ud80c\udeed\ud80c\udf2b": "\ud80c\udd35ky yin op",
        "\ud80c\udfac\ud80c\udd72\ud80c\ude7eg\ud80c\ude13A\ud80c\udf50S\ud80c\uddd3\ud80c\udd35\ud80c\udd81": "The spoo",
        "me\ud80d\udc17\ud80c\udcf6d\ud80c\udc69s\ud80c\udd4ay": "\ud80c\udde2emny\ud80c\udf60",
        "\ud80c\uddd1\ud80c\ude20\ud80c\udde2\ud80c\udcf6\ud80c\uddc7e\ud80d\udc17\ud80c\udc69y\ud80c\udd4a\ud80c\udf60m": "ens game.",
        "\ud80c\udfc4cN\ud80c\udf00Vb\ud80c\ude20\ud80c\ude50\ud80c\udc1ae": "V \ud80c\ude50\ud80c\udfc4\ud80c\udfe0ne",
        "a\ud80c\ude20.t\ud80d\udc17m\ud80c\udf60sk": "k \ud80d\udc17\ud80c\udf60e\ud80c\udcf6",
        "g\ud80c\udd72 \ud80c\uddd3S\ud80c\udfacs\ud80c\ude7e": "\ud80c\ude7eopg\ud80c\udf50",
        "\ud80c\ude7eA\ud80c\ude13\ud80c\udd72\ud80c\udf50\ud80c\udfacS\ud80c\udd81\ud80c\udd35\ud80c\uddd3g": "The brai",
        "\ud80c\udf50em\ud80c\udd81h\ud80c\udd72uA": " e\ud80c\udd81\ud80c\uddd3a",
        "\ud80c\udfe0\ud80c\udfc4V\ud80d\udc12b\ud80c\udf65\ud80c\udf2b\ud80c\ude50\ud80c\udeed\ud80c\ude20N\ud80c\udf00\ud80c\udc1a": "\ud80c\udd35k slaw tu",
        "\ud80c\udde4\ud80c\udfac\ud80c\udfac\ud80c\uddd8\ud80c\udd72q\ud80c\ude13\ud80c\udd81\ud80c\udd68\ud80c\ude20\ud80c\udfa5": "\ud80c\udfac\ud80c\ude20\ud80c\udd18\ud80c\udf65\ud80c\udef7\ud80c\udfa5\ud80c\udd68\ud80c\uddd8",
        "eS\ud80c\uddd3gr\ud80c\udd35 A": "g\ud80c\udd72 Ab",
        "\ud80c\uddc7\ud80c\udc69em\ud80c\udd4ay\ud80d\udc17\ud80c\udcf6\ud80c\uddd1\ud80c\ude20\ud80c\udf60\ud80c\udde2": "nds mine.",
        "\ud80c\udef6\ud80c\udfa5q\ud80c\uddd8\ud80c\udf7d\ud80c\udef7\ud80c\udd18kD\ud80c\udfac\ud80c\udde4\ud80c\udd68\ud80c\ude89\ud80c\udc6d": "S\ud80c\ude13\ud80c\udd72A\ud80c\udd81*g\ud80c\udfacV\ud80c\udf65\ud80c\ude20",
        " \ud80c\udc1a\ud80c\udeeda\ud80c\udfc4\ud80c\ude50\ud80c\udd35s\ud80c\udf00\ud80c\udf2b": "\ud80c\udf65bk \ud80c\ude50\ud80c\udfc4\ud80c\udf2b",
    }
    expected = {
        "The braiky yin opnds mine.",
        "The amucky yin opnds mine.",
        "The braiky yin opens game.",
        "The spooky yin oprns tank.",
        "The amucny cent erns tank.",
        "The amuck slaw tuens game.",
        "The spoony cent erns tank.",
        "The amucny cent ends mine.",
        "The braik slaw tunds mine.",
        "The amucky yin opens game.",
        "The amuck slaw tunds mine.",
        "The amucky yin oprns tank.",
        "The braik slaw tuens game.",
        "The amucny cent eens game.",
        "The spook slaw tuens game.",
        "The spoony cent ends mine.",
        "The brainy cent eens game.",
        "The spooky yin opens game.",
        "The braik slaw turns tank.",
        "The spook slaw turns tank.",
        "The brainy cent ends mine.",
        "The amuck slaw turns tank.",
        "The spook slaw tunds mine.",
        "The brainy cent erns tank.",
        "The spooky yin opnds mine.",
        "The braiky yin oprns tank.",
        "The spoony cent eens game.",
    }

    res = pharaohs_revenge(encrypted_text, pharaohs_cypher)
    print(res == expected)
    print(res)
