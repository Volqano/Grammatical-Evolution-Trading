import numpy as np


def evaluate_condition(cond, row):
    if "logic_op" in cond:
        left_res = evaluate_condition(cond["left"], row)
        right_res = evaluate_condition(cond["right"], row)
        if cond["logic_op"] == "AND":
            return left_res and right_res
        elif cond["logic_op"] == "OR":
            return left_res or right_res

    left = row[cond["left"]] if cond["left"] in row else cond["left"]
    right = row[cond["right"]] if cond["right"] in row else cond["right"]

    if cond["op"] == ">":
        return left > right
    elif cond["op"] == "<":
        return left < right
    elif cond["op"] == ">=":
        return left >= right
    elif cond["op"] == "<=":
        return left <= right
    elif cond["op"] == "==":
        return left == right


def vectorized_evaluate_condition(cond, data_dict):
    if "logic_op" in cond:
        left_res = vectorized_evaluate_condition(cond["left"], data_dict)
        right_res = vectorized_evaluate_condition(cond["right"], data_dict)
        if cond["logic_op"] == "AND":
            return left_res & right_res
        elif cond["logic_op"] == "OR":
            return left_res | right_res

    if isinstance(cond["left"], str) and cond["left"] in data_dict:
        left = data_dict[cond["left"]]
    else:
        left = cond["left"]

    if isinstance(cond["right"], str) and cond["right"] in data_dict:
        right = data_dict[cond["right"]]
    else:
        right = cond["right"]

    op = cond["op"]
    if op == ">":
        return left > right
    elif op == "<":
        return left < right
    elif op == ">=":
        return left >= right
    elif op == "<=":
        return left <= right
    elif op == "==":
        return left == right
    return False


def evaluate_strategy(strategy, row):
    if strategy["type"] == "action":
        return strategy["value"]

    condition = strategy["condition"]
    if evaluate_condition(condition, row):
        return evaluate_strategy(strategy["then"], row)
    else:
        return evaluate_strategy(strategy["else"], row)


def vectorized_evaluate_strategy(strategy, data_dict, n_rows):
    if strategy["type"] == "action":
        return np.full(n_rows, strategy["value"], dtype=object)

    condition_mask = vectorized_evaluate_condition(strategy["condition"], data_dict)
    then_values = vectorized_evaluate_strategy(strategy["then"], data_dict, n_rows)
    else_values = vectorized_evaluate_strategy(strategy["else"], data_dict, n_rows)

    return np.where(condition_mask, then_values, else_values)


def backtest(rule, data, initial_cash):
    """
    rule - decision rules used to calculating return
    ticker - ticker on which we will be testing rule

    return: total return by using given decision rule
    """
    cash = initial_cash
    stock = 0
    for i in range(len(data)):
        price = data.iloc[i]["Close"]
        action = evaluate_strategy(rule, data.iloc[i])
        if action == "BUY" and stock == 0:
            stock = cash / price
            cash = 0
        elif action == "SELL" and stock > 0:
            cash = stock * price
            stock = 0

    total_return = cash + stock * data.iloc[-1]["Close"] - initial_cash
    return total_return


def fast_backtest(rule, data_dict, initial_cash):
    prices = data_dict["Close"]
    if hasattr(prices, 'values'):
        prices = prices.values

    n_rows = len(prices)

    actions = vectorized_evaluate_strategy(rule, data_dict, n_rows)

    cash = initial_cash
    stock = 0.0

    for i in range(n_rows):
        action = actions[i]
        price = prices[i]

        if action == "BUY" and stock == 0:
            stock = cash / price
            cash = 0.0
        elif action == "SELL" and stock > 0:
            cash = stock * price
            stock = 0.0

    total_return = cash + (stock * prices[-1]) - initial_cash
    return total_return
