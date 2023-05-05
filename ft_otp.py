import sys
from cryptography.fernet import Fernet
import hashlib
import time
import hmac
import math

def encryptAndDecrypt(flag, stringIn):
    # generate key, encrypt string, store encrypted string and the key
    if flag == 1:
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encryptedString = fernet.encrypt(stringIn.encode())
        with open("encryptionKey.txt", "wb") as f:
            f.write(key)
        with open("ft_otp.key", "wb") as f:
            f.write(encryptedString)
    # decript the file and return it
    if flag == 0:
        with open("encryptionKey.txt", "rb") as f:
            key = f.read()
        fernet = Fernet(key)
        decryptedString = fernet.decrypt(stringIn).decode()
        return decryptedString

def checkif64hex(stringToCheck):
    validChars = set('0123456789abcdef')
    for x in stringToCheck:
        if x not in validChars or len(stringToCheck) < 64:
            raise ValueError("Error: key must be 64 hexadecimal characters.")

if sys.argv[1] == "-g":
    #open the original txt file, read and join them as one string
    with open(sys.argv[2], "r") as inputF:
        hexKey = inputF.read()
    #check if the length of the hexadecimal key is at least 64 characters
    checkif64hex(hexKey)
    encryptAndDecrypt(1, hexKey)

if sys.argv[1] == "-k":
    lenOtp = 6
    otpSteps = 30    
    #open the file and read as bytes, store into secret
    with open(sys.argv[2], "r") as inputF:
        encryptedString = inputF.read()
    key = encryptAndDecrypt(0, encryptedString).encode("utf-8")
    currentTime = math.floor(time.time() / otpSteps)    #generate steps from start of time and use floor
                                                        #to round the number if necessary
    msg = currentTime.to_bytes(8, byteorder='big')
    hmac1 = hmac.new(key, msg, hashlib.sha1).digest()
    offset = hmac1[-1] % 16 #take the last byte and take the remainder of the division
    truncatedHash = hmac1[offset:offset + 4] #extract from offset the next 4 bytes
    totp = int.from_bytes(truncatedHash, byteorder='big') % (10 ** lenOtp)  #convert bytes to int and discard
                                                                            #the extra digits
    totpStr = str(totp).zfill(lenOtp)
    print(totpStr)


#ref https://totp.youngforest.me/
        
#ref https://hackernoon.com/implementing-2fa-how-time-based-one-time-password-actually-works-with-python-examples-cm1m3ywt

#ref https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/