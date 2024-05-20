import re


def replace_consecutive_newlines(text) -> str:
    # Use regular expression to replace consecutive newlines with a single newline
    modified_text = re.sub(r'\n\s*\n*', '\n', text)
    return modified_text


def remove_special_characters(text) -> str:
    # Use replace to remove \x0c
    modified_text = re.sub(r'[\x0c\xad]', ' ', text)
    return modified_text


def remove_links(text) -> str:
    # Use regular expression to remove links starting with www.
    # Use regular expression to remove links
    modified_text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    return modified_text


def remove_dates(text) -> str:
    # Use regular expression to remove dates like "31 March 2006"
    modified_text = re.sub(r'\b\d{1,2} [a-zA-Z]+ \d{4}\b', ' ', text)
    return modified_text


def remove_currency(text) -> str:
    modified_text = re.sub(r'[$€£¥₹₽₩₺₴₭₪₨]', " ", text)
    return modified_text


def remove_decimal_numbers(text) -> str:
    # Use regular expression to remove decimal point numbers, sometimes followed by "p" for percent
    modified_text = re.sub(r'\b[(]?(\d{1,3},)*\d{0,3}.\d+[pkKmMbB)]?\b', ' ', text)
    return modified_text


def remove_parenthesis(text) -> str:
    modified_text = re.sub(r'\(\s*\d*[a-zA-Z]?\+?\s*\)', ' ', text)
    return modified_text


def remove_percent(text) -> str:
    # Use regular expression to remove "per cent" text and percent symbols
    modified_text = re.sub(r'\b(?:per cent|%)\b', ' ', text)
    return modified_text


def remove_lonely_symbols(text) -> str:
    modified_text = re.sub(r"\s+(\(?\d{0,2}%[),]?|\'|N/A|\(|p|per cent|\*|·|million|,|\.|-|:)\s+", ' ', text)
    return modified_text


def remove_extra_spaces(text) -> str:
    # Use regular expression to remove extra spaces
    modified_text = re.sub(r'\s+', ' ', text)
    return modified_text.strip()


def remove_extra_points(text) -> str:
    modified_text = re.sub(r'\.{2,}', r"\.", text)
    return modified_text


def remove_double_backslashes(text):
    # Use regular expression to remove double backslashes
    modified_text = re.sub(r'\\', '', text)
    return modified_text


def remove_emails(text):
    # Use regular expression to remove email addresses
    modified_text = re.sub(r'\S+@\S+', ' ', text)
    return modified_text


def remove_mult_underscore(text):
    modified_text = re.sub(r'__+', " ", text)
    return modified_text


def remove_space_betw_newlines(text):
    return re.sub(r'\n\s*\n', '\n\n', text)


def remove_newline(text) -> str:
    return re.sub(r'\n', ' ', text)


def fix_split_words(text) -> str:
    return re.sub(r'(?<=\w)-\n\s{0,1}(?=\w)', "", text)

def fix_cannot(text) -> str:
    return re.sub(r'\bcannot\b', 'can not', text)

def fix_lonely_dots(text) -> str:
    return re.sub(r'\s+\.', '.', text)

def remove_lonely_letterDot(text) -> str:
    return re.sub(r'\b(?:([A-ZŞﬁ])\.)*[A-ZŞﬁ]\.', lambda m: m.group(0).replace('.', ''), text)

def remove_lonely_letterSpaceDot(text) -> str:
    return re.sub(r'\b[A-ZŞﬁ]\b\s(\.)', lambda m: m.group(0).replace('.', ''), text)

def remove_double_letterDot(text) -> str:
    return re.sub(r'\b[A-ZŞﬁ]{2}\.', lambda m: m.group(0).replace('.', ''), text)

def fix_fmancial(text) -> str:
    return re.sub('fmancial', 'financial', text)

def remove_comma_dot(text) -> str:
    return re.sub(r'\.,', '', text)

def remove_roman_num_dot(text) -> str:
    return re.sub(r'\s(i{1,3}|iv|vi{1,3}|ix|x|a|b|c|d|No)\.', " ", text)

def remove_nullstring(text):
    return re.sub(r'(\x00|\x03)', ' ', text)

def remove_spec_uni_char(text):
    return re.sub(f'\\u0231', ' ', text)

def pre_clean(text) -> str:
    text = fix_split_words(text)
    # remove newline
    text = remove_newline(text)
    # remove extra spaces
    text = remove_extra_spaces(text)
    # split cannot into can not
    text = fix_cannot(text)
    # fix fmancial
    text = fix_fmancial(text)
    # fix ,.
    text = remove_comma_dot(text)
    # remove roman numbers with dot
    text = remove_roman_num_dot(text)
    text = remove_nullstring(text)
    text = remove_spec_uni_char(text)
    return text

def clean_text(text) -> str:
    text = remove_special_characters(text)
    text = replace_consecutive_newlines(text)
    text = remove_links(text)
    text = remove_dates(text)
    text = remove_currency(text)
    text = remove_decimal_numbers(text)
    text = remove_parenthesis(text)
    text = remove_lonely_symbols(text)
    text = remove_extra_spaces(text)
    text = remove_extra_points(text)
    text = remove_double_backslashes(text)
    text = remove_emails(text)
    text = remove_mult_underscore(text)
    return text

def clean_less(text) -> str:
    text = remove_special_characters(text)
    text = replace_consecutive_newlines(text)
    text = remove_links(text)
    text = remove_currency(text)
    text = remove_lonely_symbols(text)
    text = fix_lonely_dots(text)
    text = remove_extra_points(text)
    text = remove_extra_spaces(text)
    return text