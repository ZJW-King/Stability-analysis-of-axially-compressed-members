# Automated Calculation Program for the Overall Stability of Axially Compressed Members

An automated calculation program for checking the overall stability of axially compressed steel members with welded I-shaped (H-shaped) cross-sections, developed in accordance with the Chinese national standard GB 50017-2020 Standard for Design of Steel Structures. The repository also includes a companion script that draws the member's cross-section geometric model directly in AutoCAD via pyautocad.

**Authors:** Jianwei Zhang, Chao Yu, Xiya Liu

**Affiliation:** College of Civil Engineering, Tongji University

## Overview

The program performs a complete overall-stability verification workflow:

1. Section area calculation
2. Moment of inertia about the x and y axes (Ix, Iy)
3. Radius of gyration (ix, iy)
4. Slenderness ratio check - lambda <= 150 (stiffness requirement, GB 50017-2020)
5. Overall stability verification - stability coefficient phi via table lookup + linear interpolation, final stress ratio alpha in the range 0-1

> Benchmark result (default section): alpha = 1.022 > 1.0, so the member does NOT satisfy the overall stability requirement.

## Repository Structure

```javascript
.
├── overall_stability_calculation.py   # core stability calculation program
├── drawing.py                         # AutoCAD I-beam geometric model (pyautocad)
├── pyautocad.ipynb                    # pyautocad API exploration notebook
└── README.md
```

## Theoretical Basis (GB 50017-2020)

### 1. Section Properties

A  = 2*bf*hf + bw*hw
Ix = (bf*(hw + 2*hf)^3 - (bf - bw)*hw^3) / 12
Iy = (2*hf*bf^3 + hw*bw^3) / 12

where bf, hf are the flange width and thickness, and bw, hw are the web thickness and height (all in mm).

### 2. Radius of Gyration

ix = sqrt(Ix / A)
iy = sqrt(Iy / A)

### 3. Slenderness Ratio

lambda_x = l0x / ix
lambda_y = l0y / iy
lambda <= 150

### 4. Normalized Slenderness and Stability Coefficient

lambda_bar = lambda * sqrt(fy / 235)

For flame-cut flange edges the section about both axes belongs to Curve b (welded built-up section, no section reduction). The governing axis is the one with the larger slenderness. The stability coefficient phi is obtained by linear interpolation from the Curve b table of GB 50017-2020, implemented programmatically in overall_stability_calculation.py (no manual table lookup needed).

### 5. Overall Stability Check

The member is stable when the section stress does not exceed the critical stress, with the resistance partial safety factor considered:

alpha = N / (phi * A * fd) <= 1.0

## Getting Started

### Prerequisites

- Python >= 3.9 with numpy
- For drawing.py: Windows OS, AutoCAD installed, and the pyautocad package (pip install pyautocad)

### Installation

```bash
git clone https://github.com/ZJW-King/Stability-analysis-of-axially-compressed-members.git
cd Stability-analysis-of-axially-compressed-members
pip install numpy pyautocad
```

## Usage

### 1. Stability calculation

```bash
python overall_stability_calculation.py
```

All inputs are defined as variables at the top of the script - edit them directly:

```python
# --- Section dimensions (mm) ---
b_flange = 250      # flange width
h_flange = 12       # flange thickness
b_web    = 8        # web thickness
h_web    = 250      # web height

# --- Loading and lengths ---
N    = 2_000_000    # design axial force (N)
l_0x = 6000         # effective length about x-axis (mm)
l_0y = 3000         # effective length about y-axis (mm)

# --- Material (Q345) ---
f_y345 = 345        # yield strength (MPa)
f_d    = 305        # design strength (MPa)
E      = 206000     # elastic modulus (MPa)
```

### 2. AutoCAD cross-section drawing

Start (or open) AutoCAD, then run:

```bash
python drawing.py
```

The script connects to the active AutoCAD document (create_if_not_exists=True starts a new one if none is open) and draws the top flange, web, and bottom flange of the I-beam with AddLine, printing "I-beam geometric model drawing is completed !" when finished. Section dimensions in drawing.py mirror the calculation script.

### Sample output (default parameters)

```javascript
cross-sectional area is:  8000
The moment of inertia of the x-axis cross-section is:  113454666.67
The moment of inertia of the y-axis cross-section is:  31260666.67
x-axis cross-section rotation radius:  119.09
y-axis cross-section rotation radius:  62.51
aspect ratio of the x-axis 50.38
aspect ratio of the y-axis 47.99
lambda_x = 50.38, The x-axis meets the stiffness requirements
lambda_y = 47.99, The y-axis meets the stiffness requirements
Converted stability coefficient: 61.05   (lambda_bar = lambda_x*sqrt(345/235), x-axis governs)
Reference point before - Index: 60, Value: 0.802
Reference point after  - Index: 61, Value: 0.797
Interpolation calculation results: 0.8018
The overall stability value of the structure: 1.0223
The structure does not meet the overall stability requirements.
```


<img width="1668" height="845" alt="image" src="https://github.com/user-attachments/assets/e56bfde1-e970-49c1-884e-7fbfc48b7c8f" />


## Calculation Flow

```javascript
Input section / load / material parameters
        |
        v
Section area A ---> Ix, Iy ---> ix, iy
        |
        v
Slenderness lambda_x, lambda_y ---> lambda <= 150 ? (stiffness gate; exit if violated)
        |
        v
Governing axis (max lambda) ---> lambda_bar ---> phi: table lookup + linear interpolation
        |
        v
alpha = N / (phi*A*fd) <= 1.0 ? ---> PASS / FAIL
```

<img width="1232" height="790" alt="image" src="https://github.com/user-attachments/assets/ac9c7bd6-c8f5-4fc1-8f66-b4c5c0323f00" />


## Key Implementation Details

**Stability coefficient interpolation** (overall_stability_calculation.py):

```python
indices = np.arange(len(vector))          # index positions of the table values
differences = np.abs(indices - lambda_u)  # distance to each table position
closest_idx = np.argmin(differences)      # nearest table entry

# pick the two bracketing reference points (with edge-case handling)
...
# linear interpolation between the two bracketing phi values
phi = y0 - (lambda_u - x0) * (y0 - y1) / (x1 - x0)
```

**AutoCAD connection** (drawing.py):

```python
from pyautocad import APoint, Autocad

acad = Autocad(create_if_not_exists=True)
acad.prompt("Hello, Autocad from Python")
acad.model.AddLine(p1, p2)   # top flange / web / bottom flange edges
```

> Tip: see pyautocad.ipynb for a hands-on tour of the pyautocad API - Autocad / APoint methods, adding text/lines/circles, and iterating over drawing objects.

## Notes and Limitations

- The stability coefficient table embedded in the script corresponds to Curve b of GB 50017-2020 (flame-cut edges, welded I-section) - switch the table for other curve classes or section types.
- All inputs are currently hard-coded at the top of each script; adapt as needed for batch or parameterized use.
- drawing.py requires a Windows COM connection to AutoCAD and cannot run headless.

## References

- GB 50017-2020, Standard for Design of Steel Structures
- pyautocad documentation: https://pyautocad.readthedocs.io/

## License

MIT License - see LICENSE for details.

Copyright © 2025 Jianwei Zhang, Chao Yu, Xiya Liu. All rights reserved.
