# create_dice_placeholders.py
from PIL import Image, ImageDraw, ImageFont
import os

def create_dice_placeholder(dice_type):
    """Create a placeholder image for a dice type"""
    # Create a blank image with a white background
    img = Image.new('RGB', (200, 200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # Draw a circle
    d.ellipse([20, 20, 180, 180], outline=(0, 0, 0), width=3)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = f"d{dice_type}"
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    d.text(((200 - text_width) / 2, (200 - text_height) / 2), text, font=font, fill=(0, 0, 0))
    
    # Save the image
    os.makedirs("assets/images", exist_ok=True)
    img.save(f"assets/images/d{dice_type}.png")

# Create placeholders for all standard dice
for dice_type in [4, 6, 8, 10, 12, 20, 100]:
    create_dice_placeholder(dice_type)

print("Placeholder dice images created in assets/images/")