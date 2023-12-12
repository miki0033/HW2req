import tree


def pharaohs_revenge(encrypted_text: str, pharaohs_cypher: dict[str, str]) -> set[str]:
    # memo=memoizzazione per salvare i risultati intermedi durante la ricerca delle sequenze
    memo = {}
    result = find_shortest_sequences(encrypted_text, pharaohs_cypher, memo)
    return result


def is_partial_solution(text, transformations):
    return all(pattern in text for pattern in transformations)


def apply_transformation(text, pattern, replacement):
    return text.replace(pattern, replacement, 1)


def find_shortest_sequences(text, transformations, memo):
    if not is_partial_solution(text, transformations):
        return {text}

    if text in memo:
        return memo[text]

    shortest_sequences = set()
    min_length = float("inf")

    for pattern, replacement in transformations.items():
        indices = [
            i
            for i in range(len(text) - len(pattern) + 1)
            if text[i : i + len(pattern)] == pattern
        ]
        for index in indices:
            new_text = apply_transformation(text, pattern, replacement)
            sub_sequences = find_shortest_sequences(new_text, transformations, memo)
            length = min(len(sub_seq) for sub_seq in sub_sequences)

            if length < min_length:
                min_length = length
                shortest_sequences = sub_sequences
            elif length == min_length:
                shortest_sequences.update(sub_sequences)

    memo[text] = shortest_sequences
    return shortest_sequences


# Esempio di utilizzo
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

# Verifica se il risultato è uguale all'output desiderato
print(result == expected_result)
