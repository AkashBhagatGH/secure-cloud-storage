from cryptography.fernet import Fernet
import os 

if not os.path.exists("secret.key"):
    with open("secret.key","wb") as f:
        f.write(Fernet.generate_key())

def load_key():
    with open("secret.key","rb") as f:
     return f.read()
    
def encrypt_file(input_file,output_file):
    key = load_key()
    fernet = Fernet(key)
    with open(input_file,"rb") as f:
      data = f.read()
      encrypt_data = fernet.encrypt(data)

    with open(output_file,"wb") as f:
       f.write(encrypt_data)

def decrypt_file(input_file,output_file):
   key = load_key()
   fernet = Fernet(key)

   with open(input_file,"rb") as f:
    encrypt_data = f.read()  
   decrypt_data = fernet.decrypt(encrypt_data)

   with open(output_file,"wb") as f:
      f.write(decrypt_data)


      