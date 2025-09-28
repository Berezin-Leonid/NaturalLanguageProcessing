PASSWORD_REGEXP = r'^(?=.*([\^$%@#&*!?]))(?=.*(?!\1)[\^$%@#&*!?])(?!.*(.)\2)(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[A-Za-z0-9\^$%@#&*!?]{8,}$'
COLOR_REGEXP = r'^(rgb\(\s*(25[0-5]|2[0-4]\d|1\d\d?|[1-9]?\d[%]?|100%)\s*,\s*(25[0-5]|2[0-4]\d|1\d\d?|[1-9]?\d[%]?|100%)\s*,\s*(25[0-5]|2[0-4]\d|1\d\d?|[1-9]?\d[%]?|100%)\s*\)|#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})|hsl\(\s*([0-9]|[1-9]\d|[1-2]\d\d|3[0-5]\d|360)\s*,\s*(100%|[1-9]?\d%)\s*,\s*(100%|[1-9]?\d%)\s*\))$'
EXPRESSION_REGEXP = r'(?P<function>sin|cos|tg|ctg|tan|cot|sinh|cosh|th|cth|tanh|coth|ln|lg|log|exp|sqrt|cbrt|abs|sign)|(?P<constant>pi|e|sqrt2|ln2|ln10)|(?P<number>\d+\.\d+|\d+)|(?P<variable>[a-zA-Z_][a-zA-Z0-9_]*)|(?P<operator>[\^*/\-+])|(?P<left_parenthesis>\()|(?P<right_parenthesis>\))'
# r'^(
# (3[0-1]|[1-2][0-9]|[0]?[1-9])([./-])([0]?[1-9]|(1[0-2]))\2\d{4}|
# \d{4}([./-])(3[0-1]|[1-2][0-9]|[0]?[1-9])\1(3[0-1]|[1-2][0-9]|[0]?[1-9])|
# (0?[1-9]|[1-2][0-9]|3[0-1]) (января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря) \d{4}|
# (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December) (0?[1-9]|[12][0-9]|3[01]), \d{4}|
# \d{4}, (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December) (0?[1-9]|[12][0-9]|3[01])|
# )$'


Year = r"\d{4}"
Month = r"([0]?[1-9]|(1[0-2]))"
Day = r'(3[0-1]|[1-2][0-9]|[0]?[1-9])'
Month_russian = r'(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)'
Month_eng = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)"


DATES_REGEXP = fr'^({Day}([./-]){Month}\3{Year}|{Year}([./-]){Month}\6{Day}|{Day} {Month_russian} {Year}|{Month_eng} {Day}, {Year}|{Year}, {Month_eng} {Day})$'

PARENTHESIS_REGEXP = r''
SENTENCES_REGEXP = r''
PERSONS_REGEXP = r''
SERIES_REGEXP = r''


print(DATES_REGEXP)