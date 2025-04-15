Make it executable:
chmod +x aes.sh

On the command line:
	To Encrypt:
	./aes.sh encrypt 

	To Decrypt:
	./aes.sh decrypt 

	To encrypt/decrypt in one
	./aes.sh zcrypt

Python script:
	python run.py

The script generates and stores two files that contain the encryption key and IV (Initialization Vector). These files ensure encryption can be repeated without requiring a password.

If you want the script to work from anywhere, you can
move it to /usr/local/bin/ (optional for global usage):

```sudo mv aes.sh /usr/local/bin/aes```
```chmod +x /usr/local/bin/aes```

Run from any directory:
```aes encrypt /path/to/image.png```