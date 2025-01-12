# CarVisionAI: System for Autonomous Vehicles

## Overview
The system processes video input through multiple stages, from camera calibration to final lane visualization, providing real-time information about lane boundaries, curvature, and vehicle position.

## Dependencies
* Python 3.5
* NumPy
* OpenCV-Python
* Matplotlib
* Pickle

## Pipeline Architecture
The lane detection pipeline consists of the following key stages:

### 1. Camera Calibration
- Uses chessboard images for camera calibration
- Converts images to grayscale
- Detects chessboard corners (9x6 board)
- Calculates distortion matrices using OpenCV's `calibrateCamera()`
- Stores calibration data in 'calibrate_camera.p'

### 2. Image Processing
- Distortion correction using calibration matrices
- Creation of thresholded binary image through:
  - Horizontal Sobel operator
  - Magnitude of Sobel operator (both directions)
  - Gradient direction calculation
  - HLS color space transformation with S-channel thresholding
  - Binary image combination

### 3. Perspective Transform
- Implements bird's-eye view transformation
- Uses OpenCV's `getPerspectiveTransform()` and `warpPerspective()`
- Manual determination of source and destination points

### 4. Lane Detection
- Histogram analysis of bottom half of image
- Image partitioning into 9 horizontal slices
- Sliding window approach for lane pixel detection
- 2nd order polynomial fitting for lane boundaries
- Temporal correlation exploitation:
  - Quick search within ±100 pixels of previous detection
  - Moving average smoothing of polynomial coefficients (5 frames)

### 5. Measurements and Visualization
- Calculates radius of curvature
  - Converts measurements from pixels to meters (30m/720px vertical, 3.7m/700px horizontal)
- Determines vehicle offset from lane center
- Provides visual overlay of detected lanes
- Displays numerical data for curvature and position


## Installation and Usage
1. Clone the repository:
```bash
git clone https://github.com/apo-orvv/CarVisionAI.git
cd CarVisionAI
```

2. Install dependencies

3. Run the main script:
```bash
python line_fit.py
```

## Project Structure
```
CarVisionAI/
│
├── camera_cal/          # Camera calibration images
├── test_images/         # Test image data
├── line_fit.py         # Main lane detection script
├── Line.py             # Lane line class definition
└── calibrate_camera.p  # Calibration data
```

## Limitations and Future Work
- Algorithm performance in extreme weather conditions
- Need for algorithmic determination of perspective transform points
- Optimization for various road types

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
