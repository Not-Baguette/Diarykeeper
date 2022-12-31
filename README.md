# Diarykeeper
An offline diary keeper, secured by SHA-256 hashing and Twofish encryption algorithm.

## Features
- `Account management` (Delete Account, Change Password)
- `Portability`
- Private `Access logs` with time for all accounts
- SHA-256 `Hashing` for password
- `Twofish Encryption` Algorithm security
- Multiple diaries
- CTRL+S to save shortcut
- A prompt to make sure you wanted to quit
- Fully offline

## Preview
![image](https://user-images.githubusercontent.com/94969176/210125568-af2378b5-76ea-466a-b11f-512349a91974.png)

![image](https://user-images.githubusercontent.com/94969176/210125578-1a8207dc-c23a-4b77-859f-4fed60f88b50.png)

![image](https://user-images.githubusercontent.com/94969176/210125606-1725a920-025b-4812-95e8-cb2a3faf9453.png)

![image](https://user-images.githubusercontent.com/94969176/210125649-6179ff9d-00d1-48e8-82d3-2e00601563ac.png)

## TODO
- [ ] Add pages feature
- [ ] revamp logs(?)
- [ ] clean log of a certain id once the account is deleted(?)

## Dependencies
- Tkinter
- Passlib
- Twofish (included)

## How to install
**`Source Code`**
- Install [`python`](https://www.python.org/downloads/)
- Clone via `https://github.com/Not-Baguette/Diarykeeper.git` or `download zip`

![image](https://user-images.githubusercontent.com/94969176/210039816-198fdf21-a270-4ccd-aaf8-62fa8e3e2901.png)

- Open the zip/folder and unpack if needed
- Install the dependencies
- Run `main.py`

**`Release`**
- Not done yet

## How to use
- Install the app either via `.exe` on release or Source code
- Open the app or `main.py`
- You will be greeted with this page and a file called accounts_db.db should appear in the current directory (folder) 
- Write a username you want and click `Create account`

![image](https://user-images.githubusercontent.com/94969176/210125837-f00ac8a0-0a00-4289-a330-6f052db9c5b1.png)

- If your account name and password meets the requirement, it will show `Account created. Please log in`, simply log in

![image](https://user-images.githubusercontent.com/94969176/210125927-6690d339-ad93-4de1-a990-70bc016f0e92.png)

- You should be presented with an app similar to notepad, simply click `File > Open`

![image](https://user-images.githubusercontent.com/94969176/210126002-f41fc2ea-4662-46e8-af55-01094ea4651c.png)

- Navigate to a `.dry` file, If you haven't, open `File Explorer` and make it anywhere you need

![image](https://user-images.githubusercontent.com/94969176/210126036-0a13fd6a-8b77-485b-921b-e0503b9c45bd.png)

![image](https://user-images.githubusercontent.com/94969176/210126049-4f8e2bbc-0408-4e5e-9bca-633ad4b83b7b.png)

![image](https://user-images.githubusercontent.com/94969176/210126055-2255d303-a058-4715-bdd4-75e1df55a447.png)

- Click `Open` and you should be back with the directory name on the top

![image](https://user-images.githubusercontent.com/94969176/210126067-15a747ad-a170-44de-b37a-3ef0d7e2983a.png)

- Write whatever you want or need to and once you're done, either click `Ctrl+S` or `File > Save`

![image](https://user-images.githubusercontent.com/94969176/210126123-31f35a19-25d5-40bf-a14d-a3246455f356.png)

- And you're done! The diary page cannot be accessed by anyone else except you. (What would appear if you try to open it with another account or notepad)

![image](https://user-images.githubusercontent.com/94969176/210126195-b66a3a4e-906e-4ceb-b42f-2be366dd1a90.png)


## Warning
Anyone with decent enough coding or cryptography skill could crack it if you aree using the source code method. This program isn't really suitable for it because it shows how this program fully work, thus abling them to reverse it. I might be able to fix this in the future but if you're using the compiled version, they should be having a hard time with it. I also doubt anyone would do so far to decrypt it too though, but if you're paranoid, there's always an option of taking the diary file on a usb

## How to move
For basic functionalities, you can just move `accounts_db.db` and your diary to a new pc and install this again there. but to keep the log, you can also move `logs_db.db`. Same thing to remove it, you can just remove it via the in-app `Delete account feature`
