import os
import cv2
import argparse
import numpy as np
import glob
import shutil
import math

def parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", type=str, help="input shot directory name in the input directory", required=True)
		
	return parser.parse_args()

if __name__=="__main__":
	# parse command line arguments
	args = parser()

	# set up
	if not os.path.exists("../output/" + args.i + "/shot/"):
		print(args.i + " directory does not have shot directory.")
	else:
		input_path = "../output/" + args.i + "/shot/"
		output_path = "../output/" + args.i + "/result/"

		if not os.path.exists(output_path):
			os.makedirs(output_path)

		fnames = sorted(glob.glob(input_path + "*.avi"))

		file_idx = 0

		for fname in fnames:
			print(fname + " ----------")
			cap = cv2.VideoCapture(fname)
			w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
			h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
			
			# count the number of frames
			count = 0
			while(cap.isOpened()):
				ret, frame = cap.read()
				if ret == False:
					break
				count += 1
			if count < 30 * 3:
				continue

			# create an average image
			cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
			avg_img = np.zeros((h, w, 3), dtype=np.float32)
			while(cap.isOpened()):
				ret, frame = cap.read()
				if ret == False:
					break

				avg_img += (frame.astype(np.float32) / count)
			avg_img = avg_img.astype(np.uint8)

			# substraction
			cap.set(cv2.CAP_PROP_POS_FRAMES, int(count / 2))
			ret, frame = cap.read()
			check = 0

			diff = np.abs(frame - avg_img)
			for y in range(h):
				for x in range(w):
					norm = math.sqrt(diff[y, x, 0]**2 + diff[y, x, 1]**2 + diff[y, x, 2]**2)
					#print("{}, {}, {}".format(diff[y, x, 0], diff[y, x, 1], diff[y, x, 2]))
					if norm < 5:
						check += 1

			if (float(check) / float(w * h)) > 0.15:
				shutil.copy(fname, output_path + "{0:04d}.avi".format(file_idx))
				file_idx += 1
				print("interview")
			#cv2.imshow(fname, avg_img)
			#cv2.waitKey(0)

			cap.release()
			#cv2.destroyAllWindows()
