def break_in_lines(text: str, line_len: int) -> str:
    lines = [text[i:i + line_len] for i in range(0, len(text), line_len)]
    return '\n'.join(lines)
