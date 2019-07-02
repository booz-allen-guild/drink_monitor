with open('../credentials.txt') as f:
    text = f.read()

    text = text.split()

    server = text[0]
    port = text[1]
    db = text[2]
    user = text[3]
    password = text[4]

print(server, port, db, user, password)