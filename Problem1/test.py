import re
from solution import PASSWORD_REGEXP

pattern = re.compile(PASSWORD_REGEXP)

test_yes = [
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

test_no = [
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

def test_1_1():
    good = True

    for t in test_yes:
        if not pattern.fullmatch(t):
            print(f"{t} -> FAIL but must be OK")
            good = False

    for t in test_no:
        if pattern.fullmatch(t):
            print(f"{t} -> OK but must be FAIL")
            good = False

    if good:
        print("Task 1.1 - OK")


if __name__ == "__main__":
    test_1_1()
