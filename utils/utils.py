def codeblock(*lines, lang: str = "", end: str = "\n"):
    """get data formatted as a codeblock, with optional language"""
    b = "```"  # three backticks
    lines = end.join(lines)
    return f"{b}{lang}\n{lines}\n{b}"
