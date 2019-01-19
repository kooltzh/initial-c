from Crypto import Random
import base64
from os import chmod
from Crypto.PublicKey import RSA

def load_keys(filename):
    # load private key
    prikey = RSA.importKey(open(filename + "pri.key", "rb").read())
    # load public key
    pubkey = RSA.importKey(open(filename + "pub.key", "rb").read())
    return prikey, pubkey

def save_keys(filename):
    prikey, pubkey = gen_keys()
    # save private key
    try:
        with open(filename + "private.key", 'wb') as content_file:
            chmod(filename + "private.key", 600)
            content_file.write(prikey.exportKey('PEM'))
    except:
        print('open private file error')
    # save public key
    with open(filename + "public.key", 'wb') as content_file:
        content_file.write(pubkey.exportKey('OpenSSH'))

    return prikey, pubkey


def gen_keys():
	# RSA modulus length must be a multiple of 256 and >= 1024
	modulus_length = 256*4  # use larger value in production
	prikey = RSA.generate(modulus_length, Random.new().read)
	pubkey = prikey.publickey()
	return prikey, pubkey


def encrypt_msg(msg, pubkey):
	encrypted_msg = pubkey.encrypt(msg.encode(), 32)[0]
	# base64 encoded strings are database friendly
	encoded_encrypted_msg = base64.b64encode(encrypted_msg)
	return encoded_encrypted_msg


def decrypt_msg(encoded_encrypted_msg, prikey):
	decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
	decoded_decrypted_msg = prikey.decrypt(decoded_encrypted_msg)
	return decoded_decrypted_msg.decode()

########## BEGIN ##########

if __name__ == '__main__':
    msg = "The quick brown fox jumped over the lazy dog"
    prikey, pubkey = gen_keys()
    encrypted_msg = encrypt_msg(msg, pubkey)
    decrypted_msg = decrypt_msg(encrypted_msg, prikey)

    print ("%s - (%d)" % (prikey.exportKey(), len(prikey.exportKey())))
    print ("%s - (%d)" % (pubkey.exportKey(), len(pubkey.exportKey())))
    print ("Original content: %s - (%d)" % (msg, len(msg)))
    print ("Encrypted msg: %s - (%d)" % (encrypted_msg, len(encrypted_msg)))
    print("Decrypted msg: %s - (%d)" % (decrypted_msg, len(decrypted_msg)))
    
    save_keys('')
    print(load_keys(''))
