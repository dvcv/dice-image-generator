from PIL import Image
import sys

# Create a Grayscale version of the image
def convert_grayscale(image):
	# Get size
	width, height = image.size

	# Create new Image and a Pixel Map
	new = Image.new("RGB", (width, height), "white")
	pixels = new.load()

	# Transform to grayscale
	for i in range(width):
		for j in range(height):
			# Get Pixel
			pixel = image.getpixel((i,j))

			# Get R, G, B values (This are int from 0 to 255)
			red = pixel[0]
			green = pixel[1]
			blue =  pixel[2]

			# Transform to grayscale
			gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

			# Set Pixel in new image
			pixels[i, j] = (int(gray), int(gray), int(gray))

	# Return new image
	return new

# Resize Image
def resize(image, dice = 1000, with_border=False):
	# Get size
	width, height = image.size

	# Given a dice count
	# Calculates the amount of dice to use for the width and height
	width_ratio = width/(width + height + 0.0)
	height_ratio = 1 - width_ratio
	new_width = ((4*height_ratio*width_ratio*dice)**(1/2.0))/(2.0*height_ratio)
	new_height = dice/(new_width + 0.0)

	#round to the nearest dice
	new_width = int(round(new_width))
	new_height = int(round(new_height))

	print('width_dice_amount:{0}'.format(new_width))
	print('height_dice_amount:{0}'.format(new_height))
	print('width_dice_amount*height_dice_amount:{0}'.format(new_width*new_height))

	adjust = 7
	if with_border == True:
	 adjust = 9

	return image.resize((new_width*adjust, new_height*adjust))

def get_pixel(image, i, j):
 	# Inside image bounds?
 	width, height = image.size
 	if i >= width or j >= height:
 		return None

  	# Get Pixel
 	pixel = image.getpixel((i, j))
 	return pixel

# Create a Primary Colors version of the image
def convert_dice(image, saturation_thresholds):

	# Get size
	width, height = image.size
	# Create new Image and a Pixel Map
	new = Image.new("RGB", (width, height), "black")
	pixels = new.load()
	# Transform to dice
 	i = 0
 	j = 0
	while j < height - 0:
	 while i < width - 0:
	  # Get saturation
	  saturation = 0
	  for k in range(7):
	   for l in range(7):
		pixel = get_pixel(image, i+l, j+k)

		saturation += pixel[2]
	  saturation = saturation/49 # calculate average
	  # for k in range(7):
	  #  for l in range(7):
	  #   pixels[i+l, j+k] = (0,0,0)
	  # draw die
	  one_dice_sat = saturation_thresholds['one_dice_sat']
	  two_dice_sat = saturation_thresholds['two_dice_sat']
	  three_dice_sat = saturation_thresholds['three_dice_sat']
	  four_dice_sat = saturation_thresholds['four_dice_sat']
	  five_dice_sat = saturation_thresholds['five_dice_sat']
	  if saturation < one_dice_sat:
	    pixels[i+3, j+3] = (255,255,255)
	  elif saturation < two_dice_sat:
	   pixels[i+1, j+2] = (255,255,255)
	   pixels[i+5, j+4] = (255,255,255)
	  elif saturation < three_dice_sat:
	   pixels[i+1, j+1] = (255,255,255)
	   pixels[i+3, j+3] = (255,255,255)
	   pixels[i+5, j+5] = (255,255,255)
	  elif saturation < four_dice_sat:
	   pixels[i+2, j+2] = (255,255,255)
	   pixels[i+2, j+4] = (255,255,255)
	   pixels[i+4, j+2] = (255,255,255)
	   pixels[i+4, j+4] = (255,255,255)
	  elif saturation < five_dice_sat:
	   pixels[i+1, j+1] = (255,255,255)
	   pixels[i+5, j+1] = (255,255,255)
	   pixels[i+3, j+3] = (255,255,255)
	   pixels[i+1, j+5] = (255,255,255)
	   pixels[i+5, j+5] = (255,255,255)
	  else:
	   pixels[i+2, j+1] = (255,255,255)
	   pixels[i+4, j+1] = (255,255,255)
	   pixels[i+2, j+3] = (255,255,255)
	   pixels[i+4, j+3] = (255,255,255)
	   pixels[i+2, j+5] = (255,255,255)
	   pixels[i+4, j+5] = (255,255,255)
	  i+=7
	 i=0
	 j+=7

    # return new image
	return new

# Create a Primary Colors version of the image
def convert_dice_with_border(image, saturation_thresholds, border_color = (255, 255, 102)):

	# Get size
	width, height = image.size

	# Create new Image and a Pixel Map
	new = Image.new("RGB", (width, height), "black")
	pixels = new.load()
	# Transform to dice
 	i = 0
 	j = 0
	while j < height - 0:
	 while i < width - 0:
	  # Get saturation
	  saturation = 0
	  for k in range(9):
	   for l in range(9):
		if k%9 ==0 or l%9 ==0:
		 pixels[i+k,j+l] = border_color
		pixel = get_pixel(image, i+l, j+k)

		saturation += pixel[2]
	  saturation = saturation/81 # calculate average

	  one_dice_sat = saturation_thresholds['one_dice_sat']
	  two_dice_sat = saturation_thresholds['two_dice_sat']
	  three_dice_sat = saturation_thresholds['three_dice_sat']
	  four_dice_sat = saturation_thresholds['four_dice_sat']
	  five_dice_sat = saturation_thresholds['five_dice_sat']

  	  for k in range(9):
  	   for l in range(9):
		# if k % 9 != 0 and l % 9 != 0:
  	    if k % 9 != 0 or l % 9 != 0:

  	     pixels[i, j] = (0,0,0)


	  if saturation < one_dice_sat:
	    pixels[i+1+3, j+1+3] = (255,255,255)
	  elif saturation < two_dice_sat:
	   pixels[i+1+1, j+1+2] = (255,255,255)
	   pixels[i+1+5, j+1+4] = (255,255,255)
	  elif saturation < three_dice_sat:
	   pixels[i+1+1, j+1+1] = (255,255,255)
	   pixels[i+1+3, j+1+3] = (255,255,255)
	   pixels[i+1+5, j+1+5] = (255,255,255)
	  elif saturation < four_dice_sat:
	   pixels[i+1+2, j+1+2] = (255,255,255)
	   pixels[i+1+2, j+1+4] = (255,255,255)
	   pixels[i+1+4, j+1+2] = (255,255,255)
	   pixels[i+1+4, j+1+4] = (255,255,255)
	  elif saturation < five_dice_sat:
	   pixels[i+1+1, j+1+1] = (255,255,255)
	   pixels[i+1+5, j+1+1] = (255,255,255)
	   pixels[i+1+3, j+1+3] = (255,255,255)
	   pixels[i+1+1, j+1+5] = (255,255,255)
	   pixels[i+1+5, j+1+5] = (255,255,255)
	  else:
	   pixels[i+1+2, j+1+1] = (255,255,255)
	   pixels[i+1+4, j+1+1] = (255,255,255)
	   pixels[i+1+2, j+1+3] = (255,255,255)
	   pixels[i+1+4, j+1+3] = (255,255,255)
	   pixels[i+1+2, j+1+5] = (255,255,255)
	   pixels[i+1+4, j+1+5] = (255,255,255)
	  i+=9
	 i=0
	 j+=9

    # return new image
	return new

def main():
	# process input
	path = "/Users/dvcv/Documents/code/2dice/djs.png"

	try:
		# Load Image (JPEG/JPG needs libjpeg to load)
		original = Image.open(path)

	except FileNotFoundError:
		print(path)
		print("File not found. Please make sure your path and file name are correct and try again.")

	else:
		suffix = "." + 'png'

		# Convert to Grayscale and save
		new = convert_grayscale(original)
		new.save(path + 'gray' + suffix)

		# Load gray image
		gray = Image.open('/Users/dvcv/Documents/code/2dice/djs.pnggray.png')

		# Resize Image based on dice amount
		dice = 5000
		saturation_thresholds = {
		  "one_dice_sat": 15,
   	      "two_dice_sat": 55,
   	      "three_dice_sat": 85,
   	      "four_dice_sat": 100,
   	      "five_dice_sat": 115
		}

		# Convert to dice and save

		# border_color = (255, 255, 102)
		resized_image = resize(gray, dice)
		new = convert_dice(resized_image, saturation_thresholds)
		new.save(path + 'dice' + suffix)

		resized_image = resize(gray, dice, True)
		new = convert_dice_with_border(resized_image, saturation_thresholds)
		new.save(path + 'dice_with_' + suffix)

if __name__ == "__main__":
	main()
