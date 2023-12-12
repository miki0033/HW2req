import tree


def pharaohs_revenge(encrypted_text: str, pharaohs_cypher: dict[str, str]) -> set[str]:
    root = tree.Tree(None)
    combination(encrypted_text, "", pharaohs_cypher, root)


def combination(text, current, pharaohs_cypher, node):
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
