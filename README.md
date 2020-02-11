# Requirements
Python 2.7  

# Install  
PIL  
scipy   

## Directios
1. Place file in original image directory.  
2. Run by typing `python 2dice_color.py`  
3. Type in the amount of dice you would like to use.

## Settings
Change these setting in set_settings() method in 2dice_color.py file to your liking.  
### Saturation Levels
This decides when to use a single dot side of a dice vs two, three, ect.  
saturation_thresholds = {  
  "lvl_one": 1/6.0,  
      "lvl_two": 2/6.0,  
      "lvl_three": 3/6.0,  
      "lvl_four": 4/6.0,  
      "lvl_five": 5/6.0  
}  
### Dice colors. Enter as many dice colors as you want in RGB format.  
dice_colors = [(255,255,255)]  
### Border color. Adds a border around the dice.  
border_color = (255,255,255)  

## Description
Convert a png image into one made of dice. Script auto adjust the image to the number of dice entered.
## Examples
<image style='width: 100px' src='https://raw.githubusercontent.com/dvcv/dice-image-generator/master/examples/multi-color-dice.png'/>
