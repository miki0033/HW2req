import tree


def pharaohs_revenge(encrypted_text: str, pharaohs_cypher: dict[str, str]) -> set[str]:
    result = set()
    root_tree = tree.Tree(encrypted_text)
    anagrams = generate_anagrams(encrypted_text)
    for anag in anagrams:
        res = pharaohs_revenge_recursive(anag, pharaohs_cypher, root_tree)
        for r in res:
            result.add(r)
    return result


def pharaohs_revenge_recursive(encrypted_text, pharaohs_cypher, current_tree):
    possible_results = set()

    for search_seq, replace_seq in pharaohs_cypher.items():
        index = encrypted_text.find(search_seq)
        while index != -1:
            new_text = (
                encrypted_text[:index]
                + replace_seq
                + encrypted_text[index + len(search_seq) :]
            )
            child_tree = tree.Tree(new_text)
            current_tree.AddChild(child_tree)
            possible_results.update(
                pharaohs_revenge_recursive(new_text, pharaohs_cypher, child_tree)
            )
            index = encrypted_text.find(search_seq, index + 1)

    if not possible_results:  # No more transformations possible, add the current result
        possible_results.add(current_tree.value)

    return possible_results


def generate_anagrams(word):
    if len(word) <= 1:
        return {word}

    anagrams = set()
    for i in range(len(word)):
        prefix = word[i]
        suffix = word[:i] + word[i + 1 :]
        partial_anagrams = generate_anagrams(suffix)

        for partial_anagram in partial_anagrams:
            anagrams.add(prefix + partial_anagram)

    return anagrams


# Esempio di utilizzo:
encrypted_text = "astronaut-flying-cyrcus"
pharaohs_cypher = {
    "tuar": "me",
    "cniy": "op",
    "sorta": "tur",
    "fult": "at",
    "rycg": "nc",
}

result_tree = pharaohs_revenge(encrypted_text, pharaohs_cypher)
print(result_tree.__repr__())
