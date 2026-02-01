def build_strategy(elements):
    if elements[0] == "IF":
        return {
            "type": "if",
            "condition": elements[1],
            "then": elements[3],
            "else": elements[5]
        }

    elif len(elements) == 1:
        return elements[0]


def build_action(elements):
    return {"type": "action", "value": elements[0]}


def build_cond(elements):
    if len(elements) == 3 and elements[1] in ["AND", "OR"]:
        return {"left": elements[0], "logic_op": elements[1], "right": elements[2]}

    return {"left": elements[0], "op": elements[1], "right": elements[2]}


def map_genotype_to_fenotype(genotype, grammar, max_depth):
    """
    Zamienia liste intow na strategie
    """
    idx = 0

    builders = {
        "<start>": build_strategy,
        "<strategy>": build_strategy,
        "<action>": build_action,
        "<cond>": build_cond
    }

    def expand(symbol, depth):
        nonlocal idx

        if depth > max_depth:
            return None

        # TERMINAL
        if symbol not in grammar:
            return symbol

        gene = genotype[idx % len(genotype)]
        idx += 1

        options = grammar[symbol]
        choice = options[gene % len(options)]

        if isinstance(choice, list):
            results = []
            for item in choice:
                res = expand(item, depth + 1)
                if res is None:
                    return None
                results.append(res)
            if symbol in builders:
                return builders[symbol](results)
            else:
                return results[0] if len(results) == 1 else results

        else:
            res = expand(choice, depth + 1)
            if res is None:
                return None

            if symbol in builders:
                return builders[symbol]([res])
            return res

    return expand('<start>', 0)
