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
		if pixel == None:
			continue
		saturation += pixel[2]
		saturation = saturation/49 # calculate average
	  for k in range(7):
	   for l in range(7):
	    pixels[i+l, j+k] = (0,0,0)
	  # draw die
	  if saturation < 1:
	    pixels[i+3, j+3] = (255,255,255)
	  elif saturation < 2:
	   pixels[i+1, j+2] = (255,255,255)
	   pixels[i+5, j+4] = (255,255,255)
	  elif saturation < 3:
	   pixels[i+1, j+1] = (255,255,255)
	   pixels[i+3, j+3] = (255,255,255)
	   pixels[i+5, j+5] = (255,255,255)
	  elif saturation < 4:
	   pixels[i+2, j+2] = (255,255,255)
	   pixels[i+2, j+4] = (255,255,255)
	   pixels[i+4, j+2] = (255,255,255)
	   pixels[i+4, j+4] = (255,255,255)
	  elif saturation < 5:
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
		width, height = gray.size
		dice_amount = 1000
		width_dice_amount = 140
		height_dice_amount = 150
		print('width_dice_amount:{0}'.format(width_dice_amount))
		print('height_dice_amount:{0}'.format(height_dice_amount))
		new_image = gray.resize((width_dice_amount*7, height_dice_amount*7))
		new_image.save

		# Convert to dice and save
		new = convert_dice(new_image)
		new.save(path + 'dice' + suffix)

if __name__ == "__main__":
	main()
