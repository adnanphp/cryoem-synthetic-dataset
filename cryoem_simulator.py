"""
Cryo-EM Image Simulator for Particle Classification
Simplified version for educational purposes
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, rotate
from scipy.signal import convolve2d
import random
from PIL import Image
import os

class CryoEMSimulator:
    """
    Simulates cryo-EM images with particles and noise
    Generates 3 classes:
    - Class 0: Good particles (clean, well-defined)
    - Class 1: Bad particles (noisy, aggregated)
    - Class 2: Pure noise/background
    """
    
    def __init__(self, image_size=128, particle_size=20):
        """
        Initialize simulator
        
        Args:
            image_size: Output image size (square)
            particle_size: Approximate particle diameter in pixels
        """
        self.image_size = image_size
        self.particle_size = particle_size
        self.center = image_size // 2
        
        # Create coordinate grid
        x = np.linspace(-1, 1, image_size)
        y = np.linspace(-1, 1, image_size)
        self.X, self.Y = np.meshgrid(x, y)
        
    def _create_gaussian_particle(self, sigma=1.0, amplitude=1.0):
        """Create a Gaussian-shaped particle"""
        distance = np.sqrt(self.X**2 + self.Y**2)
        particle = amplitude * np.exp(-distance**2 / (2 * sigma**2))
        return particle
    
    def _create_protein_like_particle(self, complexity=1):
        """Create more realistic protein-like shape"""
        # Base shape
        base = self._create_gaussian_particle(sigma=0.3, amplitude=1.0)
        
        # Add some asymmetry for realism
        if complexity >= 2:
            # Add secondary blob (protein domain)
            offset_x = random.uniform(-0.3, 0.3)
            offset_y = random.uniform(-0.3, 0.3)
            domain = 0.5 * np.exp(-((self.X - offset_x)**2 + (self.Y - offset_y)**2) / (2 * 0.2**2))
            base += domain
        
        if complexity >= 3:
            # Add noise to shape
            shape_noise = np.random.normal(0, 0.1, (self.image_size, self.image_size))
            base += shape_noise * 0.2
        
        return base
    
    def _apply_ctf(self, image, defocus=1.0, voltage=300):
        """
        Apply simplified Contrast Transfer Function (CTF)
        Simulates electron microscope characteristics
        """
        # Create frequency grid
        freq_x = np.fft.fftfreq(self.image_size)
        freq_y = np.fft.fftfreq(self.image_size)
        fx, fy = np.meshgrid(freq_x, freq_y)
        spatial_freq = np.sqrt(fx**2 + fy**2)
        
        # CTF parameters (simplified)
        wavelength = 12.26 / np.sqrt(voltage * 1000 + 0.9785 * voltage**2)  # Angstrom
        cs = 2.0  # Spherical aberration (mm)
        
        # CTF model (simplified sinusoidal form)
        chi = np.pi * wavelength * spatial_freq**2 * (defocus * 1e4 - 0.5 * cs * wavelength**2 * spatial_freq**2)
        ctf = -np.sin(chi) * np.exp(-(spatial_freq / 0.5)**4)  # Envelope function
        
        # Apply in Fourier space
        image_fft = np.fft.fft2(image)
        image_fft *= np.fft.fftshift(ctf)
        image_ctf = np.real(np.fft.ifft2(image_fft))
        
        return image_ctf
    
    def _add_poisson_noise(self, image, snr=10):
        """Add Poisson (shot) noise common in electron microscopy"""
        # Scale image to have desired signal-to-noise ratio
        max_val = np.max(np.abs(image))
        image_scaled = image / max_val * snr
        
        # Add Poisson noise
        noisy = np.random.poisson(np.abs(image_scaled) * 100) / 100.0
        
        # Normalize back
        noisy = noisy / np.max(noisy) * max_val if np.max(noisy) > 0 else noisy
        
        return noisy
    
    def _add_gaussian_noise(self, image, noise_level=0.1):
        """Add Gaussian noise"""
        noise = np.random.normal(0, noise_level, image.shape)
        return image + noise
    
    def _add_ice_contamination(self, image, severity=0.3):
        """Simulate ice contamination (common in cryo-EM)"""
        ice_pattern = np.random.rand(self.image_size, self.image_size) * severity
        return image + ice_pattern
    
    def generate_good_particle(self):
        """Generate a good, clean particle image (Class 0)"""
        # Create clean particle
        particle = self._create_protein_like_particle(complexity=2)
        
        # Apply mild CTF
        particle = self._apply_ctf(particle, defocus=random.uniform(1.0, 2.0))
        
        # Add mild noise
        particle = self._add_poisson_noise(particle, snr=random.uniform(15, 25))
        particle = self._add_gaussian_noise(particle, noise_level=random.uniform(0.02, 0.05))
        
        # Mild ice contamination
        particle = self._add_ice_contamination(particle, severity=random.uniform(0.1, 0.2))
        
        # Normalize
        particle = (particle - np.min(particle)) / (np.max(particle) - np.min(particle) + 1e-8)
        
        return particle
    
    def generate_bad_particle(self):
        """Generate a bad/noisy/aggregated particle (Class 1)"""
        # Create multiple overlapping particles (aggregation)
        num_particles = random.randint(2, 4)
        particle = np.zeros((self.image_size, self.image_size))
        
        for _ in range(num_particles):
            # Create offset particle
            single_particle = self._create_protein_like_particle(complexity=1)
            
            # Random rotation
            angle = random.uniform(0, 360)
            single_particle = rotate(single_particle, angle, reshape=False)
            
            # Random position shift (for aggregation effect)
            shift_x = random.randint(-10, 10)
            shift_y = random.randint(-10, 10)
            single_particle = np.roll(single_particle, shift=(shift_x, shift_y), axis=(0, 1))
            
            particle += single_particle
        
        # Apply strong CTF (high defocus)
        particle = self._apply_ctf(particle, defocus=random.uniform(3.0, 5.0))
        
        # Add heavy noise
        particle = self._add_poisson_noise(particle, snr=random.uniform(5, 10))
        particle = self._add_gaussian_noise(particle, noise_level=random.uniform(0.1, 0.3))
        
        # Severe ice contamination
        particle = self._add_ice_contamination(particle, severity=random.uniform(0.3, 0.5))
        
        # Normalize
        particle = (particle - np.min(particle)) / (np.max(particle) - np.min(particle) + 1e-8)
        
        return particle
    
    def generate_pure_noise(self):
        """Generate pure noise/background (Class 2)"""
        # Start with Gaussian noise
        noise = np.random.normal(0, 1, (self.image_size, self.image_size))
        
        # Add some structural noise (simulating ice or carbon film)
        for _ in range(random.randint(3, 7)):
            # Add Gaussian blobs (simulating contamination)
            x = random.randint(0, self.image_size-1)
            y = random.randint(0, self.image_size-1)
            size = random.randint(5, 20)
            amplitude = random.uniform(0.5, 2.0)
            
            # Create Gaussian blob
            xx, yy = np.mgrid[:self.image_size, :self.image_size]
            blob = amplitude * np.exp(-((xx - x)**2 + (yy - y)**2) / (2 * size**2))
            noise += blob
        
        # Add CTF-like effects to noise
        noise = self._apply_ctf(noise, defocus=random.uniform(0.5, 1.5))
        
        # Normalize
        noise = (noise - np.min(noise)) / (np.max(noise) - np.min(noise) + 1e-8)
        
        return noise
    
    def save_image(self, image, filename):
        """Save image as PNG"""
        # Convert to 8-bit for saving
        image_8bit = (image * 255).astype(np.uint8)
        img = Image.fromarray(image_8bit)
        img.save(filename)
    
    def visualize_examples(self, num_examples=3):
        """Generate and display example images from each class"""
        fig, axes = plt.subplots(3, num_examples, figsize=(15, 10))
        
        for class_idx in range(3):
            for example_idx in range(num_examples):
                if class_idx == 0:
                    img = self.generate_good_particle()
                    title = "Good Particle"
                elif class_idx == 1:
                    img = self.generate_bad_particle()
                    title = "Bad Particle"
                else:
                    img = self.generate_pure_noise()
                    title = "Pure Noise"
                
                axes[class_idx, example_idx].imshow(img, cmap='gray')
                axes[class_idx, example_idx].axis('off')
                axes[class_idx, example_idx].set_title(f"{title} {example_idx+1}")
        
        plt.suptitle("Cryo-EM Dataset Examples (3 Classes)", fontsize=16)
        plt.tight_layout()
        plt.savefig('dataset_examples.png', dpi=150, bbox_inches='tight')
        plt.show()
    
    def get_dataset_statistics(self, num_samples=100):
        """Calculate statistics for dataset quality assessment"""
        stats = {
            'class_0_mean': [], 'class_0_std': [],
            'class_1_mean': [], 'class_1_std': [],
            'class_2_mean': [], 'class_2_std': []
        }
        
        print("Calculating dataset statistics...")
        for i in range(num_samples):
            # Class 0
            img0 = self.generate_good_particle()
            stats['class_0_mean'].append(np.mean(img0))
            stats['class_0_std'].append(np.std(img0))
            
            # Class 1
            img1 = self.generate_bad_particle()
            stats['class_1_mean'].append(np.mean(img1))
            stats['class_1_std'].append(np.std(img1))
            
            # Class 2
            img2 = self.generate_pure_noise()
            stats['class_2_mean'].append(np.mean(img2))
            stats['class_2_std'].append(np.std(img2))
        
        print("\n=== Dataset Statistics ===")
        print("Class 0 (Good Particles):")
        print(f"  Mean intensity: {np.mean(stats['class_0_mean']):.3f} ± {np.std(stats['class_0_mean']):.3f}")
        print(f"  Std deviation: {np.mean(stats['class_0_std']):.3f} ± {np.std(stats['class_0_std']):.3f}")
        
        print("\nClass 1 (Bad Particles):")
        print(f"  Mean intensity: {np.mean(stats['class_1_mean']):.3f} ± {np.std(stats['class_1_mean']):.3f}")
        print(f"  Std deviation: {np.mean(stats['class_1_std']):.3f} ± {np.std(stats['class_1_std']):.3f}")
        
        print("\nClass 2 (Pure Noise):")
        print(f"  Mean intensity: {np.mean(stats['class_2_mean']):.3f} ± {np.std(stats['class_2_mean']):.3f}")
        print(f"  Std deviation: {np.mean(stats['class_2_std']):.3f} ± {np.std(stats['class_2_std']):.3f}")
        
        return stats
