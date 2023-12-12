"""
    Cosa fare:
    1)Ricavare tutte le possibili combinazioni da una parola togliendo una lettera
      e vedere se una di queste combinazioni corrisponde
    2)Se l'anagramma non è traducibile si ha una sequenza finale
    3)Ricavare l'insieme delle sequenze finali e prendere le più corte
"""
import tree


def pharaohs_revenge(encrypted_text: str, pharaohs_cypher: dict[str, str]) -> set[str]:
    root = tree.Tree(None)
    memo = set()
    combination(encrypted_text, "", pharaohs_cypher, memo, root)
    return memo


def combination(text, current, pharaohs_cypher, memo, node):
    if not text:
        memo.add(current)
        return

    for i in range(len(text)):
        prefix = text[i]
        suffix = text[:i] + text[i + 1 :]
        partial_anagram = pharaohs_cypher.get(prefix, prefix)

        found_child = None
        for child in node.children:
            if child.value == partial_anagram:
                found_child = child
                break

        if not found_child:
            found_child = tree.Tree(partial_anagram)
            node.AddChild(found_child)

        combination(
            suffix, current + partial_anagram, pharaohs_cypher, memo, found_child
        )


# Esempio di utilizzo
encrypted_text = "astronaut-flying-cyrcus"
pharaohs_cypher = {
    "tuar": "me",
    "cniy": "op",
    "sorta": "tur",
    "fult": "at",
    "rycg": "nc",
}

result = pharaohs_revenge(encrypted_text, pharaohs_cypher)
print(result)


# TEST
if __name__ == "__main__":
    encrypted_text = "astronaut-flying-cyrcus"
    pharaohs_cypher = {
        "tuar": "me",
        "cniy": "op",
        "sorta": "tur",
        "fult": "at",
        "rycg": "nc",
    }
    expected_result = {"tmeopcus", "metopcus", "ameopcus", "atmepcus"}

    result = pharaohs_revenge(encrypted_text, pharaohs_cypher)
