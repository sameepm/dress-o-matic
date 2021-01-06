import os
import random

import tkinter as tk
from PIL import Image, ImageTk
from playsound import playsound

WINDOW_TITLE = "Dress-o-matic"
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 220
IMG_WIDTH = 250
IMG_HEIGHT = 250
COLOR_HEX = '#FFFFFF'

#store wardrobe Tops into file
ALL_TOPS = [str("tops/") + file for file in os.listdir("tops/") if not file.startswith('.')]
ALL_BOTTOMS = [str("bottoms/") + file for file in os.listdir("bottoms/") if not file.startswith('.')]

class WardrobeApp:
	def __init__(self, root):
		self.root = root

		#gather tops
		self.top_images = ALL_TOPS
		self.bottom_images = ALL_BOTTOMS

		#select starting point outfit
		self.tops_image_path = self.top_images[0]
		self.bottom_image_path = self.bottom_images[0]

		#solidify the frame and add the top
		self.tops_frame = tk.Frame(self.root, bg = COLOR_HEX)
		self.top_image_label = self.create_photo(self.tops_image_path, self.tops_frame)
		self.top_image_label.pack(side=tk.TOP)

		#solidify frame and add bottom
		self.bottoms_frame = tk.Frame(self.root, bg = COLOR_HEX)
		self.bottom_image_label = self.create_photo(self.bottom_image_path, self.bottoms_frame)
		self.bottom_image_label.pack(side=tk.TOP)

		self.create_background()

	def create_background(self):
		
		#adding a title to window
		self.root.title(WINDOW_TITLE)

		#changing size of window
		self.root.geometry('{0}x{1}'.format(WINDOW_WIDTH, WINDOW_HEIGHT))

		#add the buttons
		self.create_buttons()

		#add clothing into the frame
		self.tops_frame.pack(fill=tk.BOTH, expand=tk.YES)
		self.bottoms_frame.pack(fill=tk.BOTH, expand=tk.YES)

	def create_buttons(self):

		#pressing previous for top
		top_prev_button = tk.Button(self.tops_frame, text = "<<", command = self.get_prev_top)
		top_prev_button.pack(side=tk.LEFT)

		#pressing next for top
		top_next_button = tk.Button(self.tops_frame, text = ">>", command = self.get_next_top)
		top_next_button.pack(side=tk.RIGHT)

		#pressing previous for bottom
		bottom_prev_button = tk.Button(self.bottoms_frame, text = "<<", command = self.get_prev_bottom)
		bottom_prev_button.pack(side=tk.LEFT)

		#pressing next for bottom
		bottom_next_button = tk.Button(self.bottoms_frame, text = ">>", command = self.get_next_bottom)
		bottom_next_button.pack(side=tk.RIGHT)

		#randomize random outift
		create_outfit_button = tk.Button(self.tops_frame, text = " Create Outfit ", command=self.create_outfit)
		create_outfit_button.pack(side = tk.LEFT)

	#general function for navigation forward and back
	def get_next_item(self, current_item, category, increment=True):
		item_index = category.index(current_item)
		final_index = len(category) - 1
		next_index = 0

		#need to consider overflow cases
		#if on last element, circle back to first
		print("item index: " + str(item_index))
		print("final_index: " + str(final_index))

		if increment and item_index == final_index:
			next_index = 0

		#if on first elemnt and need to go prev, cycle back to last
		elif not increment and item_index == 0:
			next_index = final_index
		#else treat like normal incrementing
		else:
			incrementFactor = 1 if increment else -1
			next_index = item_index + incrementFactor

		next_image = category[next_index]

		#update image in display
		if current_item in self.top_images:
			image_label = self.top_image_label
			self.tops_image_path = next_image
		else:
			image_label = self.bottom_image_label
			self.bottom_image_path = next_image

		self.update_image(next_image, image_label)

	def get_next_top(self):
		self.get_next_item(self.tops_image_path, self.top_images, increment=True)

	def get_prev_top(self):
		self.get_next_item(self.tops_image_path, self.top_images, increment=False)

	def get_next_bottom(self):
		self.get_next_item(self.bottom_image_path, self.bottom_images, increment=True)

	def get_prev_bottom(self):
		self.get_next_item(self.bottom_image_path, self.bottom_images, increment=False)

	def update_image(self, new_image_path, image_label):
		#collect and change image
		image_file = Image.open(new_image_path)
		image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
		tk_photo = ImageTk.PhotoImage(image_resized)

		#update based on provided label
		image_label.configure(image=tk_photo)

		image_label.image = tk_photo


	def create_photo(self, image_path, frame):
		image_file = Image.open(image_path)
		image_resized = image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.ANTIALIAS)
		tk_photo = ImageTk.PhotoImage(image_resized)
		image_label = tk.Label(frame, image=tk_photo, anchor=tk.CENTER)
		image_label.image = tk_photo

		return image_label

	def create_outfit(self):
		#generate random indices
		rand_top_index = random.randint(0, len(self.top_images)-1)
		rand_bottom_index = random.randint(0, len(self.bottom_images)-1)

		#add clothes
		self.update_image(self.top_images[rand_top_index], self.top_image_label)
		self.update_image(self.bottom_images[rand_bottom_index], self.bottom_image_label)

root = tk.Tk()
app = WardrobeApp(root)
root.mainloop()
