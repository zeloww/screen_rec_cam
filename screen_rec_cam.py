import numpy as np
import win32clipboard, win32gui, win32con, sys

from time import sleep
from io import BytesIO
from shutil import rmtree
from ctypes import windll
from random import choice
from threading import Thread
from PIL import ImageGrab, Image
from os import system, remove, makedirs, path

try:
	import cv2
except:
	system("pip install opencv-python")
	import cv2

#vitesse

screen_rec = """
  ██████  ▄████▄   ██▀███  ▓█████ ▓█████  ███▄    █     ██▀███  ▓█████  ▄████▄  
▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀ ▓█   ▀  ██ ▀█   █    ▓██ ▒ ██▒▓█   ▀ ▒██▀ ▀█  
░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒███   ▒███   ▓██  ▀█ ██▒   ▓██ ░▄█ ▒▒███   ▒▓█    ▄ 
  ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄ ▒▓█  ▄ ▓██▒  ▐▌██▒   ▒██▀▀█▄  ▒▓█  ▄ ▒▓▓▄ ▄██▒
▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒░▒████▒░▒████▒▒██░   ▓██░   ░██▓ ▒██▒░▒████▒▒ ▓███▀ ░
▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░░░ ▒░ ░░░ ▒░ ░░ ▒░   ▒ ▒    ░ ▒▓ ░▒▓░░░ ▒░ ░░ ░▒ ▒  ░
░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░ ░ ░  ░ ░ ░  ░░ ░░   ░ ▒░     ░▒ ░ ▒░ ░ ░  ░  ░  ▒   
░  ░  ░  ░          ░░   ░    ░      ░      ░   ░ ░      ░░   ░    ░   ░        
      ░  ░ ░         ░        ░  ░   ░  ░         ░       ░        ░  ░░ ░      
         ░                                                             ░        
                                1 >>> SCREEN
                                2 >>> REC
                                3 >>> CAM"""

def minimise_window():
	Minimize = win32gui.GetForegroundWindow()
	win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def png2video(frames_list:list, extension:str, random_numbers:int):
	img_array = []
	for filename in frames_list:
		img = cv2.imread("frames/" + filename)
		height, width, layers = img.shape
		size = (width,height)
		img_array.append(img)

	out = cv2.VideoWriter(f"unknown_zelow[{random_numbers}]." + extension, cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

	for i in range(len(img_array)):
		out.write(img_array[i])
	out.release()

	rmtree("frames")

def on_input():
	press = input("\nPress a key to break rec\n>>> ")

	global stop
	stop = True

	return print("\nRec succesfully stopped!")

def screen():
	copy = input("Copy or just save? [c/s] >>> ").lower()
	if copy == "c":
		copy = True
	elif copy == "s":
		copy = False
	else:
		return input("Bad choice!")

	print("\n3"), sleep(1)
	print("2"), sleep(1)
	print("1"), sleep(1)
	minimise_window(), sleep(1)

	random_numbers = choice(range(111, 999))

	#get screen
	img = ImageGrab.grab()
	img_np = np.array(img)

	frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
	cv2.imwrite(f"unknown_zelow[{random_numbers}].png", frame)

	#copy to clipboard
	image = Image.open(f"unknown_zelow[{random_numbers}].png")

	output = BytesIO()
	image.convert("RGB").save(output, "BMP")
	data = output.getvalue()[14:]
	output.close()

	if copy:
		send_to_clipboard(win32clipboard.CF_DIB, data)
		remove(f"unknown_zelow[{random_numbers}].png")

		return input("\nCopied!")

	else:
		return input("\nSaved!\n" + path.abspath(f"unknown_zelow[{random_numbers}].png"))

def rec():
	frames_list = []
	makedirs(f"frames/", exist_ok=True)

	extension = input("Video extension (mp4, mp3, ...) >>> ").replace(".", "").lower()

	print("\n3"), sleep(1)
	print("2"), sleep(1)
	print("1"), sleep(1)

	minimise_window(), sleep(1)

	#get rec
	global stop
	stop = False

	thread = Thread(target=on_input)
	thread.start()

	i = 0
	while stop is not True:
		i += 1

		img = ImageGrab.grab()
		img_np = np.array(img)

		frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

		random_name = f"unknown_zelow[{i}].png"
		cv2.imwrite("frames/" + random_name, frame)
		frames_list.append(random_name)

	try:
		cv2.release()
		cv2.destroyAllWindows()
	except:
		pass

	random_numbers = choice(range(111, 999))
	png2video(frames_list, extension, random_numbers)

	return input("\nSaved!\n"  + path.abspath(f"unknown_zelow[{random_numbers}]." + extension))

def cam():
	print("Press 'q' on the new window to break cam")

	print("\n3"), sleep(1)
	print("2"), sleep(1)
	print("1"), sleep(1)

	minimise_window()

	cap = cv2.VideoCapture(0)

	while True:
		ret, img=cap.read()
		cv2.imshow("by github.com/zeloww", img)

		if cv2.waitKey(25) & 0xFF == ord('q'):
			break

	try:
		cap.release()
		cap.destroyAllWindows()
	except:
		pass

def main():
	system("color d")

	while True:
		system("cls")
		print(screen_rec)

		choice = input(">>> ")

		if choice == "1":
			screen()
		elif choice == "2":
			rec()
		elif choice == "3":
			cam()
		else:
			input("Invalid choice!")

if __name__ == "__main__":
	main()