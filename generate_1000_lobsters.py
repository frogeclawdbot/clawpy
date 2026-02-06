from PIL import Image, ImageDraw
import random
import math
import json
import os

# Import the lobster drawing code
import sys
sys.path.insert(0, '/home/claude')
from simple_lobster import TRAITS, draw_simple_lobster, generate_traits

# Configuration
output_dir = "/mnt/user-data/outputs/lobster_collection_1000"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(f"{output_dir}/images", exist_ok=True)
os.makedirs(f"{output_dir}/metadata", exist_ok=True)

w, h = 1400, 1400

def calculate_rarity_score(traits):
    """Calculate rarity score based on trait rarities (lower rarity = higher score)"""
    total_score = 0
    for category, trait_name in traits.items():
        rarity = TRAITS[category][trait_name]["rarity"]
        # Lower rarity percentage = higher score (invert it)
        total_score += (100 - rarity)
    return round(total_score, 2)

def generate_single_lobster(token_id):
    """Generate one lobster NFT with image and metadata"""
    
    # Generate random traits
    traits = generate_traits()
    
    # Get background color
    bg_color = TRAITS["Background"][traits["Background"]]["color"]
    
    # Create image
    img = Image.new('RGB', (w, h), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw lobster in center
    center_x = w / 2
    center_y = h / 2
    
    draw_simple_lobster(draw, center_x, center_y, traits, bg_color)
    
    # Save image
    image_filename = f"{token_id}.png"
    image_path = f"{output_dir}/images/{image_filename}"
    img.save(image_path)
    
    # Calculate rarity score
    rarity_score = calculate_rarity_score(traits)
    
    # Generate metadata (OpenSea/standard NFT format)
    metadata = {
        "name": f"Lobster #{token_id}",
        "description": "A unique generative lobster from the Lobster NFT collection. Each lobster is algorithmically generated with randomized traits and varying rarity.",
        "image": f"{image_filename}",
        "external_url": "https://your-project-url.com",
        "attributes": [
            {"trait_type": category, "value": value} 
            for category, value in traits.items()
        ],
        "rarity_score": rarity_score
    }
    
    # Save metadata
    metadata_path = f"{output_dir}/metadata/{token_id}.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return {
        "token_id": token_id,
        "traits": traits,
        "rarity_score": rarity_score,
        "image_path": image_path,
        "metadata_path": metadata_path
    }

def generate_collection(num_lobsters=1000):
    """Generate the full NFT collection"""
    
    print(f"🦞 Generating {num_lobsters} Lobster NFTs...")
    print(f"📁 Output directory: {output_dir}")
    print("=" * 60)
    
    collection = []
    
    for i in range(num_lobsters):
        token_id = i + 1
        lobster = generate_single_lobster(token_id)
        collection.append(lobster)
        
        # Progress updates
        if token_id % 50 == 0:
            print(f"✓ Generated {token_id}/{num_lobsters} lobsters...")
    
    print("=" * 60)
    print(f"✅ All {num_lobsters} lobsters generated!")
    
    # Sort by rarity score to assign rarity ranks
    print("\n📊 Calculating rarity ranks...")
    collection.sort(key=lambda x: x['rarity_score'], reverse=True)
    
    # Update metadata with rarity ranks
    for rank, lobster in enumerate(collection, 1):
        metadata_path = lobster['metadata_path']
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        metadata['rarity_rank'] = rank
        metadata['rarity_percentile'] = round((1 - (rank / len(collection))) * 100, 2)
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    # Generate collection summary
    print("📋 Generating collection summary...")
    
    # Count trait distributions
    trait_distribution = {}
    for category in TRAITS.keys():
        trait_distribution[category] = {}
        for lobster in collection:
            trait_value = lobster['traits'][category]
            if trait_value not in trait_distribution[category]:
                trait_distribution[category][trait_value] = 0
            trait_distribution[category][trait_value] += 1
    
    summary = {
        "collection_name": "Lobster NFT Collection",
        "total_supply": num_lobsters,
        "traits": {
            category: list(options.keys())
            for category, options in TRAITS.items()
        },
        "trait_distribution": trait_distribution,
        "rarity_distribution": {
            lobster["token_id"]: {
                "rank": i + 1,
                "score": lobster["rarity_score"],
                "percentile": round((1 - ((i + 1) / len(collection))) * 100, 2)
            }
            for i, lobster in enumerate(collection)
        },
        "top_10_rarest": [
            {
                "token_id": lobster["token_id"],
                "rank": i + 1,
                "score": lobster["rarity_score"],
                "traits": lobster["traits"]
            }
            for i, lobster in enumerate(collection[:10])
        ]
    }
    
    summary_path = f"{output_dir}/collection_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Collection summary saved to: {summary_path}")
    
    # Print statistics
    print("\n" + "=" * 60)
    print("📈 COLLECTION STATISTICS")
    print("=" * 60)
    print(f"Total Lobsters: {num_lobsters}")
    print(f"\n🏆 Top 5 Rarest Lobsters:")
    for i, lobster in enumerate(collection[:5], 1):
        print(f"  #{i}. Lobster #{lobster['token_id']} - Rarity Score: {lobster['rarity_score']}")
        print(f"      Traits: {lobster['traits']}")
    
    print(f"\n📊 Trait Distribution Highlights:")
    for category, counts in trait_distribution.items():
        print(f"\n  {category}:")
        sorted_traits = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:3]
        for trait, count in sorted_traits:
            percentage = (count / num_lobsters) * 100
            print(f"    • {trait}: {count} ({percentage:.1f}%)")
    
    print("\n" + "=" * 60)
    print("✅ COLLECTION GENERATION COMPLETE!")
    print("=" * 60)
    print(f"📁 Images: {output_dir}/images/")
    print(f"📄 Metadata: {output_dir}/metadata/")
    print(f"📊 Summary: {summary_path}")
    print("=" * 60)
    
    return collection, summary_path

if __name__ == "__main__":
    collection, summary_path = generate_collection(num_lobsters=1000)
