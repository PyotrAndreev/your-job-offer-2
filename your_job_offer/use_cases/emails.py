emails = [], passwords = []


def extract_emails_and_passwords(file_path: str):
    emails = []
    passwords = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if ':' in line:
                email, password = line.split(':', 1)
                emails.append(email)
                passwords.append(password)

    return emails, passwords
