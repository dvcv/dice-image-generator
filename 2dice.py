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

	print('The number of dice to use for the width:{0}'.format(new_width))
	print('The number of dice to use for the height:{0}'.format(new_height))
	print('Total:{0}'.format(new_width*new_height))

	return image.resize((new_width, new_height))

def get_pixel(image, i, j):
 	# Inside image bounds?
 	width, height = image.size
 	if i >= width or j >= height:
 		return None

  	# Get Pixel
 	pixel = image.getpixel((i, j))
 	return pixel

# Create a Primary Colors version of the image
def convert_dice_with_border(image, saturation_thresholds, border_color = (255, 255, 102)):
	# Get size
	width, height = image.size

	# Create new Image and a Pixel Map
	new = Image.new("RGB", (width*9, height*9), "black")
	pixels = new.load()

	# Max Saturation
	i = 0
	j = 0
	maxSaturation = 0
	count = 0

	while i < height:
		while j < width:
			pixel = image.getpixel((i,j))
			if pixel[2] > maxSaturation:
				maxSaturation = pixel[2]
			count += 1
			j+=1
		i+=1

	# Transform to dice
 	i = 0
 	j = 0
	while j < height:
	 while i < width:
	  # Get saturation
	  pixel = get_pixel(image, i, j)
	  saturation = pixel[2]
	  # Set Border Color
	  for k in range(9):
	   for l in range(9):
		if ((i*9)+k)%9 ==0 or ((j*9)+l)%9 ==0 or ((i*9)+k)%9 ==8 or ((j*9)+l)%9 ==8:
		 pixels[(i*9)+k,(j*9)+l] = border_color

	  #Use saturation thresholds to determine what dice to use
	  one_dice_sat = saturation_thresholds['one_dice_sat']
	  two_dice_sat = saturation_thresholds['two_dice_sat']
	  three_dice_sat = saturation_thresholds['three_dice_sat']
	  four_dice_sat = saturation_thresholds['four_dice_sat']
	  five_dice_sat = saturation_thresholds['five_dice_sat']

	  if saturation < maxSaturation*one_dice_sat:
	    pixels[(i*9)+4, (j*9)+4] = (255,255,255)
	  elif saturation < maxSaturation*two_dice_sat:
	   pixels[(i*9)+2, (j*9)+3] = (255,255,255)
	   pixels[(i*9)+6, (j*9)+5] = (255,255,255)
	  elif saturation < maxSaturation*three_dice_sat:
	   pixels[(i*9)+2, (j*9)+2] = (255,255,255)
	   pixels[(i*9)+4, (j*9)+4] = (255,255,255)
	   pixels[(i*9)+6, (j*9)+6] = (255,255,255)
	  elif saturation < maxSaturation*four_dice_sat:
	   pixels[(i*9)+3, (j*9)+3] = (255,255,255)
	   pixels[(i*9)+3, (j*9)+5] = (255,255,255)
	   pixels[(i*9)+5, (j*9)+3] = (255,255,255)
	   pixels[(i*9)+5, (j*9)+5] = (255,255,255)
	  elif saturation <= maxSaturation*five_dice_sat:
	   pixels[(i*9)+2, (j*9)+2] = (255,255,255)
	   pixels[(i*9)+6, (j*9)+2] = (255,255,255)
	   pixels[(i*9)+4, (j*9)+4] = (255,255,255)
	   pixels[(i*9)+2, (j*9)+6] = (255,255,255)
	   pixels[(i*9)+6, (j*9)+6] = (255,255,255)
	  else:
	   pixels[(i*9)+3, (j*9)+2] = (255,255,255)
	   pixels[(i*9)+5, (j*9)+2] = (255,255,255)
	   pixels[(i*9)+3, (j*9)+4] = (255,255,255)
	   pixels[(i*9)+5, (j*9)+4] = (255,255,255)
	   pixels[(i*9)+3, (j*9)+6] = (255,255,255)
	   pixels[(i*9)+5, (j*9)+6] = (255,255,255)
	  i+=1
	 i=0
	 j+=1
    # return new image
	return new

def main():
	# Entere file path here.
	input_path = '/Users/dvcv/Documents/code/2dice/dice-image.png'
	if "/" in input_path:
		delimiter = "/"
	elif "\\" in input_path:
		delimiter = "\\"

	input_path = input_path.split(delimiter)
	file = input_path[-1]
	path = ""

	if len(input_path) != 1:
		path = delimiter

	for i in range(len(input_path)-1):
		path += input_path[i] + delimiter

	try:
		# Load Image (JPEG/JPG needs libjpeg to load)
		original = Image.open(path + file)

	except EnvironmentError as e:
		print(path + file)
		print("File not found. Please make sure your path and file name are correct and try again.")

	else:
		suffix = "." + file.split(".")[-1]
		# Resize image to the amount of dice being used
		dice = input("Please enter the amount of dice you would like to use: ")
		resized_image = resize(original, dice)
		# Convert to Grayscale and save
		new = convert_grayscale(resized_image)
		new.save(path + 'gray' + suffix)
		# Load gray image
		gray = Image.open(path + 'gray' + suffix)
		# Saturation Levels
		saturation_thresholds = {
		  "one_dice_sat": 1/6.0,
   	      "two_dice_sat": 2/6.0,
   	      "three_dice_sat": 3/6.0,
   	      "four_dice_sat": 4/6.0,
   	      "five_dice_sat": 6/6.0
		}
		# Convert to dice and save
		new = convert_dice_with_border(gray, saturation_thresholds, (0,0,0))
		new.save(path + 'dice' + suffix)
		# Convert to dice and with border
		new = convert_dice_with_border(gray, saturation_thresholds, (50,50,50))
		new.save(path + 'dice_with_border' + suffix)

if __name__ == "__main__":
	main()
