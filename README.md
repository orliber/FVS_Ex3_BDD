# Formal Verification Systems - Exercise 3: BDD Implementation

This repository contains the solution for Exercise 3 in the Formal Verification Systems course. It implements a **Reduced Ordered Binary Decision Diagram (ROBDD)** library in Python and includes test scripts to verify various boolean formulas.

## 👤 Author
**Or Liberman, Noa Amram**

## 📂 Project Structure

The project is organized as follows:

* **`robdd.py`**: The core library containing the `ROBDD` class and implementation of BDD operations (construction, reduction, apply).
* **`test_formulas.py`**: The main execution script. It defines the boolean formulas (e.g., `Q3a_Abstract`, `Q4_HighLevel`), builds the BDDs, and generates the outputs.
* **`submission_outputs/`**: A directory containing the generated results for each test case:
    * `*.png`: Visual representation of the BDD graph.
    * `*.dot`: Graphviz source files.
    * `*.txt`: Textual description of the BDD structure.

## 🛠️ Prerequisites

* **Python 3.x**
* **Graphviz** (Required for generating `.png` images from `.dot` files)

To install the Python dependency for Graphviz (if used):
```bash
pip install graphviz
```

## 🚀 How to Run

To run the assignment and generate all BDD visualizations and text outputs, execute the `test_formulas.py` script:

```bash
python3 test_formulas.py
```

### Expected Output
Upon running the script, the `submission_outputs/` folder will be populated with files for the specific test cases, such as:
* `Q3a_Abstract`
* `Q4_HighLevel`
* `Custom_Transitivity`
* `Custom_XOR`

Each case will have its corresponding `.txt`, `.dot`, and `.png` files demonstrating the BDD structure and reduction.

## 📝 Implementation Details
The project implements:
1.  **Shannon Expansion**: Recursive construction of the BDD.
2.  **Isomorphism Reduction**: Merging identical sub-graphs.
3.  **Redundant Node Elimination**: Removing nodes where high and low children are identical.

## 🤖 AI Use Disclosure
AI tools were used to assist in generating documentation, debugging code snippets, and optimizing the project structure. All logical implementations and final code verifications were conducted by the author.

---
*Submitted by Or Liberman, Noa Amram, 2026.*
