# Interview Scene Extraction
## Packages
|Name|Version|
|:--|:--|
|python|3.5.5|
|opencv-contrib-python|3.4..0.12|

## Code
### main.py
This file executes "ShotBoundaryDetection.py", "InterviewDetection.py", and "InterviewSelection.py" sequencially.

#### options
|option|content|
|:--|:--|
|i|input file name without extension in the input directory|
|s|time length threshold (sec) (defulat: 5)|

### ShotBoundaryDetection.py
This code implements shot boundary detection.

#### options
|option|content|
|:--|:--|
|i|input file name without extension in the input directory|
|u|upper threshold of hue & saturation histogram difference between consecutive frames for cut detection (default: 0.5)|
|l|lower threshold of hue & saturation histogram difference between consecutive frames for cut detection (default: 0.1)|

### InterviewDetection.py
This code detects interview shot (over 3 seconds).

#### options
|option|content|
|:--|:--|
|i|input file name without extension in the input directory|

### InterviewSelection.py
This code selects interview shots detected in "InterviewDetection.py" over given time length.

#### options
|option|content|
|:--|:--|
|i|input file name without extension in the input directory|
|s|time length (sec) (default: 0.5)|
