Make it executable:
chmod +x rebel_aes.sh

To Encrypt:
./aes.sh encrypt 

To Decrypt:
./aes.sh decrypt 

To encrypt/decrypt in one
./aes.sh xcrypt


The script generates and stores two files that contain the encryption key and IV (Initialization Vector). These files ensure encryption can be repeated without requiring a password.
You could bypass the need for this by using a password. OpenSSL will then derive a key from the password using PBKDF2

Bonus:
If you want the script to work from anywhere, you can
move it to /usr/local/bin/ (optional for global usage):

```sudo mv aes.sh /usr/local/bin/aes```
```chmod +x /usr/local/bin/aes```

Run from any directory:
```aes encrypt /path/to/image.png```