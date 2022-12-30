# Diarykeeper
An offline diary keeper, secured by SHA-256 hashing and Twofish encryption algorithm.

## Features
- `Account management` (Delete Account, Change Password)
- `Portability`
- `Access logs` with time
- SHA-256 `Hashing` for password
- `Twofish Encryption` Algorithm security
- Multiple diaries
- CTRL+S to save shortcut
- A prompt to make sure you wanted to quit
- Fully offline

## Preview
TBA

## TODO
- Add pages feature
- revamp logs(?)

## Dependencies
- tkinter
- passlib
- twofish (included)

## How to install
**`Source Code`**
- Install [`python`](https://www.python.org/downloads/)
- clone via `https://github.com/Not-Baguette/Diarykeeper.git` or `download zip`

![image](https://user-images.githubusercontent.com/94969176/210039816-198fdf21-a270-4ccd-aaf8-62fa8e3e2901.png)

- Open the zip/folder and unpack if needed
- install the dependencies
- run `main.py`

**`Release`**
- Not done yet


## Warning
Anyone with decent enough coding or cryptography skill could crack it if you aree using the source code method. This program isn't really suitable for it because it shows how this program fully work, thus abling them to reverse it. I might be able to fix this in the future but if you're using the compiled version, they should be having a hard time with it. I also doubt anyone would do so far to decrypt it too though, but if you're paranoid, there's always an option of taking the diary file on a usb

## How to move
- For basic functionalities, you can just move `accounts_db.db` and your diary to a new pc and install this again there. but to keep the log, you can also move `logs_db.db`. Same thing to remove it, you can just remove it via the in-app `Delete account feature`
