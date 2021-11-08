# 3D CANDU-6 Quarter Core Input Files

## Description of files:

### **burnmodel.pbs:**
*-Portable Batch System file using Bash*

*-This file is the main script controlling the Serpent program, refueling python script, and data management.*

*-This script used Serpent 2.1.31, Python 3.2, and SerpentTools.*

### **refueler.py:**
#### Python script used for checking results, refueling/fuel shuffling, and writing new Serpent 2 input files (fuelmats).

### **burnmodel:**
#### Primary Serpent 2 input file
*-fdsa*

### **fuelmats:**
#### Serpent 2 material definitions for all 1140 fuel bundles.
