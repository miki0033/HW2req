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


def pharaohs_revenge(encrypted_text: str, pharaohs_cypher: dict[str, str]) -> set[str]:
    return find_shortest_sequences(encrypted_text, pharaohs_cypher)


def apply_transformations(text, transformations):
    """
    La funzione apply_transformations è utilizzata per applicare le trasformazioni a una data sequenza.
    L'insieme risultante delle sequenze finali più brevi viene restituito alla fine.
    """
    transformed_texts = set()
    for key, value in transformations.items():
        # prende chiavi e valore del cifrario
        # print(key)
        # print(value)
        indices = [i for i in range(len(text)) if text.startswith(key, i)]
        for index in indices:
            new_text = text[:index] + value + text[index + len(key) :]
            transformed_texts.add(new_text)
    return transformed_texts


def find_shortest_sequences(text, transformations):
    """
    funzione ricorsiva che trova le sequenze finali più brevi
    applicando ripetutamente le trasformazioni del cifrario
    """
    possible_sequences = apply_transformations(text, transformations)
    if not possible_sequences:
        return {text}
    shortest_sequences = set()
    min_length = float("inf")
    for sequence in possible_sequences:
        sub_sequences = find_shortest_sequences(sequence, transformations)
        length = min(len(sub_seq) for sub_seq in sub_sequences)
        if length < min_length:
            min_length = length
            shortest_sequences = sub_sequences
        elif length == min_length:
            shortest_sequences.update(sub_sequences)
    return shortest_sequences


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
