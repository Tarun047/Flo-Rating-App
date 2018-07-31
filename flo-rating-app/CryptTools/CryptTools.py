from secretsharing import PlaintextToHexSecretSharer
import base64
import os
from Crypto.Cipher import AES
import subprocess
from more_itertools import sliced
import json
from fpdf import FPDF
import pyperclip


def pad(data):
    padding = 16 - len(data) % 16
    return data + padding * chr(padding+97)

def unpad(data):
    data = str(data)
    padding =  ord(data[-2]) - 96
    return data[2:-padding]

def keyGen():
    # Generating random key of 32 bytes
    key = os.urandom(32)
    return key


def encryptMsg(plaintext, key):
    # Genarating Initialization vector for AES (16 bytes)
    IV = os.urandom(16)
    # Encrypting The plaintext
    cipher = AES.new(key, AES.MODE_CBC, IV)
    plaintext=base64.b64encode(plaintext.encode('utf-8')).decode('utf-8')
    ciphertext = cipher.encrypt(pad(plaintext).encode('utf-8'))
    # Append IV and Ciphertext
    ciphertext = base64.b64encode(IV).decode('utf-8') + base64.b64encode(ciphertext).decode('utf-8')
    return ciphertext


def decryptMsg(ciphertext, key):
    # Initialization vector in AES should be 16 bytes
    IV = base64.b64decode(ciphertext[:24])
    ciphertext=base64.b64decode(ciphertext[24:])
    # Creation of encryptor and decryptor object using above details
    cipher = AES.new(key, AES.MODE_CBC, IV)
    plaintext=unpad(cipher.decrypt(ciphertext));
    plaintext = (base64.b64decode(plaintext)).decode('utf-8')
    return plaintext
