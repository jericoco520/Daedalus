#!/bin/bash

KEY="aes_key.bin"
IV="aes_IV.bin"

[[ ! -f $KEY ]] && openssl rand -out $KEY 32
[[ ! -f $IV ]] && openssl rand -out $IV 16

mkdir -p enc dec

if [[ $1 == "encrypt" ]]; then
    for file in image/*.png image/*.zip; do
        [[ -f "$file" ]] || continue
        openssl enc -aes-256-cbc -salt -in "$file" -out "enc/$(basename "$file").enc" -K "$(xxd -p $KEY | tr -d '\n')" -iv "$(xxd -p $IV | tr -d '\n')"
    done
elif [[ $1 == "decrypt" ]]; then
    for file in enc/*.png.enc enc/*.zip.enc; do
        [[ -f "$file" ]] || continue
        openssl enc -d -aes-256-cbc -salt -in "$file" -out "dec/$(basename "${file%.enc}")" -K "$(xxd -p $KEY | tr -d '\n')" -iv "$(xxd -p $IV | tr -d '\n')"
    done
elif [[ $1 == "zcrypt" ]]; then
    # Check if there are any PNG files, and if so, create a zip of them
    if compgen -G "image/*.png" > /dev/null; then
        zip -j image/images.zip image/*.png
    fi
    # Encrypt the zip files
    for file in image/*.zip; do
        [[ -f "$file" ]] || continue
        openssl enc -aes-256-cbc -salt -in "$file" -out "enc/$(basename "$file").enc" -K "$(xxd -p $KEY | tr -d '\n')" -iv "$(xxd -p $IV | tr -d '\n')"
    done
    # Decrypt the encrypted zip files
    for file in enc/*.zip.enc; do
        [[ -f "$file" ]] || continue
        openssl enc -d -aes-256-cbc -salt -in "$file" -out "dec/$(basename "${file%.enc}")" -K "$(xxd -p $KEY | tr -d '\n')" -iv "$(xxd -p $IV | tr -d '\n')"
        
        # If the decrypted file is a zip file, unzip it
        if [[ "${file}" == *.zip.enc ]]; then
            unzip "dec/$(basename "${file%.enc}")" -d "dec/$(basename "${file%.enc}" .zip)"
            echo "Unzipped: dec/$(basename "${file%.enc}")"
        fi
    done
elif [[ $1 == "xcrypt" ]]; then
    for file in image/*.png image/*.zip; do
        [[ -f "$file" ]] || continue
        openssl enc -aes-256-cbc -salt -in "$file" -out "enc/$(basename "$file").enc" -K "$(xxd -p $KEY | tr -d '\n')" -iv "$(xxd -p $IV | tr -d '\n')"
    done
    for file in enc/*.png.enc enc/*.zip.enc; do
        [[ -f "$file" ]] || continue
        openssl enc -d -aes-256-cbc -salt -in "$file" -out "dec/$(basename "${file%.enc}")" -K "$(xxd -p $KEY | tr -d '\n')" -iv "$(xxd -p $IV | tr -d '\n')"
    done
else
    echo "Usage: $0 encrypt|decrypt|zcrypt|xcrypt"
fi
