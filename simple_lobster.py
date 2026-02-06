from PIL import Image, ImageDraw
import random
import math
import json

# Configuration
w, h = 1400, 1400
line_thickness = 7

# NFT Traits Configuration with Rarity
TRAITS = {
    "Background": {
        "Ocean Blue": {"color": (200, 230, 255), "rarity": 30},
        "Deep Sea": {"color": (150, 180, 210), "rarity": 25},
        "Coral Pink": {"color": (255, 220, 230), "rarity": 20},
        "Sandy Beige": {"color": (245, 235, 215), "rarity": 15},
        "Sunset Orange": {"color": (255, 230, 200), "rarity": 8},
        "Mystic Purple": {"color": (230, 210, 255), "rarity": 2},
    },
    
    "Shell Color": {
        "Classic Red": {"color": (220, 80, 70), "rarity": 25},
        "Orange": {"color": (255, 140, 80), "rarity": 20},
        "Brown": {"color": (160, 100, 70), "rarity": 20},
        "Blue": {"color": (100, 150, 200), "rarity": 15},
        "Green": {"color": (120, 180, 130), "rarity": 10},
        "Golden": {"color": (255, 200, 80), "rarity": 7},
        "Rainbow": {"color": (200, 150, 255), "rarity": 3},
        "Black Pearl": {"color": (40, 40, 50), "rarity": 0.5},
        "White": {"color": (245, 245, 250), "rarity": 0.5},
    },
    
    "Claw Size": {
        "Small": {"size": 0.7, "rarity": 20},
        "Medium": {"size": 1.0, "rarity": 40},
        "Large": {"size": 1.3, "rarity": 25},
        "Mega": {"size": 1.7, "rarity": 10},
        "Gigantic": {"size": 2.2, "rarity": 5},
    },
    
    "Eyes": {
        "Normal": {"style": "normal", "rarity": 40},
        "Googly": {"style": "googly", "rarity": 25},
        "Angry": {"style": "angry", "rarity": 15},
        "Heart Eyes": {"style": "hearts", "rarity": 10},
        "Star Eyes": {"style": "stars", "rarity": 8},
        "Laser Eyes": {"style": "laser", "rarity": 2},
    },
    
    "Tail": {
        "Plain": {"pattern": "plain", "rarity": 40},
        "Striped": {"pattern": "striped", "rarity": 30},
        "Spotted": {"pattern": "spotted", "rarity": 20},
        "Fancy": {"pattern": "fancy", "rarity": 10},
    },
    
    "Accessory": {
        # Head Accessories
        "None": {"type": None, "rarity": 20},
        "Crown": {"type": "crown", "rarity": 5},
        "Chef Hat": {"type": "chef_hat", "rarity": 5},
        "Pirate Hat": {"type": "pirate_hat", "rarity": 4},
        "Top Hat": {"type": "top_hat", "rarity": 4},
        "Wizard Hat": {"type": "wizard_hat", "rarity": 3},
        "Cowboy Hat": {"type": "cowboy_hat", "rarity": 4},
        "Viking Helmet": {"type": "viking_helmet", "rarity": 3},
        "Birthday Hat": {"type": "birthday_hat", "rarity": 3},
        "Halo": {"type": "halo", "rarity": 2},
        # Face Accessories
        "Sunglasses": {"type": "sunglasses", "rarity": 5},
        "3D Glasses": {"type": "3d_glasses", "rarity": 4},
        "Monocle": {"type": "monocle", "rarity": 3},
        "Eye Patch": {"type": "eye_patch", "rarity": 3},
        "Goggles": {"type": "goggles", "rarity": 3},
        # Neck/Body Accessories
        "Bow Tie": {"type": "bow_tie", "rarity": 5},
        "Gold Chain": {"type": "gold_chain", "rarity": 4},
        "Scarf": {"type": "scarf", "rarity": 3},
        "Bandana": {"type": "bandana", "rarity": 3},
        # Antennae
        "Short Antennae": {"type": "antennae_short", "rarity": 5},
        "Long Antennae": {"type": "antennae_long", "rarity": 4},
        "Curly Antennae": {"type": "antennae_curly", "rarity": 3},
        "Rainbow Antennae": {"type": "antennae_rainbow", "rarity": 2},
        # Special/Legendary
        "Angel Wings": {"type": "angel_wings", "rarity": 1},
        "Devil Horns": {"type": "devil_horns", "rarity": 1},
    },
}

def weighted_choice(trait_dict):
    traits = list(trait_dict.keys())
    weights = [trait_dict[t]["rarity"] for t in traits]
    return random.choices(traits, weights=weights)[0]

def generate_traits():
    traits = {}
    for category, options in TRAITS.items():
        traits[category] = weighted_choice(options)
    return traits

def draw_simple_lobster(draw, center_x, center_y, traits, bg_color):
    """Draw a simple, clean lobster"""
    
    shell_color = TRAITS["Shell Color"][traits["Shell Color"]]["color"]
    claw_size = TRAITS["Claw Size"][traits["Claw Size"]]["size"]
    eye_style = TRAITS["Eyes"][traits["Eyes"]]["style"]
    tail_pattern = TRAITS["Tail"][traits["Tail"]]["pattern"]
    accessory = TRAITS["Accessory"][traits["Accessory"]]["type"]
    
    # Darker outline color
    dark_color = (
        int(shell_color[0] * 0.6),
        int(shell_color[1] * 0.6),
        int(shell_color[2] * 0.6)
    )
    
    # Positioning
    x = center_x
    y = center_y
    
    ###########
    # TAIL (simple segmented shape)
    ###########
    tail_width = 100
    tail_height = 180
    num_segments = 4
    
    for i in range(num_segments):
        seg_y = y + i * (tail_height / num_segments)
        seg_width = tail_width - i * 8
        
        # Simple rectangle for each segment
        seg_fill = shell_color
        if tail_pattern == "striped" and i % 2 == 1:
            seg_fill = (min(255, shell_color[0] + 40), 
                       min(255, shell_color[1] + 40), 
                       min(255, shell_color[2] + 40))
        
        draw.rectangle([x - seg_width/2, seg_y, 
                       x + seg_width/2, seg_y + tail_height/num_segments],
                      fill=seg_fill, outline=dark_color, width=line_thickness)
        
        if tail_pattern == "spotted":
            spot_x = x + random.uniform(-20, 20)
            spot_y = seg_y + 15
            draw.ellipse([spot_x - 6, spot_y - 6, spot_x + 6, spot_y + 6],
                        fill=dark_color)
    
    # Tail fan at the end
    fan_y = y + tail_height
    fan_points = [
        (x - 60, fan_y),
        (x - 45, fan_y + 40),
        (x - 20, fan_y + 50),
        (x, fan_y + 55),
        (x + 20, fan_y + 50),
        (x + 45, fan_y + 40),
        (x + 60, fan_y),
    ]
    draw.polygon(fan_points, fill=shell_color, outline=dark_color, width=line_thickness)
    
    ###########
    # BODY (simple oval)
    ###########
    body_width = 120
    body_height = 150
    body_y = y - 80
    
    draw.ellipse([x - body_width/2, body_y, 
                  x + body_width/2, body_y + body_height],
                 fill=shell_color, outline=dark_color, width=line_thickness)
    
    ###########
    # HEAD (smaller circle on top)
    ###########
    head_radius = 50
    head_y = body_y - 20
    
    draw.ellipse([x - head_radius, head_y - head_radius,
                  x + head_radius, head_y + head_radius],
                 fill=shell_color, outline=dark_color, width=line_thickness)
    
    ###########
    # EYES (on stalks)
    ###########
    eye_spacing = 30
    stalk_height = 35
    eye_y = head_y - 10
    
    # Left eye stalk
    draw.line([(x - eye_spacing, eye_y), 
               (x - eye_spacing, eye_y - stalk_height)],
              fill=shell_color, width=line_thickness + 2)
    
    # Right eye stalk
    draw.line([(x + eye_spacing, eye_y), 
               (x + eye_spacing, eye_y - stalk_height)],
              fill=shell_color, width=line_thickness + 2)
    
    # Eye balls
    eye_size = 20
    
    if eye_style == "normal":
        for eye_x in [x - eye_spacing, x + eye_spacing]:
            draw.ellipse([eye_x - eye_size/2, eye_y - stalk_height - eye_size/2,
                         eye_x + eye_size/2, eye_y - stalk_height + eye_size/2],
                        fill=(255, 255, 255), outline=dark_color, width=line_thickness)
            # Pupil
            draw.ellipse([eye_x - 6, eye_y - stalk_height - 6,
                         eye_x + 6, eye_y - stalk_height + 6],
                        fill=(0, 0, 0))
    
    elif eye_style == "googly":
        for eye_x in [x - eye_spacing, x + eye_spacing]:
            draw.ellipse([eye_x - eye_size/2, eye_y - stalk_height - eye_size/2,
                         eye_x + eye_size/2, eye_y - stalk_height + eye_size/2],
                        fill=(255, 255, 255), outline=dark_color, width=line_thickness)
            # Random pupil position
            offset_x = random.uniform(-5, 5)
            offset_y = random.uniform(-5, 5)
            draw.ellipse([eye_x - 5 + offset_x, eye_y - stalk_height - 5 + offset_y,
                         eye_x + 5 + offset_x, eye_y - stalk_height + 5 + offset_y],
                        fill=(0, 0, 0))
    
    elif eye_style == "angry":
        for i, eye_x in enumerate([x - eye_spacing, x + eye_spacing]):
            draw.ellipse([eye_x - eye_size/2, eye_y - stalk_height - eye_size/2,
                         eye_x + eye_size/2, eye_y - stalk_height + eye_size/2],
                        fill=(255, 255, 255), outline=dark_color, width=line_thickness)
            # Eyebrow
            if i == 0:  # Left
                draw.line([(eye_x - 12, eye_y - stalk_height - 15),
                          (eye_x + 8, eye_y - stalk_height - 8)],
                         fill=dark_color, width=line_thickness)
            else:  # Right
                draw.line([(eye_x - 8, eye_y - stalk_height - 8),
                          (eye_x + 12, eye_y - stalk_height - 15)],
                         fill=dark_color, width=line_thickness)
            # Pupil
            draw.ellipse([eye_x - 5, eye_y - stalk_height - 5,
                         eye_x + 5, eye_y - stalk_height + 5],
                        fill=(0, 0, 0))
    
    elif eye_style == "hearts":
        for eye_x in [x - eye_spacing, x + eye_spacing]:
            eye_cy = eye_y - stalk_height
            # Simple heart with two circles and triangle
            draw.ellipse([eye_x - 10, eye_cy - 12, eye_x, eye_cy - 2],
                        fill=(255, 100, 150), outline=dark_color, width=3)
            draw.ellipse([eye_x, eye_cy - 12, eye_x + 10, eye_cy - 2],
                        fill=(255, 100, 150), outline=dark_color, width=3)
            draw.polygon([(eye_x - 10, eye_cy - 6), (eye_x + 10, eye_cy - 6), (eye_x, eye_cy + 8)],
                        fill=(255, 100, 150), outline=dark_color, width=3)
    
    elif eye_style == "stars":
        for eye_x in [x - eye_spacing, x + eye_spacing]:
            eye_cy = eye_y - stalk_height
            # Simple 5-pointed star
            star_pts = []
            for i in range(10):
                angle = i * 36 - 90
                radius = 12 if i % 2 == 0 else 5
                px = eye_x + radius * math.cos(math.radians(angle))
                py = eye_cy + radius * math.sin(math.radians(angle))
                star_pts.append((px, py))
            draw.polygon(star_pts, fill=(255, 220, 100), outline=dark_color, width=3)
    
    elif eye_style == "laser":
        for eye_x in [x - eye_spacing, x + eye_spacing]:
            eye_cy = eye_y - stalk_height
            draw.ellipse([eye_x - eye_size/2, eye_cy - eye_size/2,
                         eye_x + eye_size/2, eye_cy + eye_size/2],
                        fill=(255, 0, 0), outline=(255, 100, 100), width=4)
            # Laser beam
            draw.line([(eye_x, eye_cy - eye_size/2), (eye_x, eye_cy - 80)],
                     fill=(255, 0, 0), width=5)
    
    ###########
    # CLAWS (two kite/diamond shapes as pincers - BIGGER)
    ###########
    claw_y = body_y + 50
    base_claw_size = 65 * claw_size  # Increased from 40
    
    # Left claw
    left_claw_x = x - body_width/2 - 25
    # Arm (thicker)
    draw.rectangle([left_claw_x - 15, claw_y - 12,
                   x - body_width/2 + 5, claw_y + 12],
                  fill=shell_color, outline=dark_color, width=line_thickness)
    
    # Upper pincer (kite/diamond shape - bigger)
    upper_pincer_left = [
        (left_claw_x, claw_y),
        (left_claw_x - base_claw_size * 0.7, claw_y - base_claw_size * 0.4),
        (left_claw_x - base_claw_size * 1.1, claw_y - base_claw_size * 0.2),
        (left_claw_x - base_claw_size * 0.6, claw_y),
    ]
    draw.polygon(upper_pincer_left, fill=shell_color, outline=dark_color, width=line_thickness)
    
    # Lower pincer (kite/diamond shape - bigger)
    lower_pincer_left = [
        (left_claw_x, claw_y),
        (left_claw_x - base_claw_size * 0.7, claw_y + base_claw_size * 0.4),
        (left_claw_x - base_claw_size * 1.1, claw_y + base_claw_size * 0.2),
        (left_claw_x - base_claw_size * 0.6, claw_y),
    ]
    draw.polygon(lower_pincer_left, fill=shell_color, outline=dark_color, width=line_thickness)
    
    # Right claw
    right_claw_x = x + body_width/2 + 25
    # Arm (thicker)
    draw.rectangle([x + body_width/2 - 5, claw_y - 12,
                   right_claw_x + 15, claw_y + 12],
                  fill=shell_color, outline=dark_color, width=line_thickness)
    
    # Upper pincer (kite/diamond shape - bigger)
    upper_pincer_right = [
        (right_claw_x, claw_y),
        (right_claw_x + base_claw_size * 0.7, claw_y - base_claw_size * 0.4),
        (right_claw_x + base_claw_size * 1.1, claw_y - base_claw_size * 0.2),
        (right_claw_x + base_claw_size * 0.6, claw_y),
    ]
    draw.polygon(upper_pincer_right, fill=shell_color, outline=dark_color, width=line_thickness)
    
    # Lower pincer (kite/diamond shape - bigger)
    lower_pincer_right = [
        (right_claw_x, claw_y),
        (right_claw_x + base_claw_size * 0.7, claw_y + base_claw_size * 0.4),
        (right_claw_x + base_claw_size * 1.1, claw_y + base_claw_size * 0.2),
        (right_claw_x + base_claw_size * 0.6, claw_y),
    ]
    draw.polygon(lower_pincer_right, fill=shell_color, outline=dark_color, width=line_thickness)
    
    ###########
    # ACCESSORY
    ###########
    # Helper positions
    hat_y = head_y - head_radius - 10
    glasses_y = eye_y - 5
    bow_y = body_y + body_height - 20
    antenna_spacing = 25
    
    # HEAD ACCESSORIES
    if accessory == "crown":
        crown_pts = [
            (x - 35, hat_y), (x - 25, hat_y - 25), (x - 12, hat_y - 10),
            (x, hat_y - 30), (x + 12, hat_y - 10), (x + 25, hat_y - 25), (x + 35, hat_y),
        ]
        draw.polygon(crown_pts, fill=(255, 215, 0), outline=dark_color, width=line_thickness)
    
    elif accessory == "chef_hat":
        draw.rectangle([x - 45, hat_y, x + 45, hat_y + 15],
                      fill=(255, 255, 255), outline=dark_color, width=line_thickness)
        draw.ellipse([x - 40, hat_y - 40, x + 40, hat_y + 8],
                    fill=(255, 255, 255), outline=dark_color, width=line_thickness)
    
    elif accessory == "pirate_hat":
        hat_pts = [(x - 55, hat_y), (x - 40, hat_y - 35), (x + 40, hat_y - 35), (x + 55, hat_y)]
        draw.polygon(hat_pts, fill=(40, 40, 40), outline=dark_color, width=line_thickness)
        draw.ellipse([x - 15, hat_y - 25, x + 15, hat_y - 5],
                    fill=(255, 255, 255), outline=dark_color, width=3)
    
    elif accessory == "top_hat":
        draw.rectangle([x - 50, hat_y, x + 50, hat_y + 12],
                      fill=(40, 40, 40), outline=dark_color, width=line_thickness)
        draw.rectangle([x - 35, hat_y - 50, x + 35, hat_y],
                      fill=(40, 40, 40), outline=dark_color, width=line_thickness)
    
    elif accessory == "wizard_hat":
        wizard_pts = [(x - 50, hat_y), (x, hat_y - 60), (x + 50, hat_y)]
        draw.polygon(wizard_pts, fill=(80, 60, 150), outline=dark_color, width=line_thickness)
        # Stars on hat
        for sx in [x - 15, x + 15]:
            draw.ellipse([sx - 4, hat_y - 30 - 4, sx + 4, hat_y - 30 + 4],
                        fill=(255, 215, 0))
    
    elif accessory == "cowboy_hat":
        draw.ellipse([x - 55, hat_y - 5, x + 55, hat_y + 15],
                    fill=(139, 90, 43), outline=dark_color, width=line_thickness)
        draw.ellipse([x - 35, hat_y - 35, x + 35, hat_y + 5],
                    fill=(139, 90, 43), outline=dark_color, width=line_thickness)
    
    elif accessory == "viking_helmet":
        draw.ellipse([x - 40, hat_y - 30, x + 40, hat_y + 10],
                    fill=(180, 180, 180), outline=dark_color, width=line_thickness)
        # Horns
        draw.polygon([(x - 40, hat_y - 10), (x - 55, hat_y - 40), (x - 35, hat_y - 15)],
                    fill=(220, 220, 200), outline=dark_color, width=line_thickness)
        draw.polygon([(x + 40, hat_y - 10), (x + 55, hat_y - 40), (x + 35, hat_y - 15)],
                    fill=(220, 220, 200), outline=dark_color, width=line_thickness)
    
    elif accessory == "birthday_hat":
        birthday_pts = [(x - 30, hat_y), (x, hat_y - 50), (x + 30, hat_y)]
        draw.polygon(birthday_pts, fill=(255, 100, 150), outline=dark_color, width=line_thickness)
        draw.ellipse([x - 8, hat_y - 58, x + 8, hat_y - 42],
                    fill=(255, 215, 0))
    
    elif accessory == "halo":
        draw.ellipse([x - 35, hat_y - 50, x + 35, hat_y - 35],
                    fill=None, outline=(255, 215, 0), width=6)
    
    elif accessory == "beanie":
        draw.ellipse([x - 42, hat_y - 25, x + 42, hat_y + 10],
                    fill=(200, 80, 80), outline=dark_color, width=line_thickness)
        draw.ellipse([x - 8, hat_y - 30, x + 8, hat_y - 14],
                    fill=(180, 60, 60))
    
    elif accessory == "sombrero":
        draw.ellipse([x - 65, hat_y, x + 65, hat_y + 15],
                    fill=(210, 180, 140), outline=dark_color, width=line_thickness)
        draw.ellipse([x - 35, hat_y - 25, x + 35, hat_y + 8],
                    fill=(210, 180, 140), outline=dark_color, width=line_thickness)
    
    elif accessory == "fez":
        draw.polygon([(x - 28, hat_y), (x - 22, hat_y - 35), (x + 22, hat_y - 35), (x + 28, hat_y)],
                    fill=(180, 40, 40), outline=dark_color, width=line_thickness)
        draw.ellipse([x - 6, hat_y - 42, x + 6, hat_y - 30],
                    fill=(255, 215, 0))
    
    elif accessory == "baseball_cap":
        draw.ellipse([x - 40, hat_y - 20, x + 40, hat_y + 10],
                    fill=(80, 100, 180), outline=dark_color, width=line_thickness)
        draw.polygon([(x - 42, hat_y), (x - 65, hat_y + 5), (x - 42, hat_y + 10)],
                    fill=(80, 100, 180), outline=dark_color, width=line_thickness)
    
    elif accessory == "backwards_cap":
        draw.ellipse([x - 40, hat_y - 20, x + 40, hat_y + 10],
                    fill=(220, 100, 100), outline=dark_color, width=line_thickness)
        draw.polygon([(x + 42, hat_y), (x + 65, hat_y + 5), (x + 42, hat_y + 10)],
                    fill=(220, 100, 100), outline=dark_color, width=line_thickness)
    
    elif accessory == "beret":
        draw.ellipse([x - 38, hat_y - 18, x + 38, hat_y + 8],
                    fill=(100, 60, 100), outline=dark_color, width=line_thickness)
        draw.ellipse([x - 5, hat_y - 20, x + 5, hat_y - 10],
                    fill=(90, 50, 90))
    
    # FACE ACCESSORIES
    elif accessory == "sunglasses":
        draw.ellipse([x - eye_spacing - 18, glasses_y - 15, x - eye_spacing + 18, glasses_y + 15],
                    fill=(40, 40, 40), outline=dark_color, width=line_thickness)
        draw.ellipse([x + eye_spacing - 18, glasses_y - 15, x + eye_spacing + 18, glasses_y + 15],
                    fill=(40, 40, 40), outline=dark_color, width=line_thickness)
        draw.line([(x - 12, glasses_y), (x + 12, glasses_y)], fill=dark_color, width=line_thickness)
    
    elif accessory == "3d_glasses":
        draw.ellipse([x - eye_spacing - 18, glasses_y - 15, x - eye_spacing + 18, glasses_y + 15],
                    fill=(255, 50, 50), outline=dark_color, width=line_thickness)
        draw.ellipse([x + eye_spacing - 18, glasses_y - 15, x + eye_spacing + 18, glasses_y + 15],
                    fill=(50, 150, 255), outline=dark_color, width=line_thickness)
        draw.line([(x - 12, glasses_y), (x + 12, glasses_y)], fill=dark_color, width=line_thickness)
    
    elif accessory == "monocle":
        draw.ellipse([x + eye_spacing - 15, glasses_y - 15, x + eye_spacing + 15, glasses_y + 15],
                    fill=None, outline=dark_color, width=line_thickness + 1)
        draw.line([(x + eye_spacing + 15, glasses_y), (x + eye_spacing + 25, glasses_y + 15)],
                 fill=dark_color, width=line_thickness)
    
    elif accessory == "aviator_sunglasses":
        for side_x in [x - eye_spacing, x + eye_spacing]:
            pts = [(side_x - 18, glasses_y - 15), (side_x + 18, glasses_y - 15),
                   (side_x + 15, glasses_y + 15), (side_x - 15, glasses_y + 15)]
            draw.polygon(pts, fill=(100, 100, 100), outline=dark_color, width=line_thickness)
        draw.line([(x - 12, glasses_y - 5), (x + 12, glasses_y - 5)], fill=dark_color, width=line_thickness)
    
    elif accessory == "heart_sunglasses":
        for side_x in [x - eye_spacing, x + eye_spacing]:
            draw.ellipse([side_x - 15, glasses_y - 15, side_x - 2, glasses_y - 2],
                        fill=(255, 100, 150), outline=dark_color, width=3)
            draw.ellipse([side_x + 2, glasses_y - 15, side_x + 15, glasses_y - 2],
                        fill=(255, 100, 150), outline=dark_color, width=3)
            draw.polygon([(side_x - 15, glasses_y - 7), (side_x + 15, glasses_y - 7), (side_x, glasses_y + 12)],
                        fill=(255, 100, 150), outline=dark_color, width=3)
        draw.line([(x - 12, glasses_y), (x + 12, glasses_y)], fill=dark_color, width=line_thickness)
    
    elif accessory == "star_sunglasses":
        for side_x in [x - eye_spacing, x + eye_spacing]:
            star_pts = []
            for i in range(10):
                angle = i * 36 - 90
                radius = 15 if i % 2 == 0 else 7
                px = side_x + radius * math.cos(math.radians(angle))
                py = glasses_y + radius * math.sin(math.radians(angle))
                star_pts.append((px, py))
            draw.polygon(star_pts, fill=(255, 215, 100), outline=dark_color, width=3)
        draw.line([(x - 12, glasses_y), (x + 12, glasses_y)], fill=dark_color, width=line_thickness)
    
    elif accessory == "nerd_glasses":
        draw.rectangle([x - eye_spacing - 15, glasses_y - 12, x - eye_spacing + 15, glasses_y + 12],
                      fill=None, outline=dark_color, width=line_thickness + 1)
        draw.rectangle([x + eye_spacing - 15, glasses_y - 12, x + eye_spacing + 15, glasses_y + 12],
                      fill=None, outline=dark_color, width=line_thickness + 1)
        draw.line([(x - 12, glasses_y), (x + 12, glasses_y)], fill=dark_color, width=line_thickness)
    
    elif accessory == "eye_patch":
        draw.ellipse([x - eye_spacing - 15, glasses_y - 15, x - eye_spacing + 15, glasses_y + 15],
                    fill=(40, 40, 40), outline=dark_color, width=line_thickness)
        draw.line([(x - eye_spacing - 15, glasses_y), (x - 60, glasses_y - 20)],
                 fill=dark_color, width=line_thickness)
        draw.line([(x - eye_spacing + 15, glasses_y), (x + 60, glasses_y - 20)],
                 fill=dark_color, width=line_thickness)
    
    elif accessory == "mask":
        mask_pts = [(x - 50, glasses_y), (x - 35, glasses_y - 12), (x + 35, glasses_y - 12), (x + 50, glasses_y),
                    (x + 50, glasses_y + 15), (x + 35, glasses_y + 12), (x - 35, glasses_y + 12), (x - 50, glasses_y + 15)]
        draw.polygon(mask_pts, fill=(150, 50, 150), outline=dark_color, width=line_thickness)
        # Eye holes
        draw.ellipse([x - eye_spacing - 8, glasses_y - 8, x - eye_spacing + 8, glasses_y + 8],
                    fill=(0, 0, 0))
        draw.ellipse([x + eye_spacing - 8, glasses_y - 8, x + eye_spacing + 8, glasses_y + 8],
                    fill=(0, 0, 0))
    
    elif accessory == "goggles":
        draw.ellipse([x - eye_spacing - 18, glasses_y - 15, x - eye_spacing + 18, glasses_y + 15],
                    fill=(150, 200, 220), outline=dark_color, width=line_thickness + 1)
        draw.ellipse([x + eye_spacing - 18, glasses_y - 15, x + eye_spacing + 18, glasses_y + 15],
                    fill=(150, 200, 220), outline=dark_color, width=line_thickness + 1)
        draw.line([(x - 12, glasses_y), (x + 12, glasses_y)], fill=(100, 100, 100), width=line_thickness + 2)
    
    
    # NECK/BODY ACCESSORIES
    elif accessory == "bow_tie":
        draw.polygon([(x - 35, bow_y - 12), (x - 15, bow_y - 18), (x - 15, bow_y + 18), (x - 35, bow_y + 12)],
                    fill=(200, 50, 50), outline=dark_color, width=line_thickness)
        draw.polygon([(x + 35, bow_y - 12), (x + 15, bow_y - 18), (x + 15, bow_y + 18), (x + 35, bow_y + 12)],
                    fill=(200, 50, 50), outline=dark_color, width=line_thickness)
        draw.ellipse([x - 12, bow_y - 12, x + 12, bow_y + 12],
                    fill=(200, 50, 50), outline=dark_color, width=line_thickness)
    
    elif accessory == "necktie":
        draw.polygon([(x - 12, bow_y - 10), (x + 12, bow_y - 10), (x + 8, bow_y + 30), (x - 8, bow_y + 30)],
                    fill=(80, 80, 180), outline=dark_color, width=line_thickness)
    
    elif accessory == "gold_chain":
        chain_y = bow_y - 15
        for i in range(7):
            cx = x - 30 + i * 10
            draw.ellipse([cx - 4, chain_y - 4, cx + 4, chain_y + 4],
                        fill=(255, 215, 0), outline=dark_color, width=2)
        # Pendant
        draw.polygon([(x - 8, chain_y + 5), (x + 8, chain_y + 5), (x, chain_y + 20)],
                    fill=(255, 215, 0), outline=dark_color, width=2)
    
    elif accessory == "pearl_necklace":
        chain_y = bow_y - 15
        for i in range(9):
            cx = x - 32 + i * 8
            draw.ellipse([cx - 5, chain_y - 5, cx + 5, chain_y + 5],
                        fill=(245, 245, 250), outline=dark_color, width=2)
    
    elif accessory == "scarf":
        draw.polygon([(x - 25, bow_y - 15), (x + 25, bow_y - 15), (x + 30, bow_y + 15), (x + 15, bow_y + 40),
                     (x - 15, bow_y + 40), (x - 30, bow_y + 15)],
                    fill=(200, 100, 100), outline=dark_color, width=line_thickness)
    
    elif accessory == "lei":
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            fx = x + 35 * math.cos(rad)
            fy = bow_y + 25 * math.sin(rad)
            colors = [(255, 100, 150), (255, 200, 100), (150, 100, 255)]
            color = colors[int(angle / 30) % 3]
            draw.ellipse([fx - 5, fy - 5, fx + 5, fy + 5], fill=color)
    
    elif accessory == "bandana":
        draw.polygon([(x - 40, head_y), (x + 40, head_y), (x + 30, head_y + 15),
                     (x - 30, head_y + 15)],
                    fill=(220, 50, 50), outline=dark_color, width=line_thickness)
    
    elif accessory == "medallion":
        draw.ellipse([x - 15, bow_y + 10, x + 15, bow_y + 40],
                    fill=(255, 215, 0), outline=dark_color, width=line_thickness)
        draw.ellipse([x - 8, bow_y + 17, x + 8, bow_y + 33],
                    fill=(200, 170, 40))
    
    # ANTENNAE
    elif accessory == "antennae_short":
        antenna_len = 50
        draw.line([(x - antenna_spacing, head_y - head_radius),
                   (x - antenna_spacing - 10, head_y - head_radius - antenna_len)],
                  fill=dark_color, width=line_thickness)
        draw.line([(x + antenna_spacing, head_y - head_radius),
                   (x + antenna_spacing + 10, head_y - head_radius - antenna_len)],
                  fill=dark_color, width=line_thickness)
    
    elif accessory == "antennae_long":
        antenna_len = 90
        draw.line([(x - antenna_spacing, head_y - head_radius),
                   (x - antenna_spacing - 15, head_y - head_radius - antenna_len)],
                  fill=dark_color, width=line_thickness)
        draw.line([(x + antenna_spacing, head_y - head_radius),
                   (x + antenna_spacing + 15, head_y - head_radius - antenna_len)],
                  fill=dark_color, width=line_thickness)
    
    elif accessory == "antennae_curly":
        start_y = head_y - head_radius
        for side in [-1, 1]:
            start_x = x + side * antenna_spacing
            points = [(start_x, start_y)]
            for i in range(5):
                curve_offset = side * -15 * math.sin(i * 0.8)
                points.append((start_x + curve_offset, start_y - i * 12))
            for i in range(len(points) - 1):
                draw.line([points[i], points[i + 1]], fill=dark_color, width=line_thickness)
    
    elif accessory == "antennae_rainbow":
        antenna_len = 70
        colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130)]
        for i, color in enumerate(colors):
            offset = i * 2
            draw.line([(x - antenna_spacing, head_y - head_radius + offset),
                      (x - antenna_spacing - 15, head_y - head_radius - antenna_len + offset)],
                     fill=color, width=2)
            draw.line([(x + antenna_spacing, head_y - head_radius + offset),
                      (x + antenna_spacing + 15, head_y - head_radius - antenna_len + offset)],
                     fill=color, width=2)
    
    elif accessory == "antennae_glowing":
        antenna_len = 80
        draw.line([(x - antenna_spacing, head_y - head_radius),
                   (x - antenna_spacing - 15, head_y - head_radius - antenna_len)],
                  fill=(100, 255, 255), width=line_thickness + 2)
        draw.line([(x + antenna_spacing, head_y - head_radius),
                   (x + antenna_spacing + 15, head_y - head_radius - antenna_len)],
                  fill=(100, 255, 255), width=line_thickness + 2)
        # Glow tips
        for side_x in [x - antenna_spacing - 15, x + antenna_spacing + 15]:
            draw.ellipse([side_x - 8, head_y - head_radius - antenna_len - 8,
                         side_x + 8, head_y - head_radius - antenna_len + 8],
                        fill=(255, 255, 100))
    
    elif accessory == "antennae_zigzag":
        antenna_len = 70
        for side in [-1, 1]:
            start_x = x + side * antenna_spacing
            start_y = head_y - head_radius
            points = [(start_x, start_y)]
            for i in range(4):
                zigzag = 10 if i % 2 == 0 else -10
                points.append((start_x + side * zigzag, start_y - (i + 1) * 18))
            for i in range(len(points) - 1):
                draw.line([points[i], points[i + 1]], fill=dark_color, width=line_thickness)
    
    # SPECIAL/LEGENDARY
    elif accessory == "smoking_cigar":
        mouth_y = head_y + 20
        draw.rectangle([x + 15, mouth_y - 3, x + 45, mouth_y + 3],
                      fill=(139, 90, 43), outline=dark_color, width=2)
        # Smoke
        for i in range(3):
            sx = x + 45 + i * 8
            sy = mouth_y - 10 - i * 5
            draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4],
                        fill=(200, 200, 200), outline=None)
    
    elif accessory == "bubble_pipe":
        mouth_y = head_y + 20
        draw.line([(x + 15, mouth_y), (x + 35, mouth_y - 15)],
                 fill=(100, 70, 40), width=line_thickness)
        draw.ellipse([x + 30, mouth_y - 20, x + 50, mouth_y],
                    fill=None, outline=dark_color, width=line_thickness)
        # Bubbles
        for i in range(3):
            bx = x + 50 + i * 12
            by = mouth_y - 25 - i * 10
            size = 6 - i
            draw.ellipse([bx - size, by - size, bx + size, by + size],
                        fill=(200, 230, 255), outline=(150, 180, 200), width=2)
    
    elif accessory == "headphones":
        draw.arc([x - 50, head_y - head_radius - 35, x + 50, head_y - head_radius + 15],
                0, 180, fill=(60, 60, 60), width=line_thickness + 2)
        for side_x in [x - 35, x + 35]:
            draw.ellipse([side_x - 15, eye_y - 10, side_x + 15, eye_y + 20],
                        fill=(80, 80, 80), outline=dark_color, width=line_thickness)
    
    elif accessory == "vr_headset":
        draw.rectangle([x - 45, glasses_y - 18, x + 45, glasses_y + 18],
                      fill=(220, 220, 220), outline=dark_color, width=line_thickness)
        # Lenses
        draw.ellipse([x - 25, glasses_y - 10, x - 5, glasses_y + 10],
                    fill=(100, 150, 200))
        draw.ellipse([x + 5, glasses_y - 10, x + 25, glasses_y + 10],
                    fill=(100, 150, 200))
    
    elif accessory == "laurel_wreath":
        for angle in range(-60, 240, 20):
            rad = math.radians(angle)
            lx = x + 45 * math.cos(rad)
            ly = head_y + 45 * math.sin(rad)
            draw.ellipse([lx - 6, ly - 3, lx + 6, ly + 3],
                        fill=(100, 180, 100), outline=(80, 140, 80), width=2)
    
    elif accessory == "diamond_earring":
        ear_y = head_y + 10
        for side_x in [x - head_radius - 5, x + head_radius + 5]:
            draw.polygon([(side_x, ear_y), (side_x - 5, ear_y + 8), (side_x, ear_y + 12), (side_x + 5, ear_y + 8)],
                        fill=(200, 230, 255), outline=dark_color, width=2)
    
    elif accessory == "flower_crown":
        for angle in range(0, 180, 30):
            rad = math.radians(angle + 90)
            fx = x + 40 * math.cos(rad)
            fy = head_y - head_radius + 40 * math.sin(rad) - 20
            colors = [(255, 100, 150), (255, 200, 100), (200, 100, 255), (100, 200, 255)]
            color = colors[int(angle / 30) % 4]
            for petal in range(5):
                petal_rad = math.radians(petal * 72)
                px = fx + 6 * math.cos(petal_rad)
                py = fy + 6 * math.sin(petal_rad)
                draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=color)
            draw.ellipse([fx - 3, fy - 3, fx + 3, fy + 3], fill=(255, 215, 0))
    
    elif accessory == "propeller_hat":
        draw.ellipse([x - 35, hat_y - 15, x + 35, hat_y + 10],
                    fill=(255, 200, 100), outline=dark_color, width=line_thickness)
        # Propeller
        draw.ellipse([x - 3, hat_y - 20, x + 3, hat_y - 14],
                    fill=(180, 180, 180))
        draw.polygon([(x - 30, hat_y - 25), (x - 5, hat_y - 17), (x + 5, hat_y - 17), (x + 30, hat_y - 25)],
                    fill=(200, 200, 200), outline=dark_color, width=2)
    
    elif accessory == "angel_wings":
        wing_y = body_y + 60
        # Left wing
        for i in range(3):
            wing_x = x - 60 - i * 15
            draw.ellipse([wing_x - 20, wing_y - 10 - i * 8, wing_x + 5, wing_y + 20 + i * 8],
                        fill=(255, 255, 255), outline=dark_color, width=line_thickness)
        # Right wing
        for i in range(3):
            wing_x = x + 60 + i * 15
            draw.ellipse([wing_x - 5, wing_y - 10 - i * 8, wing_x + 20, wing_y + 20 + i * 8],
                        fill=(255, 255, 255), outline=dark_color, width=line_thickness)
    
    elif accessory == "devil_horns":
        for side in [-1, 1]:
            horn_x = x + side * 35
            horn_y = head_y - head_radius - 5
            horn_pts = [(horn_x, horn_y), (horn_x + side * 10, horn_y - 25), (horn_x + side * 15, horn_y - 15), (horn_x + side * 5, horn_y)]
            draw.polygon(horn_pts, fill=(200, 50, 50), outline=dark_color, width=line_thickness)

def generate_single_lobster():
    """Generate one lobster for testing"""
    traits = generate_traits()
    bg_color = TRAITS["Background"][traits["Background"]]["color"]
    
    img = Image.new('RGB', (w, h), bg_color)
    draw = ImageDraw.Draw(img)
    
    draw_simple_lobster(draw, w/2, h/2, traits, bg_color)
    
    output_path = "/mnt/user-data/outputs/simple_lobster.png"
    img.save(output_path)
    
    print("✅ Simple lobster generated!")
    print(f"   Background: {traits['Background']}")
    print(f"   Shell Color: {traits['Shell Color']}")
    print(f"   Claw Size: {traits['Claw Size']}")
    print(f"   Eyes: {traits['Eyes']}")
    print(f"   Accessory: {traits['Accessory']}")
    
    return output_path

def generate_grid():
    """Generate a 5x5 grid of 25 simple lobsters"""
    
    grid_x = 5
    grid_y = 5
    cell_size = 700
    grid_w = cell_size * grid_x
    grid_h = cell_size * grid_y
    
    # Create main image
    img = Image.new('RGB', (grid_w, grid_h), (240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    all_traits = []
    lobster_num = 1
    
    print("Generating 5x5 grid of 25 simple lobsters...")
    
    for i in range(grid_x):
        for j in range(grid_y):
            # Generate unique traits
            traits = generate_traits()
            all_traits.append({"lobster_number": lobster_num, "traits": traits})
            
            # Get background color
            lobster_bg = TRAITS["Background"][traits["Background"]]["color"]
            
            # Calculate cell position
            cell_x = i * cell_size
            cell_y = j * cell_size
            
            # Draw background rectangle
            draw.rectangle(
                [cell_x + 2, cell_y + 2, cell_x + cell_size - 2, cell_y + cell_size - 2],
                fill=lobster_bg
            )
            
            # Calculate lobster center position
            lobster_x = cell_x + cell_size / 2
            lobster_y = cell_y + cell_size / 2 - 50
            
            # Draw the lobster
            draw_simple_lobster(draw, lobster_x, lobster_y, traits, lobster_bg)
            
            print(f"✓ Lobster #{lobster_num} ({i},{j})")
            lobster_num += 1
    
    # Save
    output_path = "/mnt/user-data/outputs/simple_lobster_grid_25.png"
    img.save(output_path)
    print(f"\n✅ Grid saved to: {output_path}")
    
    metadata_path = "/mnt/user-data/outputs/simple_lobster_grid_25_traits.json"
    with open(metadata_path, 'w') as f:
        json.dump(all_traits, f, indent=2)
    print(f"✅ Traits saved to: {metadata_path}")
    
    return output_path, metadata_path

if __name__ == "__main__":
    generate_grid()
