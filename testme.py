from PIL import Image
import numpy as np
import logging, os

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s', force=True)

def find_image_differences(image_path1, image_path2):

	# put a try except block to catch the error
	# and print the error message
    try:
        # Load the images
        image1 = Image.open(image_path1)
        image2 = Image.open(image_path2)
    
        # Convert images to numpy arrays
        image1_array = np.array(image1)
        image2_array = np.array(image2)
        
        # Check if images have the same dimensions
        if image1_array.shape != image2_array.shape:
            return "Images have different shapes and cannot be compared."
        
        # Calculate the absolute difference between the images
        difference = np.abs(image1_array - image2_array)
        
        # Identify where the difference is significant (e.g., above a threshold)
        significant_diff = difference > 30  # Adjust threshold as needed
        
        # If needed, return the difference or a summary
        if np.any(significant_diff):
            print("Differences found.")
            # Optionally, save or display the difference image
            # diff_image = Image.fromarray(difference)
            # diff_image.show()
        else:
            print("No significant differences found.")
    except Exception as e:
        logging.exception(f"Exception: {e}")
        return


main_folder = '/Users/myuser/Documents/fstau/aug23/'
image1 =  os.path.join(main_folder,'1996.jpg')
image2 = os.path.join(main_folder,'1997.jpg')
out_folder = os.path.join(main_folder,'output')

from PIL import Image
import numpy as np
import os
import cv2


def create_intermediate_images(image_path1, image_path2, num_intermediates=5, out_folder='.'):
	# do nothing for now
	print(f"doing nothing ...")
	logging.info(f"paths {image_path1} and {image_path2}")
	return
	
	# Load the images
	img1 = Image.open(image_path1).convert('RGBA')
	img2 = Image.open(image_path2).convert('RGBA')

	# Resize the smaller image to match the size of the larger image
	if img1.size != img2.size:
		if img1.size[0] * img1.size[1] < img2.size[0] * img2.size[1]:
			img1 = img1.resize(img2.size, Image.LANCZOS)
		else:
			img2 = img2.resize(img1.size, Image.LANCZOS)

	# Convert images to numpy arrays
	img1_array = np.array(img1)
	img2_array = np.array(img2)

	# Ensure the output folder exists
	if not os.path.exists(out_folder):
		os.makedirs(out_folder)

	# Generate intermediate images
	for i in range(1, num_intermediates + 1):
		alpha = i / (num_intermediates + 1)
		intermediate_array = (1 - alpha) * img1_array + alpha * img2_array

		# Move the dots to the new position
		intermediate_array = move_dots(intermediate_array)

		intermediate_image = Image.fromarray(np.uint8(intermediate_array))

		# Save or display the intermediate image
		output_path = os.path.join(out_folder, f'intermediate_{i}.png')
		intermediate_image.save(output_path)
		print(f'Saved: {output_path}')

def move_dots(image_array):
	# Find the coordinates of the dots in the image
	dot_coordinates = np.where(np.all(image_array == [255, 0, 0, 255], axis=-1))

	# Calculate the new coordinates for the dots
	new_dot_coordinates = (dot_coordinates[0] + np.random.randint(-10, 10, size=dot_coordinates[0].shape),
						   dot_coordinates[1] + np.random.randint(-10, 10, size=dot_coordinates[1].shape))

	# Ensure new coordinates are within bounds
	new_dot_coordinates = (np.clip(new_dot_coordinates[0], 0, image_array.shape[0] - 1),
						   np.clip(new_dot_coordinates[1], 0, image_array.shape[1] - 1))

	# Update the image array with the new dot positions
	image_array[dot_coordinates] = [0, 0, 0, 0]
	image_array[new_dot_coordinates] = [255, 0, 0, 255]

	return image_array

def create_movie(image_folder, output_path, fps=30):
	# Get the list of image files in the folder
	image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])

	# Read the first image to get the size
	first_image = cv2.imread(os.path.join(image_folder, image_files[0]))
	height, width, _ = first_image.shape

	# Create a VideoWriter object
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

	# Write each image to the video file
	for image_file in image_files:
		image_path = os.path.join(image_folder, image_file)
		image = cv2.imread(image_path)
		video_writer.write(image)

	# Release the VideoWriter object
	video_writer.release()

# create intermediate images using image1 and image2 and save them in the out_folder
# create_intermediate_images(image1, image2, num_intermediates=5, out_folder=out_folder)

# create a 10-second movie from the intermediate images
# create_movie(out_folder, 'output.mp4', fps=30)

from astropy.io import fits
import os
import cv2

def show_fits_info(fits_file_path):
    # Open the FITS file
    with fits.open(fits_file_path) as hdul:
        # Display the structure of the FITS file
        hdul.info()
        
        # Access the primary HDU (Header/Data Unit)
        primary_hdu = hdul[0]
        
        # Print the header of the primary HDU
        print("\nPrimary HDU Header:")
        print(repr(primary_hdu.header))
        
        # If there are additional HDUs, print their headers
        for i in range(1, len(hdul)):
            print(f"\nHDU {i} Header:")
            print(repr(hdul[i].header))

# Example usage
# show_fits_info('/Users/myuser/Documents/fits/jw01373014001_03101_00001_nrcb4_rate.fits')
