"""
Quick test to verify everything works
"""

# Test 1: Import and create simulator
print("Test 1: Importing CryoEMSimulator...")
from cryoem_simulator import CryoEMSimulator

sim = CryoEMSimulator(image_size=64)
print("✓ Simulator created successfully")

# Test 2: Generate one image of each class
print("\nTest 2: Generating sample images...")
good_particle = sim.generate_good_particle()
bad_particle = sim.generate_bad_particle()
pure_noise = sim.generate_pure_noise()

print(f"Good particle shape: {good_particle.shape}")
print(f"Good particle range: [{good_particle.min():.3f}, {good_particle.max():.3f}]")
print(f"Bad particle shape: {bad_particle.shape}")
print(f"Pure noise shape: {pure_noise.shape}")
print("✓ Sample images generated successfully")

# Test 3: Save sample images
print("\nTest 3: Saving sample images...")
import os
os.makedirs("test_samples", exist_ok=True)

sim.save_image(good_particle, "test_samples/good_particle.png")
sim.save_image(bad_particle, "test_samples/bad_particle.png")
sim.save_image(pure_noise, "test_samples/pure_noise.png")
print("✓ Sample images saved to test_samples/")

# Test 4: Generate small dataset
print("\nTest 4: Generating small dataset (3 classes, 10 samples each)...")
from dataset_generation import generate_dataset
generate_dataset(num_samples_per_class=10, image_size=64)
print("✓ Small dataset generated successfully")

print("\n" + "="*50)
print("ALL TESTS PASSED! ✅")
print("="*50)
print("\nTo generate full dataset, run:")
print("python dataset_generation.py --size full")
