import argparse
import ShotBoundaryDetection
import InterviewDetection
import InterviewSelection

def parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", type=str, help="input file name without extension", required=True)
	parser.add_argument("-s", type=int, help="time length [sec] (default: 5)", required=False)

	return parser.parse_args()

if __name__=="__main__":
	args = parser()

	if args.i != None:
		sec = 3
		if args.s != None:
			sec = args.s

		ShotBoundaryDetection.ShotBoundaryDetection(args.i)
		InterviewDetection.InterviewDetection(args.i)
		InterviewSelection.InterviewSelection(args.i, sec)

