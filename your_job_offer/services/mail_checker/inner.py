from dataclasses import replace
import imaplib
import email
from email.header import decode_header

from your_job_offer.entities.user import EmailMessage
from .handlers import *


def get_email_message(msg) -> EmailMessage | None:
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else "utf-8")

    # Получаем отправителя
    from_ = msg.get("From")

    # Получаем дату
    date_ = msg.get("Date")
    date_time = email.utils.parsedate_to_datetime(date_)

    result = EmailMessage(from_, date_time, subject)
    # Печатаем информацию

    # Получаем тело письма (если оно составное)
    if msg.is_multipart():
        for part in msg.walk():
            # print(part)
            # Ищем текстовую часть
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
    else:
        # Если письмо не составное
        # print(1)
        body = msg.get_payload(decode=True).decode()
    if "body" not in locals():
        return None
    result.body = body
    return result


def get_messages(username: str, password_app: str) -> list[EmailMessage]:
    """
    получает все сообщения

    :param username: почта с яндексовым доменом и подключенным IMAP
    :param passwsord_app: пароль, созданные для приложения
    """
    YA_HOST = "imap.yandex.ru"
    YA_PORT = 993

    mail = imaplib.IMAP4_SSL(host=YA_HOST, port=YA_PORT)
    mail.login(username, password_app)

    # Выбор папки "Входящие"
    mail.select("inbox")

    # Поиск писем
    status, messages = mail.search(None, "ALL")

    # Получение списка ID сообщений
    email_ids = messages[0].split()

    result: list[EmailMessage] = []
    # Перебираем каждое письмо
    for email_id in email_ids:
        # Получаем письмо
        res, msg = mail.fetch(email_id, "(RFC822)")

        # Получаем текст письма
        msg = email.message_from_bytes(msg[0][1])
        email_message = get_email_message(msg)
        if email_message is not None:
            result.append(email_message)

    # Закрываем соединение
    mail.close()
    mail.logout()

    return result
