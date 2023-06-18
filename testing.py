from hashlib import md5
password = md5(input("Ingrese pass: ").encode())
print(password.hexdigest())