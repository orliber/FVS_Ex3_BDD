# ROBDD Python Package
### Formal Verification and Synthesis - Assignment 3

## Overview
This project implements a **Reduced Ordered Binary Decision Diagram (ROBDD)** package in Python.
The package parses boolean formulas, constructs the corresponding BDD structure, performs reduction (removing redundant nodes and merging isomorphic subgraphs), and exports the results as text and visualizations.

## Files
* `robdd.py`: The core library containing the BDD node structure, parser, and reduction logic.
* `test_formulas.py`: Test script that generates BDDs for the assignment formulas and custom test cases.

## Prerequisites & Installation

To generate the visual graphs (PNG files), you need both the system-level Graphviz tool and the Python wrapper.

### 1. Install Graphviz (System Tool)
* **macOS:**
  ```bash
  brew install graphviz
Windows/Linux: Download from Graphviz.org or use your package manager.

2. Install Python Dependencies

Bash
pip3 install graphviz
Usage
Run the main test script to process the formulas:

Bash
python3 test_formulas.py
Outputs

The results will be generated in the submission_outputs/ directory. For each formula, three files are created:

.txt: Textual representation of the BDD structure.

.dot: Graphviz source description.

.png: Visual image of the BDD graph.

AI Use Disclosure
I utilized an AI assistant (Gemini) to assist in the development of the Python BDD package. Specifically, I used the AI to:

Refactor the initial BDD class structure to support parsing of complex boolean formulas.

Implement the "Dot" export functionality to visualize the BDDs using Graphviz.

Create an abstraction layer in the test script to map the LTL temporal operators (from Assignment 3) into boolean variables that the BDD package can process.

I manually verified the code's correctness by testing it against known tautologies (such as the Transitivity law), confirming that the resulting BDD correctly reduced to the generic 'True' terminal node.
