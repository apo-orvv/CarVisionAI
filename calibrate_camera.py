import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle


def calibrate_camera():
	# Mapping each calibration image to number of checkerboard corners
	objp_dict = {
		1: (9, 5),
		2: (9, 6),
		3: (9, 6),
		4: (9, 6),
		5: (9, 6),
		6: (9, 6),
		7: (9, 6),
		8: (9, 6),
		9: (9, 6),
		10: (9, 6),
		11: (9, 6),
		12: (9, 6),
		13: (9, 6),
		14: (9, 6),
		15: (9, 6),
		16: (9, 6),
		17: (9, 6),
		18: (9, 6),
		19: (9, 6),
		20: (9, 6),
	}

	# List of object points and corners for calibration
	objp_list = []
	corners_list = []

	# Parsing all images and finding corners
	for k in objp_dict:
		nx, ny = objp_dict[k]

		# Prepare object points, (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
		objp = np.zeros((nx*ny,3), np.float32)
		objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)

		# List of calibration images
		fname = 'camera_cal/calibration%s.jpg' % str(k)
		img = cv2.imread(fname)

		# Grayscale Conversion
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# Chessboard Corners Recognition
		ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

		# If found, save & draw corners
		if ret == True:
			objp_list.append(objp)
			corners_list.append(corners)

			# Draw and display the corners
			#cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
			#plt.imshow(img)
			#plt.show()
			#print('Found corners for %s' % fname)
		else:
			continue
			# print('Warning: ret = %s for %s' % (ret, fname))

	# Calibrate camera and undistort a test image
	img = cv2.imread('test_images/straight_lines1.jpg')
	img_size = (img.shape[1], img.shape[0])
	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objp_list, corners_list, img_size,None,None)

	return mtx, dist


if __name__ == '__main__':
	mtx, dist = calibrate_camera()
	save_dict = {'mtx': mtx, 'dist': dist}
	with open('calibrate_camera.p', 'wb') as f:
		pickle.dump(save_dict, f)

	for i in range(1, 21):
		img_path = 'camera_cal/calibration{}.jpg'.format(i)
		img = mpimg.imread(img_path)
		
		# Undistort the image using the calibration matrices
		dst = cv2.undistort(img, mtx, dist, None, mtx)
		save_path = 'calib_test/distortfree{}.png'.format(i)
		plt.imshow(dst)
		plt.savefig(save_path)
