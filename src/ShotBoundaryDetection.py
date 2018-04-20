import os
import cv2
import argparse
import numpy as np
import glob

def parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", type=str, help="input file name in the input directory", required=True)
	parser.add_argument("-u", type=float, help="upper threshold of hs histogram difference between consecutive frames for cut detection (default: 0.5)", required=False)
	parser.add_argument("-l", type=float, help="lower threshold of hs histogram difference between consecutive frames for cut detection (defulat: 0.1)", required=False)

	return parser.parse_args()

def ShotBoundaryDetection(ifilename, lower_thr=0.1, upper_thr=0.5):
	paths = glob.glob("../input/" + ifilename + ".*")
	
	# set up
	if not os.path.exists(paths[0]):
		print(ifilename + " does not exist in the input directory.")
	else:
		input_path = paths[0]
		output_path = "../output/" + ifilename + "/shot/"

		if not os.path.exists(output_path):
			os.makedirs(output_path)

		print("input : " + input_path)
		print("output: " + output_path)

		# initialization
		cap = cv2.VideoCapture(input_path)
		w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		fps = cap.get(cv2.CAP_PROP_FPS)
		num_pixels = w * h

		flag = False
		pre_hist = np.zeros((180, 256))
		shot_idx = 0
		frame_idx = 0
		
		fourcc = cv2.VideoWriter_fourcc(*"XVID")
		writer = cv2.VideoWriter(output_path + "{0:04d}.avi".format(shot_idx), fourcc, fps, (w, h))

		while(cap.isOpened()):
			if frame_idx % 100 == 0:
				print("frame #{}".format(frame_idx))
			
			ret, frame = cap.read()
			if ret == False:
				break

			# convert image from RGB to HSV
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
			# calculate histogram of HSV
			hist = cv2.calcHist([hsv], [0, 1], None, [64, 64], [0, 256, 0, 256])

			if frame_idx != 0:
				diff = np.sum(np.abs(pre_hist - hist)) / num_pixels
				if flag and diff > upper_thr:
					flag = False
					shot_idx += 1;
					writer.release()
					writer = cv2.VideoWriter(output_path + "{0:04d}.avi".format(shot_idx), fourcc, fps, (w, h))
				elif (not flag) and diff < lower_thr:
					flag = True

			writer.write(frame)

			# update
			frame_idx += 1
			pre_hist = hist

		writer.release()
		cap.release()

if __name__=="__main__":
	# parse command line arguments
	args = parser()
	if args.i != None:
		if (args.l != None) and (args.u != None):
			ShotBoundaryDetection(args.i, args.l, args.u)
		else:
			ShotBoundaryDetection(args.i)
