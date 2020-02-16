from PIL import Image
import scipy.spatial as sp
import os

# Settings
def set_settings():
	# Saturation Levels
	saturation_thresholds = {
	  "lvl_one": 1/6.0,
	      "lvl_two": 2/6.0,
	      "lvl_three": 3/6.0,
	      "lvl_four": 4.4/6.0,
	      "lvl_five": 6/6.0
	}
	#Dice colors. Enter as many dice colors as you want in RGB format and in an array.
	dice_colors = [(0,0,0)]
	#Border color. Adds a border around the dice. Use an empty string '' to hide border. Otherwise type use something like (0,0,0).
	border_color = ''
	return {'saturation_thresholds': saturation_thresholds, 'dice_colors': dice_colors, 'border_color': border_color}

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

# Create a Primary Colors version of the image
def convert_dice_with_border(image, saturation_thresholds, border_color, main_colors = [(255,255,255)]):
	if border_color != '':
	 square_width = 9
	 adjust = 0
	 border = True
	else:
	 square_width = 7
	 adjust = -1
	 border = False
	# Get size
	width, height = image.size

	# Create new Image and a Pixel Map
	new = Image.new("RGB", (width*square_width, height*square_width), "black")
	pixels = new.load()

	# Max Saturation
	i = 0
	j = 0
	maxSaturation = 0

	while j < height:
		while i < width:
			pixel = image.getpixel((i, j))
			if  (pixel[0]) + (pixel[1]) + (pixel[2]) > maxSaturation:
				maxSaturation = (pixel[0]) + (pixel[1]) + (pixel[2])
			i+=1
		i=0
		j+=1

	# Transform to dice
 	i = 0
 	j = 0
	while j < height:
	 while i < width:
	  # Get saturation
	  pixel = image.getpixel((i, j))
	  saturation = (pixel[0]) + (pixel[1]) + (pixel[2])
	  # Calculate nearest coolor
	  input_color = (pixel[0],pixel[1],pixel[2])
	  tree = sp.KDTree(main_colors)
	  ditsance, result = tree.query(input_color)
	  nearest_color = main_colors[result]
	  # Color Background of dice with nearest coolor
	  for k in range(square_width):
	   for l in range(square_width):
	    pixels[(i*square_width)+k,(j*square_width)+l] = nearest_color
	  # Set Border Color
	  if border:
	   for k in range(square_width):
	    for l in range(square_width):
		 if ((i*square_width)+k)%square_width ==0 or ((j*square_width)+l)%square_width ==0 or ((i*square_width)+k)%square_width ==8 or ((j*square_width)+l)%square_width ==8:
		  pixels[(i*square_width)+k,(j*square_width)+l] = border_color

	  #Use saturation thresholds to determine what dice to use
	  lvl_one = saturation_thresholds['lvl_one']
	  lvl_two = saturation_thresholds['lvl_two']
	  lvl_three = saturation_thresholds['lvl_three']
	  lvl_four = saturation_thresholds['lvl_four']
	  lvl_five = saturation_thresholds['lvl_five']
	  #If color is not white use white dots else use black
	  if nearest_color != (255,255,255):
		if saturation < maxSaturation*lvl_one:
		   pixels[(i*square_width+adjust)+4, (j*square_width+adjust)+4] = (255,255,255)
		elif saturation < maxSaturation*lvl_two:
		   pixels[(i*square_width+adjust)+2, (j*square_width+adjust)+3] = (255,255,255)
		   pixels[(i*square_width+adjust)+6, (j*square_width+adjust)+5] = (255,255,255)
		elif saturation < maxSaturation*lvl_three:
		   pixels[(i*square_width+adjust)+2, (j*square_width+adjust)+2] = (255,255,255)
		   pixels[(i*square_width+adjust)+4, (j*square_width+adjust)+4] = (255,255,255)
		   pixels[(i*square_width+adjust)+6, (j*square_width+adjust)+6] = (255,255,255)
		elif saturation < maxSaturation*lvl_four:
		   pixels[(i*square_width+adjust)+3, (j*square_width+adjust)+3] = (255,255,255)
		   pixels[(i*square_width+adjust)+3, (j*square_width+adjust)+5] = (255,255,255)
		   pixels[(i*square_width+adjust)+5, (j*square_width+adjust)+3] = (255,255,255)
		   pixels[(i*square_width+adjust)+5, (j*square_width+adjust)+5] = (255,255,255)
		elif saturation <= maxSaturation*lvl_five:
		   pixels[(i*square_width+adjust)+2, (j*square_width+adjust)+2] = (255,255,255)
		   pixels[(i*square_width+adjust)+6, (j*square_width+adjust)+2] = (255,255,255)
		   pixels[(i*square_width+adjust)+4, (j*square_width+adjust)+4] = (255,255,255)
		   pixels[(i*square_width+adjust)+2, (j*square_width+adjust)+6] = (255,255,255)
		   pixels[(i*square_width+adjust)+6, (j*square_width+adjust)+6] = (255,255,255)
		else:
		   print('saturation')
		   print(saturation)
		   print(maxSaturation)
		   pixels[(i*square_width+adjust)+3, (j*square_width+adjust)+2] = (255,255,255)
		   pixels[(i*square_width+adjust)+5, (j*square_width+adjust)+2] = (255,255,255)
		   pixels[(i*square_width+adjust)+3, (j*square_width+adjust)+4] = (255,255,255)
		   pixels[(i*square_width+adjust)+5, (j*square_width+adjust)+4] = (255,255,255)
		   pixels[(i*square_width+adjust)+3, (j*square_width+adjust)+6] = (255,255,255)
		   pixels[(i*square_width+adjust)+5, (j*square_width+adjust)+6] = (255,255,255)
	  else:
		if saturation < maxSaturation*lvl_one:
		   pixels[(i*square_width+adjust)+3, (j*square_width+adjust)+2] = (0,0,0)
		   pixels[(i*square_width+adjust)+5, (j*square_width+adjust)+2] = (0,0,0)
		   pixels[(i*square_width+adjust)+3, (j*square_width+adjust)+4] = (0,0,0)
		   pixels[(i*square_width+adjust)+5, (j*square_width+adjust)+4] = (0,0,0)
		   pixels[(i*square_width+adjust)+3, (j*square_width+adjust)+6] = (0,0,0)
		   pixels[(i*square_width+adjust)+5, (j*square_width+adjust)+6] = (0,0,0)
		elif saturation < maxSaturation*lvl_two:
		   pixels[(i*square_width+adjust)+2, (j*square_width+adjust)+2] = (0,0,0)
		   pixels[(i*square_width+adjust)+6, (j*square_width+adjust)+2] = (0,0,0)
		   pixels[(i*square_width+adjust)+4, (j*square_width+adjust)+4] = (0,0,0)
		   pixels[(i*square_width+adjust)+2, (j*square_width+adjust)+6] = (0,0,0)
		   pixels[(i*square_width+adjust)+6, (j*square_width+adjust)+6] = (0,0,0)
		elif saturation < maxSaturation*lvl_three:
		   pixels[(i*square_width+adjust)+3, (j*square_width+adjust)+3] = (0,0,0)
		   pixels[(i*square_width+adjust)+3, (j*square_width+adjust)+5] = (0,0,0)
		   pixels[(i*square_width+adjust)+5, (j*square_width+adjust)+3] = (0,0,0)
		   pixels[(i*square_width+adjust)+5, (j*square_width+adjust)+5] = (0,0,0)
		elif saturation < maxSaturation*lvl_four:
		   pixels[(i*square_width+adjust)+2, (j*square_width+adjust)+2] = (0,0,0)
		   pixels[(i*square_width+adjust)+4, (j*square_width+adjust)+4] = (0,0,0)
		   pixels[(i*square_width+adjust)+6, (j*square_width+adjust)+6] = (0,0,0)
		elif saturation <= maxSaturation*lvl_five:
		   pixels[(i*square_width+adjust)+2, (j*square_width+adjust)+3] = (0,0,0)
		   pixels[(i*square_width+adjust)+6, (j*square_width+adjust)+5] = (0,0,0)
		else:
		   pixels[(i*square_width+adjust)+4, (j*square_width+adjust)+4] = (0,0,0)
	  i+=1
	 i=0
	 j+=1
    # return new image
	return new

def main():
	cwd = os.getcwd()

	if "/" in cwd:
		delimiter = "/"
	elif "\\" in cwd:
		delimiter = "\\"
	image_path = cwd + delimiter + 'original_image'
	input_path = ''
	for file in os.listdir(image_path):
	 if file.endswith(".png"):
	  input_path = os.path.join(image_path, file)
	  break
	if input_path == '':
	 print('No Image found with .png extension in original_image directory')
	 return

	# Load Image (JPEG/JPG needs libjpeg to load)
	print(input_path.strip())
	original = Image.open(input_path)

	suffix = ".png"
	# Resize image to the amount of dice being used
	dice = input("Please enter the amount of dice you would like to use: ")
	#Resize Image
	resized_image = resize(original, dice)
	# SETTINGS
	settings = set_settings()
	# Saturation Levels
	saturation_thresholds = settings['saturation_thresholds']
	#Dice colors. Enter as many dice colors as you want in RGB format.
	dice_colors = settings['dice_colors']
	#Border color. Adds a border around the dice.
	border_color = settings['border_color']
	################################
	# Convert to dice and save
	new = convert_dice_with_border(resized_image, saturation_thresholds, border_color, dice_colors)
	path = cwd + delimiter + 'dice_image' + delimiter
	if not os.path.exists(path):
	 os.makedirs(path)
	new.save(path + 'dice' + suffix)
	new.show()
if __name__ == "__main__":
	main()
