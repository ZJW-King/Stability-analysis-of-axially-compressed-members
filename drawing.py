# -*- coding: utf-8 -*-
"""
Draw an I-beam geometric model in AutoCAD using pyautocad.

This script connects to an existing AutoCAD instance (or creates a new one),
draws the top flange, web, and bottom flange of an I-beam based on the
provided sectional dimensions, and outputs a completion prompt.

Requirements:
    - Windows OS with AutoCAD installed
    - pyautocad
"""

import math

from pyautocad import APoint, Autocad


# ============================================================
# 1. Connect to AutoCAD
# ============================================================

acad = Autocad(create_if_not_exists=True)
# acad.prompt()
acad.prompt("Hello, Autocad from Python")
print(acad.doc.Name)


# ============================================================
# 2. Input parameters
# ============================================================

flange_length_top = 250
flange_height_top = 12
web_length = 250
web_thickness = 8
flange_length_bottom = 250
flange_height_bottom = 12


# ============================================================
# 3. Regulation factor
# ============================================================

w1 = flange_length_top - 250
h1 = flange_height_top - 12
w2 = web_length - 250
h2 = web_thickness - 8
w3 = flange_length_bottom - 250
h3 = flange_height_bottom - 12


# ============================================================
# 4. Define the size parameters
# ============================================================

p1 = APoint(0, 274 + w2 + h3 + h1)
p2 = APoint(250 + w1, 274 + w2 + h3 + h1)
p3 = APoint(0, 262 + w2 + h3)
p4 = APoint(250 + w1, 262 + w2 + h3)
p5 = APoint(121 + w3 / 2, 262 + w2 + h3)
p6 = APoint(129 + w3 / 2, 262 + w2 + h3)
p7 = APoint(121 + w3 / 2, 12 + h3)
p8 = APoint(129 + w3 / 2, 12 + h3)
p9 = APoint(0, 12 + h3)
p10 = APoint(250 + w3, 12 + h3)
p11 = APoint(0, 0)
p12 = APoint(250 + w3, 0)


# ============================================================
# 5. Draw the I-beam
# ============================================================

# Top flange plate
acad.model.AddLine(p1, p2)
acad.model.AddLine(p1, p3)
acad.model.AddLine(p2, p4)
acad.model.AddLine(p3, p4)

# Web
acad.model.AddLine(p5, p7)
acad.model.AddLine(p6, p8)

# Bottom flange plate
acad.model.AddLine(p9, p10)
acad.model.AddLine(p9, p11)
acad.model.AddLine(p10, p12)
acad.model.AddLine(p11, p12)

acad.prompt("I-beam geometric model drawing is completed !\n")