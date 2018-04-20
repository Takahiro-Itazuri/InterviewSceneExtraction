import os
import cv2
import glob
import argparse
import shutil

def parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", type=str, help="input file name without extension", required=True)
	parser.add_argument("-s", type=int, help="time length [sec] (default: 5)", required=False)

	return parser.parse_args()

def InterviewSelection(ifilename, sec):
	if not os.path.exists("../output/" + ifilename + "/result/"):
		print(args.i + " directory does not have result directory")
	else:
		input_path = "../output/" + ifilename + "/result/"
		output_path = "../output/" + ifilename + "/{}/".format(sec)

		if not os.path.exists(output_path):
			os.makedirs(output_path)

		fnames = sorted(glob.glob(input_path + "*.avi"))
		file_idx = 0

		for fname in fnames:
			print(fname + " --------------")
			cap = cv2.VideoCapture(fname)
			count = 0
			
			while(cap.isOpened()):
				ret, frame = cap.read()
				if ret == False:
					break
				count += 1

			if count > sec * 30:
				shutil.copy(fname, output_path + "{0:04d}.avi".format(file_idx))
				file_idx += 1

			cap.release()

if __name__=="__main__":
	args = parser()

	if args.i != None:
		sec = 3
		if args.s != None:
			sec = args.s
		InterviewSelection(args.i, sec)
