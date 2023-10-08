
def to_camel(string: str) -> str:
    """
        Converts the string to camel case and replaces _ with no space
        e.g., is_null -> IsNull
    @param string: Input string
    @return: Output camel case string
    """
    if "_" not in string:
        return string
    words = string.split("_")
    words = [words[0]] + [word.capitalize() for word in words[1:]]
    return "".join(words)
