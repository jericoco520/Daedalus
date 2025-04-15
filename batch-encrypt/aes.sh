#!/bin/bash

KEY="aes_key.bin"
IV="aes_IV.bin"

[[ ! -f $KEY ]] && openssl rand -out $KEY 32
[[ ! -f $IV ]] && openssl rand -out $IV 16

mkdir -p enc

if [[ $1 == "encrypt" ]]; then
    for file in image/*.png; do
        [[ -f "$file" ]] || continue
        openssl enc -aes-256-cbc -salt -pbkdf2 -in "$file" -out "enc/$(basename "$file").enc" -K "$(xxd -p $KEY | tr -d '\n')" -iv "$(xxd -p $IV | tr -d '\n')"
    done
elif [[ $1 == "decrypt" ]]; then
    for file in enc/*.png.enc; do
        [[ -f "$file" ]] || continue
        openssl enc -d -aes-256-cbc -salt -pbkdf2 -in "$file" -out "enc/$(basename "${file%.enc}")" -K "$(xxd -p $KEY | tr -d '\n')" -iv "$(xxd -p $IV | tr -d '\n')"
    done
elif [[ $1 == "xcrypt" ]]; then
    for file in image/*.png; do
        [[ -f "$file" ]] || continue
        openssl enc -aes-256-cbc -salt -pbkdf2 -in "$file" -out "enc/$(basename "$file").enc" -K "$(xxd -p $KEY | tr -d '\n')" -iv "$(xxd -p $IV | tr -d '\n')"
    done
    for file in enc/*.png.enc; do
        [[ -f "$file" ]] || continue
        openssl enc -d -aes-256-cbc -salt -pbkdf2 -in "$file" -out "enc/$(basename "${file%.enc}")" -K "$(xxd -p $KEY | tr -d '\n')" -iv "$(xxd -p $IV | tr -d '\n')"
    done
else
    echo "Usage: $0 encrypt|decrypt|xcrypt"
fi
