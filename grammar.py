grammar = {
    "<strategy>": [
        ["IF", "<cond>", "THEN", "<strategy>", "ELSE", "<strategy>"],
        ["<action>"]
    ],
    "<cond>": [
        ["<expr>", "<op>", "<expr>"],
        ["<cond>", "AND", "<cond>"],
        ["<cond>", "OR", "<cond>"]
    ],
    "<expr>": [
        "Close", "SMA10", "SMA50", "RSI", "<const>"
    ],
    "<op>": [
        ">", "<", ">=", "<=", "=="
    ],
    "<action>": [
        "BUY", "SELL", "HOLD"
    ],
    "<const>": [
        10, 20, 30, 40, 50, 60, 70, 80, 90, 100
    ]
}
