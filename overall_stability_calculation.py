# -*- coding: utf-8 -*-
"""
Automatic calculation program for overall stability of axial compression members.

Authors: Jianwei Zhang, Chao Yu, Xiya Liu
Affiliation: College of Civil Engineering, Tongji University

Copyright (c) 2025 Jianwei Zhang, Chao Yu, Xiya Liu. All rights reserved.

This script calculates the overall stability of an axial compression member
with an H-shaped (or I-shaped) cross-section according to the given
sectional dimensions, material properties, and loading conditions.
"""

import sys

import numpy as np


# ============================================================
# 1. Input parameters
# ============================================================

# Flange plate width: 250 millimeters
b_flange = 250
# Flange plate height: 12 millimeters
h_flange = 12
# Web width: 8 millimeters
b_web = 8
# Web height: 250 millimeters
h_web = 250

# Force: 2000 kilo-newton
N = 2000000

# Calculate length: x: 6000 millimeters; y: 3000 millimeters
l_0x = 6000
l_0y = 3000

# 345 steel yield point: 345 megapascal
f_y345 = 345
# 235 steel yield point: 235 megapascal
f_y235 = 235
# 345 steel design value: 305 megapascal
f_d = 305
# Elastic modulus: 206000 megapascal
E = 206000

# Stability coefficient table of axial compression members
data = [
    [1.000, 1.000, 1.000, 0.999, 0.999, 0.998, 0.997, 0.996, 0.995, 0.994],
    [0.992, 0.991, 0.989, 0.987, 0.985, 0.983, 0.981, 0.978, 0.976, 0.973],
    [0.970, 0.967, 0.963, 0.960, 0.957, 0.953, 0.950, 0.946, 0.943, 0.939],
    [0.936, 0.932, 0.929, 0.925, 0.922, 0.918, 0.914, 0.910, 0.906, 0.903],
    [0.899, 0.895, 0.891, 0.887, 0.882, 0.878, 0.874, 0.870, 0.865, 0.861],
    [0.856, 0.852, 0.847, 0.842, 0.838, 0.833, 0.828, 0.823, 0.818, 0.813],
    [0.807, 0.802, 0.797, 0.791, 0.786, 0.780, 0.774, 0.769, 0.763, 0.757],
    [0.751, 0.746, 0.739, 0.732, 0.726, 0.720, 0.714, 0.707, 0.701, 0.694],
    [0.688, 0.681, 0.675, 0.668, 0.661, 0.655, 0.648, 0.641, 0.635, 0.628],
    [0.621, 0.614, 0.608, 0.601, 0.594, 0.588, 0.581, 0.575, 0.568, 0.561],
    [0.555, 0.549, 0.542, 0.536, 0.529, 0.523, 0.517, 0.511, 0.505, 0.499],
    [0.493, 0.487, 0.481, 0.475, 0.470, 0.464, 0.458, 0.453, 0.447, 0.442],
    [0.437, 0.432, 0.426, 0.421, 0.416, 0.411, 0.406, 0.402, 0.397, 0.392],
    [0.387, 0.383, 0.378, 0.374, 0.370, 0.365, 0.361, 0.357, 0.353, 0.349],
    [0.345, 0.341, 0.337, 0.333, 0.329, 0.326, 0.322, 0.318, 0.315, 0.311],
    [0.308, 0.304, 0.301, 0.298, 0.295, 0.291, 0.288, 0.285, 0.282, 0.279],
    [0.276, 0.273, 0.270, 0.267, 0.265, 0.262, 0.259, 0.256, 0.254, 0.251],
    [0.249, 0.246, 0.244, 0.241, 0.239, 0.236, 0.234, 0.232, 0.229, 0.227],
    [0.225, 0.223, 0.220, 0.218, 0.216, 0.214, 0.212, 0.210, 0.208, 0.206],
    [0.204, 0.202, 0.200, 0.198, 0.197, 0.195, 0.193, 0.191, 0.190, 0.188],
    [0.186, 0.184, 0.183, 0.181, 0.180, 0.178, 0.176, 0.175, 0.173, 0.172],
    [0.170, 0.169, 0.167, 0.166, 0.165, 0.163, 0.162, 0.160, 0.159, 0.158],
    [0.156, 0.155, 0.154, 0.153, 0.151, 0.150, 0.149, 0.148, 0.146, 0.145],
    [0.144, 0.143, 0.142, 0.141, 0.140, 0.138, 0.137, 0.136, 0.135, 0.134],
    [0.133, 0.132, 0.131, 0.130, 0.129, 0.128, 0.127, 0.126, 0.125, 0.124],
    [0.123, None, None, None, None, None, None, None, None, None],
]

# Convert to numpy array
data_array = np.array(data)
vector = data_array.flatten()


# ============================================================
# 2. Sectional area
# ============================================================

A = b_flange * h_flange * 2 + b_web * h_web
print(f"cross-sectional area is: ", A)


# ============================================================
# 3. Sectional moment of inertia about x-axis and y-axis
# ============================================================

I_x = (b_flange * (h_web + h_flange * 2) ** 3 - (b_flange - b_web) * h_web ** 3) / 12
print(f"The moment of inertia of the x-axis cross-section is: ", I_x)

I_y = (2 * h_flange * b_flange ** 3 + h_web * b_web ** 3) / 12
print(f"The moment of inertia of the y-axis cross-section is: ", I_y)


# ============================================================
# 4. Radius of rotation for x-axis and y-axis
# ============================================================

i_x = (I_x / A) ** 0.5
print(f"x-axis cross-section rotation radius: ", i_x)

i_y = (I_y / A) ** 0.5
print(f"y-axis cross-section rotation radius: ", i_y)


# ============================================================
# 5. Slenderness ratio
# ============================================================

# Calculate the slenderness ratio along the x-axis
lambda_x = l_0x / i_x
print(f"aspect ratio of the x-axis", lambda_x)

# Calculate the slenderness ratio along the y-axis
lambda_y = l_0y / i_y
print(f"aspect ratio of the y-axis", lambda_y)

# Verify if the length-to-diameter ratio meets the stiffness requirements.
if lambda_x > 150:
    print("The x-axis does not meet the stiffness requirements")  # Output prompt information
    sys.exit()  # Terminate the program execution
else:
    print(f"lambda_x = {lambda_x}, The x-axis meets the stiffness requirements")

if lambda_y > 150:
    print("The y-axis does not meet the stiffness requirements")  # Output prompt information
    sys.exit()  # Terminate the program execution
else:
    print(f"lambda_y = {lambda_y}, The y-axis meets the stiffness requirements")


# ============================================================
# 6. Stability checking calculation
# ============================================================

# Conversion stability coefficient
if lambda_x > lambda_y:
    # If lambda_x is greater than lambda_y, run formula a.
    lambda_u = lambda_x * (f_y345 / 235) ** 0.5
    print("The x-axis is the strong axis, and the aspect ratio is calculated based on the x-axis.")

if lambda_x < lambda_y:
    # If lambda_x is greater than lambda_y, run formula a.
    lambda_u = lambda_y * (f_y345 / 235) ** 0.5
    print("The y-axis is the strong axis,and the aspect ratio is calculated based on the y-axis.")

print("Converted stability coefficient:", lambda_u)  # Output the conversion of length-to-thickness ratio

# Generate index positions corresponding to vector values (representing the sorting positions of the original data)
indices = np.arange(len(vector))

# Calculate the absolute difference of each element in the vector with a.
differences = np.abs(indices - lambda_u)

# Find the index of the smallest difference (the position of the element closest to a)
closest_idx = np.argmin(differences)

# Determine the two reference points before and after.
if closest_idx == 0:
    # Handle the edge case of the first element
    idx_prev = 0
    idx_next = 1
elif closest_idx == len(vector) - 1:
    # Handle the edge case of the last element
    idx_prev = len(vector) - 2
    idx_next = len(vector) - 1
else:
    # Determine whether to take the left or right side as the reference point before and after.
    if lambda_u < vector[closest_idx]:
        idx_prev = closest_idx - 1
        idx_next = closest_idx
    else:
        idx_prev = closest_idx
        idx_next = closest_idx + 1

# Obtain the values of the reference points before and after.
x0, y0 = indices[idx_prev], vector[idx_prev]
x1, y1 = indices[idx_next], vector[idx_next]

# Linear interpolation calculation
if x1 != x0:  # Avoid division by zero
    phi = y0 - (lambda_u - x0) * (y0 - y1) if y1 != y0 else y0
else:
    phi = y0

# Output result
print(f"Reference point before - Index: {idx_prev}, Value: {y0}")
print(f"Reference point after - Index: {idx_next}, Value: {y1}")
print(f"Interpolation calculation results: {phi:.6f}")

alpha = N / (phi * A * f_d)
print("The overall stability value of the structure:", alpha)

# Assess overall stability
if 0 <= alpha <= 1:
    print("The structure meets the overall stability requirements.")
else:
    print("The structure does not meet the overall stability requirements.")