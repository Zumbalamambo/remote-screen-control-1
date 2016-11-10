import pyscreenshot as img_grab
import io
from PIL import Image
import cv2
import numpy as np

class ScreenFeed:
	def __init__(self, name):
		self.name = name

	def get_frame(self):
		img = img_grab.grab()
		img_arr = np.array(img)
		cv_img = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)
		pil_img = Image.fromarray(cv_img)
		b = io.BytesIO()
		pil_img.save(b, 'jpeg')
		img_bytes = b.getvalue()
		return img_bytes

	def set_frame(self, frame_bytes):
		img_bytes = io.BytesIO(frame_bytes)
		pil_img = Image.open(img_bytes)
		cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_GRAY2RGB)
		cv2.imshow(self.name, cv_img)
		cv2.waitKey(1000)


if __name__ == "__main__":
	frame = ScreenFeed('Teamviewer')
	frame_bytes = frame.get_frame()
	frame.set_frame(frame_bytes)
