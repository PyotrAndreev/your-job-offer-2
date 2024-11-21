# здесь лежат функции для того, чтобы парсить из письма в mail его сообщение


def clean_message_from_hh(message: str) -> str:
    lines = message.split("\n")
    begin_first_line = "<http"
    last_line = "Вопросы и ответы\r"
    first_ind = -1
    for i, line in enumerate(lines):
        if (
            first_ind < 0
            and len(line) >= len(begin_first_line)
            and line[: len(begin_first_line)] == begin_first_line
        ):
            first_ind = i + 1
        if line == last_line:
            last_ind = i - 1
    message_lines = [
        line[:-1]
        for line in lines[first_ind:last_ind]
        if line != "\r"
        and not (
            len(line) >= len(begin_first_line)
            and line[: len(begin_first_line)] == begin_first_line
        )
    ]
    return " ".join(message_lines)
