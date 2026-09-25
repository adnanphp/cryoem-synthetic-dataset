# 🔬 Synthetic Cryo-EM Dataset

> A synthetic cryo-electron microscopy (cryo-EM) image dataset and simulation pipeline for machine-learning experiments in particle quality classification.

This repository provides a configurable **cryo-EM image simulator** for generating synthetic particle images under different imaging conditions, noise levels, and structural artifacts.

The current dataset contains three classes of **128×128 grayscale cryo-EM-like images** representing good particles, degraded particles, and background noise.

---

## 📊 Dataset Overview

| Property         |                   Value |
| ---------------- | ----------------------: |
| Classes          |                   **3** |
| Images per class |               **1,000** |
| Total images     |               **3,000** |
| Image size       |           **128 × 128** |
| Format           | **8-bit grayscale PNG** |
| Dataset size     |              **~13 MB** |

### Classes

| Class                   | Description                                            |
| ----------------------- | ------------------------------------------------------ |
| `class0_good_particles` | Clean, well-defined simulated protein particles        |
| `class1_bad_particles`  | Noisy, degraded, aggregated, or contaminated particles |
| `class2_pure_noise`     | Background/no-particle images dominated by noise       |

---

## 🧪 Simulation Pipeline

The dataset is generated using a custom **`CryoEMSimulator`** class.

The simulator incorporates several effects designed to produce realistic cryo-EM-like images:

### Particle Generation

* Gaussian particle structures
* Random particle positions
* Random rotations
* Multiple and overlapping particles

### Imaging Effects

* Contrast Transfer Function (**CTF**) effects
* Variable signal-to-noise conditions

### Noise and Contamination

* Poisson noise representing electron-counting statistics
* Gaussian detector noise
* Ice contamination
* Particle degradation
* Background noise

### Simulation Workflow

```text
Particle Parameters
        │
        ▼
Gaussian Particle Generation
        │
        ▼
Random Position / Rotation
        │
        ▼
Multiple Particle Composition
        │
        ▼
CTF Application
        │
        ▼
Poisson + Gaussian Noise
        │
        ▼
Ice / Contamination Effects
        │
        ▼
Normalization
        │
        ▼
128×128 Grayscale Image
```

---

## 🧠 Why Synthetic Cryo-EM Data?

Obtaining and labeling large cryo-EM datasets can be challenging. Synthetic data provides a controlled environment for testing machine-learning methods before applying them to experimental data.

The simulator allows experiments where individual factors can be varied systematically, including:

* Particle quality
* Noise level
* CTF effects
* Particle overlap
* Contamination
* Background conditions
* Signal-to-noise ratio

This makes the dataset useful for studying **model robustness and domain shift**.

---

## 📁 Project Structure

```text
cryoem-synthetic-dataset/
│
├── dataset_generation.py
│   └── Dataset generation CLI
│
├── cryoem_simulator.py
│   └── Cryo-EM image simulation engine
│
├── requirements.txt
├── README.md
│
└── data/
    └── simulated_3class/
        ├── class0_good_particles/
        ├── class1_bad_particles/
        └── class2_pure_noise/
```

---

# 🚀 Getting Started

## Requirements

* Python 3.x
* NumPy
* Scientific Python dependencies listed in `requirements.txt`

### Install Dependencies

```bash
pip install -r requirements.txt
```

Using a virtual environment is recommended:

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## 🏗️ Generate the Dataset

### Full Dataset

Generate the current full dataset:

```bash
python dataset_generation.py --size full --image_size 128
```

This generates:

```text
1,000 good particles
1,000 bad particles
1,000 pure-noise images
------------------------
3,000 total images
```

### Small Dataset

For quick development and experimentation:

```bash
python dataset_generation.py --size small --image_size 128
```

### Test Dataset

For rapid testing of the pipeline:

```bash
python dataset_generation.py --size test --image_size 64
```

Generated images are stored under:

```text
data/simulated_3class/
```

---

# 🔬 Intended Applications

The dataset can be used for experiments involving:

### Cryo-EM Analysis

* Particle-quality classification
* Particle picking
* Image preprocessing
* Noise characterization
* Imaging-artifact analysis

### Machine Learning

* CNN-based image classification
* Synthetic-data experimentation
* Robustness testing
* Data augmentation
* Representation learning
* Domain-shift evaluation
* Synthetic-to-real transfer learning

---

# 🤖 Potential ML Workflow

A possible downstream classification pipeline is:

```text
Synthetic Cryo-EM Dataset
          │
          ▼
     Preprocessing
          │
          ▼
    Train / Validation / Test
          │
          ▼
       CNN Model
          │
          ▼
   Particle Classification
          │
          ▼
 Robustness / Domain-Shift
       Evaluation
```

Possible future models include:

* CNN baseline
* ResNet
* MobileNet
* Vision Transformer
* Contrastive-learning models

---

# 📈 Future Work

Planned or potential extensions include:

* [ ] CNN baseline classifier
* [ ] ResNet/MobileNet comparison
* [ ] Systematic noise robustness experiments
* [ ] CTF robustness evaluation
* [ ] Particle-overlap experiments
* [ ] Domain-shift evaluation
* [ ] Synthetic-to-real transfer learning
* [ ] Model interpretability with saliency/attention methods
* [ ] Expanded particle morphology simulation
* [ ] Larger synthetic datasets
* [ ] Quantitative comparison with experimental cryo-EM datasets

---

# ⚠️ Scientific Disclaimer

This repository contains a **synthetic research dataset** generated by a computational simulation pipeline.

The images are intended for **machine-learning experimentation and methodological development**. They are not intended to reproduce the complete physical complexity of experimental cryo-EM imaging and should not be treated as a replacement for experimentally acquired cryo-EM datasets.

Results obtained exclusively on this synthetic dataset should therefore be validated against appropriate experimental data before drawing conclusions about real-world cryo-EM performance.

---

# 📄 License

This project is available under the **MIT License**.

See the `LICENSE` file for details.

---

# 👨‍💻 Author

**Muhammad Adnan Shahzad**

GitHub: https://github.com/adnanphp

---

<div align="center">

### 🔬 Synthetic Cryo-EM × Machine Learning

**Scientific Computing • Image Simulation • Computer Vision • Machine Learning**

</div>
