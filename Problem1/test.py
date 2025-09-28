import re
from solution import *

pattern = re.compile(PASSWORD_REGEXP)
regex_1_1 = re.compile(PASSWORD_REGEXP)
regex_1_2 = re.compile(COLOR_REGEXP)
token_pattern = re.compile(EXPRESSION_REGEXP, re.VERBOSE)

test_yes_1_1 = [
    "YesLength&#Over8",
    "YeEq#@e8",
    "yesBigelement0@#",
    "YesLItTLELEMENT0@#",
    "YesNumber1234@#",
    "YesAbcdefg1^$",
    "YesSingleB1#@",
    "rtG3FG!Tr^e",
    "aA1!*!1Aa",
    "oF^a1D@y5e6",
    "enroi#$rkdeR#$092uwedchf34tguv394h",
]

test_no_1_1 = [
    "NOe@#s8",
    "nobigelemen0@#",
    "NOLITTLEELEMENT0@#",
    "NoNumber@#",
    "NOAcdefgh1^",
    "NOABcdefg1^^",
    "NOdoubleBB1#@",
    "пароль",
    "password",
    "qwerty",
    "lOngPa$$W0Rd",
]

test_yes_1_2 = [
    "#21f48D",
    "rgb(123, 40% ,32)",
    "hsl(200,100%,50%)",
    "rgb(100,100,100)",
    "rgb(100,100%,100)",
    "rgb(100, 100%,100)",
    "rgb(123, 40% ,32)",
    "#888",
    "rgb(255, 255,255)",
    "rgb(10%, 20%, 0%)",
    "hsl(200,100%,50%)",
    "hsl(0, 0%, 0%)",
]

test_no_1_2 = [
    "hsl(361, 55%, 41%)",
    "rgb(233, 256, 234)",
    "#2345",
    "ffffff",
    "rgb(257, 50, 10)",
    "hsl(20, 10, 0.5)",
    "hsl(34%, 20%, 50%)",
]

expressions = [
    "sin(x) + cos(y) * 2.5",
    "pi + usO5NlMvU",
    "( 63393394.98 /8505 )",
    "(         63393394.98 /8505      )",
]

expected = [
    [
        {"type": "function", "span": [0, 3]},
        {"type": "left_parenthesis", "span": [3, 4]},
        {"type": "variable", "span": [4, 5]},
        {"type": "right_parenthesis", "span": [5, 6]},
        {"type": "operator", "span": [7, 8]},
        {"type": "function", "span": [9, 12]},
        {"type": "left_parenthesis", "span": [12, 13]},
        {"type": "variable", "span": [13, 14]},
        {"type": "right_parenthesis", "span": [14, 15]},
        {"type": "operator", "span": [16, 17]},
        {"type": "number", "span": [18, 21]}
    ],
    [
        {"type": "constant", "span": [0, 2]},
        {"type": "operator", "span": [3, 4]},
        {"type": "variable", "span": [5, 14]}
    ],
    [
        {"type": "left_parenthesis", "span": [0, 1]},
        {"type": "number", "span": [2, 13]},
        {"type": "operator", "span": [14, 15]},
        {"type": "number", "span": [15, 19]},
        {"type": "right_parenthesis", "span": [20, 21]}
    ],
    [
        {"type": "left_parenthesis", "span": [0, 1]},
        {"type": "number", "span": [10, 21]},
        {"type": "operator", "span": [22, 23]},
        {"type": "number", "span": [23, 27]},
        {"type": "right_parenthesis", "span": [33, 34]}
    ]
]


def test_1_1():
    good = True

    for t in test_yes_1_1:
        if not regex_1_1.fullmatch(t):
            print(f"{t} -> FAIL but must be OK")
            good = False

    for t in test_no_1_1:
        if regex_1_1.fullmatch(t):
            print(f"{t} -> OK but must be FAIL")
            good = False

    if good:
        print("Task 1.1 - OK")

def test_1_2():
    good = True

    for t in test_yes_1_2:
        if not regex_1_2.fullmatch(t):
            print(f"{t} -> FAIL but must be OK")
            good = False

    for t in test_no_1_2:
        if regex_1_2.fullmatch(t):
            print(f"{t} -> OK but must be FAIL")
            good = False

    if good:
        print("Task 1.2 - OK")


def test_1_3():
    good = True
    def tokenize(expression):
        tokens = []
        for match in token_pattern.finditer(expression):
            token_type = match.lastgroup
            span = match.span()
            tokens.append({"type": token_type, "span": list(span)})
        return tokens
    
    for expr, expect in zip(expressions, expected):
        result = tokenize(expr)
        if result != expect:
            print(f"Fail for {expr}:\nExpect{expect}\nResult:\n{result}")
            good = False
    if good:
        print("Task 1.3 - OK")

if __name__ == "__main__":
    test_1_1()
    test_1_2()
    test_1_3()


