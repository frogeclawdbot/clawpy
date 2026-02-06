from PIL import Image, ImageDraw, ImageFont
import random
import math
import json

# Import the lobster drawing code
import sys
sys.path.insert(0, '/home/claude')
from simple_lobster import TRAITS, draw_simple_lobster

# Configuration for showcase grid
cell_size = 700
grid_cols = 5  # 5 columns
grid_rows = 5  # 5 rows = 25 total

w = cell_size * grid_cols
h = cell_size * grid_rows

# Get all accessory names
all_accessories = list(TRAITS["Accessory"].keys())
print(f"Total accessories: {len(all_accessories)}")

# Create main image with light gray background
img = Image.new('RGB', (w, h), (240, 240, 240))
draw = ImageDraw.Draw(img)

# Fixed traits for all lobsters (only accessory changes)
base_traits = {
    "Background": "Ocean Blue",
    "Shell Color": "Classic Red",
    "Claw Size": "Medium",
    "Eyes": "Normal",
    "Tail": "Plain",
}

print("Generating accessory showcase grid (5x5)...")

for idx, accessory_name in enumerate(all_accessories):
    col = idx % grid_cols
    row = idx // grid_cols
    
    # Calculate cell position
    cell_x = col * cell_size
    cell_y = row * cell_size
    
    # Get background color
    lobster_bg = TRAITS["Background"][base_traits["Background"]]["color"]
    
    # Draw background rectangle
    draw.rectangle(
        [cell_x + 2, cell_y + 2, cell_x + cell_size - 2, cell_y + cell_size - 2],
        fill=lobster_bg
    )
    
    # Create traits with current accessory
    traits = base_traits.copy()
    traits["Accessory"] = accessory_name
    
    # Calculate lobster center position
    lobster_x = cell_x + cell_size / 2
    lobster_y = cell_y + cell_size / 2 - 50
    
    # Draw the lobster
    draw_simple_lobster(draw, lobster_x, lobster_y, traits, lobster_bg)
    
    # Draw label at bottom
    label_y = cell_y + cell_size - 40
    # Draw label background
    label_bg = [cell_x + 10, label_y - 5, cell_x + cell_size - 10, label_y + 30]
    draw.rectangle(label_bg, fill=(255, 255, 255), outline=(0, 0, 0), width=3)
    
    # Draw text (accessory name)
    text = accessory_name
    # Approximate text centering (rough calculation)
    text_x = cell_x + cell_size / 2 - len(text) * 4
    draw.text((text_x, label_y + 5), text, fill=(0, 0, 0))
    
    print(f"✓ {idx + 1}/25: {accessory_name}")

# Save
output_path = "/mnt/user-data/outputs/lobster_25_accessories_showcase.png"
img.save(output_path)
print(f"\n✅ Accessory showcase saved to: {output_path}")
print(f"Grid size: {grid_cols} x {grid_rows} = {len(all_accessories)} accessories")
