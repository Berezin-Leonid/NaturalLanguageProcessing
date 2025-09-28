PASSWORD_REGEXP = r'^(?=.*([\^$%@#&*!?]))(?=.*(?!\1)[\^$%@#&*!?])(?!.*(.)\2)(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[A-Za-z0-9\^$%@#&*!?]{8,}$'
COLOR_REGEXP = r'^(rgb\(\s*(25[0-5]|2[0-4]\d|1\d\d?|[1-9]?\d[%]?|100%)\s*,\s*(25[0-5]|2[0-4]\d|1\d\d?|[1-9]?\d[%]?|100%)\s*,\s*(25[0-5]|2[0-4]\d|1\d\d?|[1-9]?\d[%]?|100%)\s*\)|#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})|hsl\(\s*([0-9]|[1-9]\d|[1-2]\d\d|3[0-5]\d|360)\s*,\s*(100%|[1-9]?\d%)\s*,\s*(100%|[1-9]?\d%)\s*\))$'
EXPRESSION_REGEXP = r'(?P<function>sin|cos|tg|ctg|tan|cot|sinh|cosh|th|cth|tanh|coth|ln|lg|log|exp|sqrt|cbrt|abs|sign)|(?P<constant>pi|e|sqrt2|ln2|ln10)|(?P<number>\d+\.\d+|\d+)|(?P<variable>[a-zA-Z_][a-zA-Z0-9_]*)|(?P<operator>[\^*/\-+])|(?P<left_parenthesis>\()|(?P<right_parenthesis>\))'
DATES_REGEXP = r''

PARENTHESIS_REGEXP = r''
SENTENCES_REGEXP = r''
PERSONS_REGEXP = r''
SERIES_REGEXP = r''


