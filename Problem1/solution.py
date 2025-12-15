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


# Second part

# Скобочная последовательность длины 1
paren_len_1 = r'^(?:\(\)|\[\]|\{\})*$'

def get_n_deepth_regexp(n):
    final = r'(?:\(\)|\[\]|\{\})*'
    for i in range(n - 1):
        if i == n - 2:
            final = fr'^(?:\({final}\)|\[{final}\]|{{{final}}})*$'
        else:
            final = fr'(?:\({final}\)|\[{final}\]|{{{final}}})*'

    return final



PARENTHESIS_REGEXP = get_n_deepth_regexp(n=11)


SENTENCES_REGEXP = r"(?P<sentence>(?:\d+\.\s*)?(?:\S.*?)(?:\:)(?:(?:\d+\.\s*)?(?:\S.*?)(?:\;)(?!\s*[а-яё])(?<![А-ЯЁ]\.)(?=(?:\s*|$)(?:[\'\"\«\(\+\-\=\%\^\$\#\@\~])*(?:\s*|$)(?:[А-ЯЁ0-9]|$)))+(?:(?:\d+\.\s*)?(?:\S.*?)(?:\.\.\.|[.!?]|$)(?!\s*[а-яё])(?<![А-ЯЁ]\.)(?=(?:\s*|$)(?:[\'\"\«\(\+\-\=\%\^\$\#\@\~])*(?:\s*|$)(?:[А-ЯЁ0-9]|$)))|(?:\d+\.\s*)?(?:\S.*?)(?:\.\.\.|[.!?]|$)(?!\s*[а-яё])(?<![А-ЯЁ]\.)(?=(?:\s*|$)(?:[\'\"\«\(\+\-\=\%\^\$\#\@\~])*(?:\s*|$)(?:[А-ЯЁ0-9]|$)))"

PERSONS_REGEXP = r"(?P<person>(?:(?:[А-ЯЁ]\.\s*){1,2}[А-ЯЁ][а-яё]+|(?:[А-ЯЁ][а-яё]{2,}(?:-[А-ЯЁ][а-яё]{2,})?(?:\s+(?![А-ЯЁ]{2,}\b)[А-ЯЁ][а-яё]{2,}){1,2})|(?:[А-ЯЁ][а-яё]{2,}(?:-(?:[А-ЯЁ][а-яё]{2,}))?(?:ов|ев|ёв|ин|ын|ский|цкий|ова|ева|енко|юк|ко|ич|евич|ян|ук|ина|овна|ская|цкая|янна))))\b"

SERIES_REGEXP = r'(?is)(?:<h1[^>]*>\s*<a[^>]+href="/series/\d+/"[^>]*>(?P<name>[^<]+)</a>\s*</h1>)|(?:Эпизоды:\s*</b>\s*</td>\s*<td[^>]*>(?P<episodes_count>\d+)</td>)|(?:Сезон\s+(?P<season>\d+)</h1>\s*(?P<season_year>\d{4})\s*,\s*эпизодов:\s*(?P<season_episodes>\d+))|(?:Эпизод\s+(?P<episode_number>\d+)</span>.*?<b>(?P<episode_name>[^<]+)</b>.*?<span[^>]*>(?P<episode_original_name>[^<]+)</span>.*?<td[^>]*>(?P<episode_date>\d{1,2}\s+[а-яё]+\s+\d{4})</td>)'
