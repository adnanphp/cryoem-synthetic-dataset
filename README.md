# Synthetic Cryo-EM Dataset

A synthetic cryo-electron microscopy (cryo-EM) image dataset and simulation pipeline for machine learning experiments in particle quality classification.

The project generates three classes of 128×128 grayscale cryo-EM-like images representing good particles, degraded/bad particles, and background noise.

## Dataset

The current dataset contains:

- **3 classes**
- **1,000 images per class**
- **3,000 images total**
- **128×128 pixels**
- **8-bit grayscale PNG**
- Approximately **13 MB**

### Classes

| Class | Description |
|---|---|
| `class0_good_particles` | Clean, well-defined simulated protein particles |
| `class1_bad_particles` | Noisy, degraded, aggregated, or contaminated particles |
| `class2_pure_noise` | Background/no-particle images dominated by noise |

## Simulation

The dataset is generated using a custom `CryoEMSimulator` class.

The simulation includes:

- Gaussian particle structures
- Contrast Transfer Function (CTF) effects
- Poisson noise representing electron-counting statistics
- Gaussian detector noise
- Ice contamination
- Multiple/overlapping particles
- Random particle positions
- Random rotations
- Different signal-to-noise conditions

## Project Structure

```text
cryoem-synthetic-dataset/
├── dataset_generation.py
├── cryoem_simulator.py
├── requirements.txt
├── README.md
└── data/
    └── simulated_3class/
        ├── class0_good_particles/
        ├── class1_bad_particles/
        └── class2_pure_noise/
Generate the Dataset

Install the dependencies:

pip install -r requirements.txt

Generate the full dataset:

python dataset_generation.py --size full --image_size 128

Generate a smaller dataset for quick experiments:

python dataset_generation.py --size small --image_size 128

Generate a very small test dataset:

python dataset_generation.py --size test --image_size 64
Intended Applications

The dataset is intended for experimentation with:

Cryo-EM particle classification
Particle picking
Image preprocessing
CNN-based classification
Synthetic-data machine learning
Robustness to noise and imaging artifacts
Synthetic-to-real domain-transfer experiments
Current Status

This repository currently focuses on dataset generation and simulation.

Future experiments may include:

CNN baseline models
ResNet/MobileNet comparisons
Noise and CTF robustness experiments
Domain-shift evaluation
Synthetic-to-real transfer
Model interpretability
Disclaimer

This is a synthetic research dataset generated for machine learning experimentation. It is not intended to reproduce the full physical complexity of experimental cryo-EM imaging or replace experimentally acquired datasets.

Author

Muhammad Adnan Shahzad

GitHub: https://github.com/adnanphp
