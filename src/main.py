import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from cryptography.fernet import Fernet, InvalidToken
import re

tk = Tk()
tk.title('Vaultify')
tk.geometry('400x300')

def fernet_key_generate():
	key = Fernet.generate_key()

	filetypes = [
		('Anahtar dosyaları', '*.key'),
		('Tüm dosyalar', '*.*')
	]

	f = filedialog.asksaveasfile(mode = 'wb', defaultextension = '.key', filetypes = filetypes)

	f.write(key)
	f.close()

fernetKey = ''
def fernet_key_load():
	global fernetKey

	filetypes = [
		('Anahtar dosyaları', '*.key'),
		('Tüm dosyalar', '*.*')
	]

	fernetKey = filedialog.askopenfilename(title = 'Güvenlik anahtarınızı seçin.', filetypes = filetypes)

	if (fernetKey != ''):
		selectFernetKey.config(text = 'Güvenlik Anahtarı Değiştir (Seçili: {})' . format(fernetKey))
	else:
		selectFernetKey.config(text = 'Güvenlik Anahtarı Seç')

def encrypt():
	if (fernetKey != '' and selectedDir != ''):
		with open(fernetKey, 'rb') as f:
			fernetKeyRead = f.read()
			f.close()

		fernet = Fernet(fernetKeyRead)

		filesToEncrypt = []
		for path, subdirs, files in os.walk(selectedDir):
			for name in files:
				if (re.search(r'\.(.*)$', name, re.IGNORECASE)):
					if (re.search(r'\.vaultify_locker$', name, re.IGNORECASE)):
						pass
					else:
						filesToEncrypt.append(str(os.path.join(path, name)))

		if (len(filesToEncrypt) == 0):
			messagebox.showerror('Hata!', 'Dizin içerisinde şifrelenebilecek dosya bulunamadı.')
			return

		for file in filesToEncrypt:
			with open(file, 'rb') as f:
				encrypted = fernet.encrypt(f.read())
				f.close()

			with open(file, 'wb') as f:
				f.write(encrypted)
				f.close()

				os.rename(file, file + '.vaultify_locker')

		messagebox.showinfo('Başarılı!', 'Dosyalar başarıyla şifrelendi. Dosyaları deşifre etmeden ilgili dizinde dosya silmek dışında değişiklik yapmayın!')
	else:
		messagebox.showerror('Hata!', 'Güvenlik anahtarı ve/veya dizin seçilmedi!')

def decrypt():
	if (fernetKey != '' and selectedDir != ''):
		with open(fernetKey, 'rb') as f:
			fernetKeyRead = f.read()
			f.close()

		fernet = Fernet(fernetKeyRead)

		filesToDecrypt = []
		for path, subdirs, files in os.walk(selectedDir):
			for name in files:
				if (re.search(r'\.(.*)$', name, re.IGNORECASE)):
					if (re.search(r'\.vaultify_locker$', name, re.IGNORECASE)):
						filesToDecrypt.append(str(os.path.join(path, name)))

		if (len(filesToDecrypt) < 1):
			messagebox.showerror('Hata!', 'Dizin içerisinde şifrelenmiş dosya bulunamadı.')
			return

		for file in filesToDecrypt:
			print(file)
			with open(file, 'rb') as f:
				try:
					decrypted = fernet.decrypt(f.read())
				except InvalidToken:
					messagebox.showerror('Hata!', 'Güvenlik anahtarı ilgili dosyalar için geçerli değil.')
					return

				f.close()

			with open(file, 'wb') as f:
				f.write(decrypted)
				f.close()

				os.rename(file, file.rsplit('.', 1)[0])

		messagebox.showinfo('Başarılı!', 'Dosyalar deşifre edildi.')
	else:
		messagebox.showerror('Hata!', 'Güvenlik anahtarı ve/veya dizin seçilmedi!')

selectedDir = ''
def selectDir():
	global selectedDir

	selectedDir = filedialog.askdirectory(title = 'İşlem dizinini seçin.')

	if (selectedDir != ''):
		selectDirBtn.config(text = 'Dizin Değiştir (Seçili: {})' . format(selectedDir))
	else:
		selectDirBtn.config(text = 'Dizin Seç')

selectDirBtn = Button(tk, text = 'Dizin Seç', width = 50, wraplength = 300, command = selectDir)
selectDirBtn.pack(padx = 10, pady = 10)

generateFernetKey = Button(tk, text = 'Güvenlik Anahtarı Oluştur', width = 50, command = fernet_key_generate)
generateFernetKey.pack(padx = 10, pady = 10)

selectFernetKey = Button(tk, text = 'Güvenlik Anahtarı Seç', width = 50, wraplength = 300, command = fernet_key_load)
selectFernetKey.pack(padx = 10, pady = 10)

encryptButton = Button(tk, text = 'Şifrele', width = 50, command = encrypt)
encryptButton.pack(padx = 10, pady = 10)

decryptButton = Button(tk, text = 'Deşifre Et', width = 50, command = decrypt)
decryptButton.pack(padx = 10, pady = 10)

tk.mainloop()