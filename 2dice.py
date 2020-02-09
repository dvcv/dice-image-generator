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
def resize(image, dice = 1000):
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

	return image.resize((new_width*7, new_height*7))

def get_pixel(image, i, j):
 	# Inside image bounds?
 	width, height = image.size
 	if i >= width or j >= height:
 		return None

  	# Get Pixel
 	pixel = image.getpixel((i, j))
 	return pixel

# Create a Primary Colors version of the image
def convert_dice(image):

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
	  if saturation < 15:
	    pixels[i+3, j+3] = (255,255,255)
	  elif saturation < 55:
	   pixels[i+1, j+2] = (255,255,255)
	   pixels[i+5, j+4] = (255,255,255)
	  elif saturation < 85:
	   pixels[i+1, j+1] = (255,255,255)
	   pixels[i+3, j+3] = (255,255,255)
	   pixels[i+5, j+5] = (255,255,255)
	  elif saturation < 100:
	   pixels[i+2, j+2] = (255,255,255)
	   pixels[i+2, j+4] = (255,255,255)
	   pixels[i+4, j+2] = (255,255,255)
	   pixels[i+4, j+4] = (255,255,255)
	  elif saturation < 115:
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
		resized_image = resize(gray, dice)

		# Convert to dice and save
		new = convert_dice(resized_image)
		new.save(path + 'dice' + suffix)

if __name__ == "__main__":
	main()
