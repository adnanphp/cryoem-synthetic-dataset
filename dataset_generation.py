"""
Main script to generate 3-class cryo-EM dataset
"""

import os
import sys
from tqdm import tqdm
import numpy as np
from cryoem_simulator import CryoEMSimulator

def create_directory_structure():
    """Create folder structure for dataset"""
    base_dir = "data/simulated_3class"
    classes = ["class0_good_particles", "class1_bad_particles", "class2_pure_noise"]
    
    for class_dir in classes:
        os.makedirs(os.path.join(base_dir, class_dir), exist_ok=True)
    
    return base_dir, classes

def generate_dataset(num_samples_per_class=1000, image_size=128):
    """
    Generate the complete 3-class dataset
    
    Args:
        num_samples_per_class: Number of images per class
        image_size: Size of generated images (square)
    """
    
    print("=" * 60)
    print("CRYO-EM DATASET GENERATION")
    print("=" * 60)
    print(f"Image size: {image_size}x{image_size}")
    print(f"Samples per class: {num_samples_per_class}")
    print(f"Total images: {3 * num_samples_per_class}")
    print("=" * 60)
    
    # Create directories
    base_dir, classes = create_directory_structure()
    
    # Initialize simulator
    simulator = CryoEMSimulator(image_size=image_size)
    
    # Generate visualization examples first
    print("\n1. Generating example visualizations...")
    simulator.visualize_examples(num_examples=3)
    
    # Calculate statistics
    print("\n2. Calculating dataset statistics...")
    stats = simulator.get_dataset_statistics(num_samples=50)
    
    # Generate dataset
    print("\n3. Generating full dataset...")
    
    # Class 0: Good particles
    print(f"\nGenerating Class 0: Good particles...")
    for i in tqdm(range(num_samples_per_class), desc="Class 0"):
        img = simulator.generate_good_particle()
        filename = os.path.join(base_dir, classes[0], f"good_particle_{i:04d}.png")
        simulator.save_image(img, filename)
    
    # Class 1: Bad particles
    print(f"\nGenerating Class 1: Bad particles...")
    for i in tqdm(range(num_samples_per_class), desc="Class 1"):
        img = simulator.generate_bad_particle()
        filename = os.path.join(base_dir, classes[1], f"bad_particle_{i:04d}.png")
        simulator.save_image(img, filename)
    
    # Class 2: Pure noise
    print(f"\nGenerating Class 2: Pure noise...")
    for i in tqdm(range(num_samples_per_class), desc="Class 2"):
        img = simulator.generate_pure_noise()
        filename = os.path.join(base_dir, classes[2], f"pure_noise_{i:04d}.png")
        simulator.save_image(img, filename)
    
    # Create dataset summary
    print("\n4. Creating dataset summary...")
    create_dataset_summary(base_dir, classes, num_samples_per_class, image_size)
    
    print("\n" + "=" * 60)
    print("DATASET GENERATION COMPLETE!")
    print("=" * 60)
    print(f"Dataset saved to: {base_dir}")
    print(f"Classes: {len(classes)}")
    print(f"Total images: {3 * num_samples_per_class}")
    print("\nFolder structure:")
    print_dataset_structure(base_dir)

def create_dataset_summary(base_dir, classes, num_samples_per_class, image_size):
    """Create a summary text file about the dataset"""
    summary_file = os.path.join(base_dir, "dataset_summary.txt")
    
    with open(summary_file, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("CRYO-EM SIMULATED DATASET SUMMARY\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("DATASET INFORMATION:\n")
        f.write(f"  Number of classes: {len(classes)}\n")
        f.write(f"  Images per class: {num_samples_per_class}\n")
        f.write(f"  Total images: {len(classes) * num_samples_per_class}\n")
        f.write(f"  Image size: {image_size}x{image_size} pixels\n")
        f.write(f"  Format: PNG (8-bit grayscale)\n\n")
        
        f.write("CLASS DESCRIPTIONS:\n")
        f.write("  1. class0_good_particles: Clean, well-defined protein particles\n")
        f.write("     - Mild CTF effects\n")
        f.write("     - Low noise (SNR: 15-25)\n")
        f.write("     - Good contrast\n\n")
        
        f.write("  2. class1_bad_particles: Noisy, aggregated, or damaged particles\n")
        f.write("     - Strong CTF effects (high defocus)\n")
        f.write("     - High noise (SNR: 5-10)\n")
        f.write("     - Multiple overlapping particles\n")
        f.write("     - Ice contamination\n\n")
        
        f.write("  3. class2_pure_noise: Background/empty areas\n")
        f.write("     - Random Gaussian noise\n")
        f.write("     - Structural noise (ice/carbon artifacts)\n")
        f.write("     - No real particles\n\n")
        
        f.write("SIMULATION PARAMETERS:\n")
        f.write("  - Gaussian particle shapes\n")
        f.write("  - Contrast Transfer Function (CTF) applied\n")
        f.write("  - Poisson noise (electron counting statistics)\n")
        f.write("  - Gaussian noise (detector noise)\n")
        f.write("  - Ice contamination simulation\n")
        f.write("  - Random rotations and positions\n\n")
        
        f.write("INTENDED USE:\n")
        f.write("  Training CNNs for cryo-EM particle picking\n")
        f.write("  Binary/ternary classification: particle vs noise\n")
        f.write("  Testing preprocessing methods for cryo-EM\n\n")
        
        f.write("GENERATED: " + str(np.datetime64('now')) + "\n")
        f.write("=" * 60 + "\n")
    
    print(f"Dataset summary saved to: {summary_file}")

def print_dataset_structure(base_dir):
    """Print the generated folder structure"""
    print(f"\n{base_dir}/")
    for root, dirs, files in os.walk(base_dir):
        level = root.replace(base_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        if level == 1:  # Class directories
            # Show first few files
            for i, file in enumerate(sorted(files)[:3]):
                if i == 0:
                    print(f"{subindent}{file}")
                elif i == 1:
                    print(f"{subindent}{file}")
                elif i == 2:
                    print(f"{subindent}{file}")
                    if len(files) > 3:
                        print(f"{subindent}... ({len(files) - 3} more files)")
        elif level == 0 and "dataset_summary.txt" in files:
            print(f"{subindent}dataset_summary.txt")

def verify_dataset(base_dir, classes, num_to_check=5):
    """Verify that dataset was generated correctly"""
    print("\n5. Verifying dataset...")
    
    for class_idx, class_name in enumerate(classes):
        class_path = os.path.join(base_dir, class_name)
        files = os.listdir(class_path)
        
        print(f"\n  {class_name}:")
        print(f"    Files found: {len(files)}")
        
        # Check file sizes
        sizes = []
        for i in range(min(num_to_check, len(files))):
            file_path = os.path.join(class_path, files[i])
            size = os.path.getsize(file_path)
            sizes.append(size)
        
        avg_size = np.mean(sizes) / 1024  # Convert to KB
        print(f"    Average file size: {avg_size:.1f} KB")
        
        # Check images are readable
        from PIL import Image
        try:
            test_file = os.path.join(class_path, files[0])
            img = Image.open(test_file)
            print(f"    Image format: {img.format}, Size: {img.size}, Mode: {img.mode}")
            img.close()
        except Exception as e:
            print(f"    Error reading image: {e}")
    
    print("\n✓ Dataset verification complete!")

def create_small_test_dataset():
    """Create a small test dataset for quick experimentation"""
    print("\nCreating small test dataset (for quick testing)...")
    generate_dataset(num_samples_per_class=100, image_size=64)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate cryo-EM dataset")
    parser.add_argument("--size", type=str, default="full", 
                       choices=["small", "medium", "full", "test"],
                       help="Dataset size")
    parser.add_argument("--image_size", type=int, default=128,
                       help="Image size in pixels")
    
    args = parser.parse_args()
    
    if args.size == "test":
        # Very small for testing
        generate_dataset(num_samples_per_class=50, image_size=64)
    elif args.size == "small":
        # Small dataset
        generate_dataset(num_samples_per_class=300, image_size=args.image_size)
    elif args.size == "medium":
        # Medium dataset
        generate_dataset(num_samples_per_class=1000, image_size=args.image_size)
    else:  # full
        # Full dataset (as specified in requirements)
        generate_dataset(num_samples_per_class=1000, image_size=args.image_size)
