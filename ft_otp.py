import sys
from cryptography.fernet import Fernet
import hashlib
import time
###
import base64
import struct
import hmac
import math

if sys.argv[1] == "-g":
    #open the original txt file, read and join them as one string
    f = open(sys.argv[2], "r")
    l = (f.readlines())
    string = '\n'.join([line.strip() for line in l])
    print ("original string:", string)
    #transform to hex
    hexKey = ""
    for c in string:
        # ord transforms to decimal and zfill adds a 0 if necessary 
        # to ensure it has 2 digits then is converted to hexadecimal
        hexVal = hex(ord(c))[2:].zfill(2)
        hexKey += hexVal
    print("len of hexKey is", len(hexKey))
    print("hexKey =", hexKey)
    #check if the length of the hexadecimal key is at least 64 characters
    if len(hexKey) < 64:
        print("error: key must be 64 hexadecimal characters.")
    else:
        #create/open and store the key
        with open("ft_otp.key", "w") as storehex:
            storehex.write(hexKey)
        #encrypt the file where the key is stored
        # encrypted = storestring.encrypt(storestring)
        print("Key was successfully saved in ft_otp.key.")

if sys.argv[1] == "-k":
    #open the file and read as bytes, store into secret
    with open(sys.argv[2], "r") as inputF:
        secret = inputF.read()
    bytesSecret = secret.encode("utf-8")
    b32Secret = base64.b32encode(bytesSecret)
    lenOtp = 6
    otpSteps = 30
    currentTime = math.floor(time.time() / otpSteps)    #generate steps from start of time and use floor
                                                        #to round the number if necessary
    
    msg = currentTime.to_bytes(8, byteorder='big')
    key = base64.b32decode(b32Secret)
    
    hmac1 = hmac.new(key, msg, hashlib.sha1).digest()
    
    offset = hmac1[-1] & 0x0f
    truncatedHash = hmac1[offset:offset + 4]
    totp = int.from_bytes(truncatedHash, byteorder='big') & 0x7fffffff
    totp %= 10 ** lenOtp
    
    print(totp)
    # hash = hmac.new(bytes(secret, encoding="utf-8"), currentTime.to_bytes(length=8, byteorder="big"), hashlib.sha1, )
    
    # bitstring = bin(int(hash.hexdigest(), base=16)) #convert hast to binary string
    # print("bitstring =", bitstring)
    # last4bits = bitstring[-4:] #get last four bits
    # print("last4bits =", last4bits)
    # offset = int(last4bits, base=2) #use last4bits as offset
    # print("offset =", offset)
    # takeBits = bitstring[offset:offset * 8] #use the offset and get next 32bits of the string
    # print("takeBits =", takeBits)
    # code = str(int(takeBits, base=2)) #convert the taken bits to int
    # print("code1 =", code)
    # code = code[-lenOtp:] #get the last digits
    # print(code)
    
    # while len(secret) % 8 != 0:
    #     secret += b"="
    # key = base64.b32decode(secret)
    
    # for ix in range(-2, 3):
    #     b = struct.pack(">q", currentTime + ix)
    #     hm = hmac.HMAC(key, b, hashlib.sha1).digest()
    #     offset = hm[-1] & 0x0F
    #     truncatedHash = hm[offset:offset + 4]
    #     code = struct.unpack(">L", truncatedHash)[-1]
    #     code &= 0x7FFFFFFF
    #     code %= 1000000
    # print(code)
    
    #currentTime = 0

    #calculate the number of intervals since unix epoch
    #this allows to generate the same OTP in a time given window
    # intervalC = int(currentTime // otpInterval)
            # #intervalC = otpInterval
            # #we convert the interval to bytes so It can be use with sha256
            # #that only uses bytes, I was going to use little endian for the
            # # performance but Raul told me to use big endian so..., weuse a length of 4 bytes as is sufficient
            # #for most applications
            # intervalCBytes = intervalC.to_bytes(8, byteorder='big')
            # #we calculate the hash of the secret and the interval count
            # #digests is used as a binary representation of the hash
            # shaResult = hashlib.sha1(secret + intervalCBytes).digest()
            # #extract the last 5 bytes of the binary of the hash, except the last one
            # #because is the offset
            # fourBytes = shaResult[-4:]
            # #convert the 4 bytes to int and make the modulo of the len we want of the otp pass
            # otp = int.from_bytes(fourBytes, byteorder='big') % (10 ** lenOtp)
            # #we use zfill to add the 0's so it matches the lenOtp
            # otpStr = str(otp).zfill(lenOtp)
            # print(otpStr)

#ref https://totp.youngforest.me/
        
#ref https://hackernoon.com/implementing-2fa-how-time-based-one-time-password-actually-works-with-python-examples-cm1m3ywt

#ref https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/