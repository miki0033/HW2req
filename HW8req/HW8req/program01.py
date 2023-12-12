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
    Cosa fare:
    1)Ricavare tutte le possibili combinazioni da una parola togliendo una lettera
      e vedere se una di queste combinazioni corrisponde
    2)Se l'anagramma non è traducibile si ha una sequenza finale
    3)Ricavare l'insieme delle sequenze finali e prendere le più corte
"""
import tree


def pharaohs_revenge(encrypted_text: str, pharaohs_cypher: dict[str, str]) -> set[str]:
    root = tree.Tree(None)  # inizializzo un albero
    recursive_decypher(root, encrypted_text, pharaohs_cypher)
    print(root.__repr__)
    # cercare nelle foglie dell'albero la sequenza con lunghezza minima
    leafsvalue = set()
    check_leaf_value(root, leafsvalue)
    print("FOGLIE:")
    print(leafsvalue)
    minimum = float("inf")
    result = set()
    for value in leafsvalue:
        if value != None:
            minimum = min(minimum, len(value))
            result.add(value)

    return result


def recursive_decypher(node, text, cypher):
    for key, value in cypher.items():
        letters_to_replace = [*key]

        for i in range(len(text)):
            # cerca l'anagramma in una sotto sequenza di caratteri
            sublen = len(letters_to_replace) + 1
            preText = text[:i]
            subtext = text[i : i + sublen]
            postText = text[i + sublen :]
            flagpos = [-1]
            for letter in letters_to_replace:
                # controllo se trovo tutte le lettere da rimpiazzare
                subpos = subtext.find(letter)
                if flagpos[0] == -1 and subpos != -1:
                    flagpos[0] = subpos + i
                else:
                    flagpos.append(subpos + i)
            flag = True
            for pos in flagpos:
                if pos == -1:
                    flag = False
            if flag:  # se le ha trovate tutte effettua la sostituzione
                subtext = value
                text = preText + subtext
                text = text + postText
                # print(text)
                tree_node = tree.Tree(text)
                node.AddChild(tree_node)
                recursive_decypher(tree_node, text, cypher)


def check_leaf_value(node, leafsvalue):
    # Controlla se il nodo è una foglia
    if node.isLeaf:
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
