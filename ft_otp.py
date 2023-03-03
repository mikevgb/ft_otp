import sys
from cryptography.fernet import Fernet

if sys.argv[1] == "-g":
    #open the original txt file, read and join them as one string
    f = open(sys.argv[2], "r")
    l = (f.readlines())
    string = '\n'.join([line.strip() for line in l])
    print (string)
    #check if the length of the hexadecimal key is at least 64 characters
    if len(string) < 64:
        print("error: key must be 64 hexadecimal characters.")
    else:
        #open and store the key
        storestring = open("ft_otp.key", "wb") 
        storestring.write(string)
        storestring.close()
        #encrypt the file where the key is stored
        encrypted = storestring.encrypt(storestring)
        print("Key was successfully saved in ft_otp.key.")

if sys.argv[1] == "-d":
    


if sys.argv[1] == "-k":


#ref https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/