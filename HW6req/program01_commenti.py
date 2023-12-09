# #!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
È una tranquilla serata di dicembre e mentre fuori piove a dirotto
ricevi una chiamata dalla tuo amico Bart, poco esperto di computer.
Dopo averlo calmato, ti racconta di essersi messo al
pc per cercare un regalo perfetto sull'onda del successo dei siti di
e-commerce alternativi, facendo ricerche sui siti più disparati
utilizzando un traduttore automatico. Ti racconta di essere finito
su un sito con il dominio .atp, pensando che avesse a che fare
con il tennis, sua grande passione. Dopo aver
seguito un paio di prodotti sullo strano sito, si è accorto che
il suo browser rispondeva più lentamente e il puntatore del mouse
cominciava ad andare a scatti. Dopo pochi secondi, gli è apparso un
messaggio di avvertimento che lo informava di essere stato
infettato da un ransomware di ultima generazione, che prende
di mira i file del pc. Colto dal panico, si è ricordato della
tua impresa con gli spartiti dei Tarahumara e ti ha chiamato
affinché lo aiuti a recuperare i suoi file. Il giorno dopo,
ti rechi a casa di Bart e analizzi la situazione: come pensavi,
il ransomware è il famigerato Burl1(ONE), che cifra i file del pc
memorizzando la chiave di cifratura all'interno delle immagini
con estensione .png, trasformandole in puzzle complicatissimi.
Poiché Bart memorizza le sue immagini su un servizio on cloud,
riesci a recuperare le immagini originali in modo da poter
risalire alla chiave di cifratura del ransomware. Riuscirai
a trovare tutte le chiavi? Bart conta su di te!

Il ransomware Burl1 memorizza la chiave di cifratura dividendo
in tasselli quadrati le immagini con estensione .png ed eseguendo
o meno delle rotazioni dei singoli tasselli di 90, 180 oppure 270°, 
ovvero eseguendo una, due o tre rotazioni a destra. La chiave avrà
rispettivamente una 'R' (right) una 'F' (flip) o una 'L' (left) a
seconda della rotazione fatta. L'assenza di rotazione indica il
carattere 'N'. Per ogni immagine è necessario ricostruire la chiave
di cifratura sotto forma di una lista di stringhe: ogni stringa
corrisponde alla sequenza di rotazioni di ogni tassello di una
riga. Per cui un'immagine 100x60 in cui i tasselli hanno dimensione
20 nasconderà una chiave di cifratura di 15 caratteri, organizzati
in tre stringhe da cinque caratteri ognuna. Infatti, ci saranno
5 tasselli per riga (100//20 = 5) e 3 righe (60//20 = 3).
Per scoprire le rotazioni eseguite devi utilizzare l'immagine
che hai recuperato dal cloud per eseguire il confronto con
l'immagine cifrata.

Devi scrivere la funzione
jigsaw(puzzle_image: str, plain_image: str, tile_size:int, encrypted_file: str, plain_file: str) -> list[str]:
che prende in ingresso 
- il nome del file contenente l'immagine con i tasselli ruotati, 
- il nome del file contenente l'immagine con i tasselli non ruotati, 
- un intero che indica la dimensione del lato dei tasselli quadrati, 
- il nome di un file di testo da decifrare con la chiave di cifratura 
- e il nome in cui salvare il file decifrato.

La funzione deve restituire la chiave di cifratura nascosta
nell'immagine in puzzle_image, ovvero la sequenza di
rotazioni da fare per ricostruire l'immagine iniziale e decifrare
il file in input.

Ad esempio, confrontando l'immagine in test01_in.png con test01_exp.png
e considerando i tasselli quadrati da 20 pixel, è possibile
stabilire che le rotazioni applicate sono state
            - 'LFR' per i tasselli della prima riga
            - 'NFF' per i tasselli della seconda riga e
            - 'FNR' per i tasselli della terza riga
            Per cui la chiave da ritornare sarà: ['LFR', 'NFF', 'FNR'].
            
La decifratura del file si ottiene attuando una trasformazione del
cattere in posizione i mediante il carattere della chiave in posizione
i modulo la lunghezza della chiave.

Ad esempio, se la chiave è ['LFR', 'NFF', 'FNR'], la chiave è lunga 9 
e bisogna decifrare il carattere in posizione 14 del file in input,
bisogna considerare il carattere in posizione 14%9 = 5 della chiave,
ovvero 'F'.
Le trasformazioni per la decifratura sono le seguenti:
    - R = text[i] sostituito dal carattere con ord seguente
    - L = text[i] sostituito dal carattere con ord precedente
    - N = resta invariato
    - F = swap text[i] con text[i+1]. Se i+1 non esiste, si considera 
          il carattere text[0].

Ad esempio, se la chiave di cifratura è LFR e il testo cifrato è BNVDCAP,
il testo in chiaro sarà AVOCADO, in quanto la decifratura è la seguente:

step     key      deciphering-buffer
1        LFR      BNVDCAP -> ANVDCAP
         ^        ^
2        LFR      ANVDCAP -> AVNDCAP
          ^        ^
3        LFR      AVNDCAP -> AVODCAP
           ^        ^
4        LFR      AVODCAP -> AVOCCAP
         ^           ^
5        LFR      AVOCCAP -> AVOCACP
          ^           ^
6        LFR      AVOCACP -> AVOCADP
           ^           ^
7        LFR      AVOCADP -> AVOCADO
         ^              ^

"""

# %%
import images


# CODICE
def jigsaw(
    puzzle_image: str,
    plain_image: str,
    tile_size: int,
    encrypted_file: str,
    plain_file: str,
) -> list[str]:
    # Carica le immagini
    puzzle_img = images.load(puzzle_image)
    plain_img = images.load(plain_image)

    # Ottieni le dimensioni delle immagini
    width = len(puzzle_img[0]) // tile_size  # * tile_size
    height = len(puzzle_img) // tile_size  # * tile_size

    # Inizializza la chiave di cifratura
    encryption_key = []
    debug = True
    # Confronta i tasselli e ottieni la chiave
    for y in range(len(puzzle_img) // tile_size):
        key_row = ""
        for x in range(len(puzzle_img[0]) // tile_size):
            # suddivide le immagini in tasselli
            puzzle_tile = [
                row[x * tile_size : (x + 1) * tile_size]
                for row in puzzle_img[y * tile_size : (y + 1) * tile_size]
            ]

            plain_tile = [
                row[x * tile_size : (x + 1) * tile_size]
                for row in plain_img[y * tile_size : (y + 1) * tile_size]
            ]

            key_row = obtainKeyChar(key_row, puzzle_tile, plain_tile)

        # Aggiungi la riga della chiave alla chiave totale
        encryption_key.append(key_row)

    # Decifra il file utilizzando la chiave di cifratura

    with open(encrypted_file, "r", encoding="utf-8") as encrypted_file_content:
        encrypted_text = encrypted_file_content.read()

        decrypted_text = decipherBuffer(encrypted_text, encryption_key)

        # print(decrypted_text)
        # Salva il file decifrato
        with open(plain_file, "w", encoding="utf-8") as plain_file_content:
            plain_file_content.write(decrypted_text)

    return encryption_key


def decipherBuffer(encrypted_text, encryption_key):
    decryption_key = "".join(
        encryption_key
    )  # Unisci la chiave di cifratura in una singola stringa
    key_length = len(decryption_key)
    decrypted_text = ""
    encrypted_list = [*encrypted_text]

    for i, char in enumerate(encrypted_list):
        key_char = decryption_key[i % key_length]

        if key_char == "R":
            decrypted_text += chr(ord(char) + 1)
            encrypted_list[i] = chr(ord(char) + 1)
        elif key_char == "L":
            decrypted_text += chr(ord(char) - 1)
            encrypted_list[i] = chr(ord(char) - 1)
        elif key_char == "N":
            decrypted_text += char
        elif key_char == "F":
            next_index = (i + 1) % len(encrypted_text)
            next_char = encrypted_list[next_index]  # swap temp=i+1

            encrypted_list[i] = next_char  # swap i=temp

            decrypted_text += next_char
            encrypted_list[next_index] = char  # swap i+1=i

    # caso particolare fine con f devo rimodificare l'inizio
    if key_char == "F":
        decrypted_text = list(decrypted_text)
        decrypted_text[0] = encrypted_list[0]

    # print(key_char)
    decrypted_text = "".join(decrypted_text)
    return decrypted_text


def obtainKeyChar(key_row, puzzle_tile, plain_tile):
    # Confronta i tasselli e aggiungi la rotazione alla chiave
    if matrixEqual(puzzle_tile, plain_tile):
        key_row += "N"
    else:
        rotated_tile = rotateMatrix(puzzle_tile, 90)  # Esegui rotazione a destra
        if matrixEqual(rotated_tile, plain_tile):
            key_row += "R"
        else:
            flipped_tile = rotateMatrix(puzzle_tile, 180)  # Esegui flip
            if matrixEqual(flipped_tile, plain_tile):
                key_row += "F"
            else:
                key_row += "L"

    return key_row


def rotateMatrix(matrix, degrees):
    rows = len(matrix)
    cols = len(matrix[0])
    # Calcola il numero di iterazioni in base agli angoli
    iterations = degrees // 90
    # Esegui le iterazioni necessarie
    for _ in range(iterations):
        # Trasponi la matrice
        new_matrix = [[0] * rows for _ in range(cols)]
        for i in range(rows):
            for j in range(cols):
                new_matrix[j][i] = matrix[i][j]
        matrix = new_matrix
        # Inverti le colonne
        for i in range(cols):
            matrix[i].reverse()
        # Aggiorna le dimensioni
        rows, cols = cols, rows

    return matrix


def matrixEqual(matrix1, matrix2):
    if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        # Verifica se le dimensioni delle matrici sono diverse
        return False
    for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            if matrix1[i][j] != matrix2[i][j]:
                # Verifica se gli elementi corrispondenti sono diversi
                return False
    # Se tutte le condizioni sono soddisfatte, le matrici sono uguali
    return True


if __name__ == "__main__":
    out = jigsaw(
        "tests/test03_in.png",
        "tests/test03_exp.png",
        44,
        "tests/test03_enc.txt",
        "output/test03_out.txt",
    )
    print(out)

    out = jigsaw(
        "tests/test06_in.png",
        "tests/test06_exp.png",
        40,
        "tests/test06_enc.txt",
        "output/test06_out.txt",
    )
    print(out)

    out = jigsaw(
        "tests/test08_in.png",
        "tests/test08_exp.png",
        220,
        "tests/test08_enc.txt",
        "output/test08_out.txt",
    )
    print(out)
    """
    decript = decipherBuffer("BNVDCAP", "LFR")
    print(decript)"""
