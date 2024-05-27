from passlib.hash import pbkdf2_sha256

nome = 'douglas'
nome_falso = 'douglass' #Vai retornar falso

criptografando = pbkdf2_sha256.hash(nome)
ver_senha = pbkdf2_sha256.verify(nome_falso, criptografando)

print(criptografando, ver_senha)