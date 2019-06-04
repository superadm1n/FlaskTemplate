from app import bcrypt


def hash_password(pw):
    return bcrypt.generate_password_hash(pw).decode('utf-8')


def check_password(pw, hashed_pw):
    return bcrypt.check_password_hash(hashed_pw.encode('utf-8'), pw.encode('utf-8'))