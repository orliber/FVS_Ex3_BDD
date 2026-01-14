# ROBDD Python Package
### Formal Verification and Synthesis - Assignment 3

## 📖 Overview
This project implements a **Reduced Ordered Binary Decision Diagram (ROBDD)** package in Python. It allows for the construction, manipulation, and visualization of BDDs from boolean formulas.

The package features a custom recursive descent parser that converts string formulas into BDD structures, automatically applies reduction rules (removing redundant nodes and merging isomorphic subgraphs), and exports the results to Graphviz formats.

## ✨ Features
* **Formula Parsing:** Supports complex boolean expressions with operator precedence.
* **Canonical Representation:** Ensures unique nodes for equivalent sub-formulas using a hash map.
* **Automatic Reduction:** Implements the BDD reduction rule (`low == high` -> return child) on the fly.
* **Visualization:** Auto-generates `.png` images of the BDD trees using Graphviz.
* **Export Formats:** Supports textual output (`.txt`) and DOT language (`.dot`).

## 🛠️ Supported Logic Syntax
The parser supports the following boolean operators (ordered by precedence):

| Operator | Symbol | Description |
| :--- | :---: | :--- |
| **Not** | `~` | Negation |
| **And** | `&` | Conjunction |
| **Or** | `|` | Disjunction |
| **Implication** | `->` | If... Then... |
| **Iff** | `<->` | Equivalence |
| **Grouping** | `( )` | Parentheses for explicit precedence |

## 📂 Project Structure
* `robdd.py`: The core library containing the `ROBDD` class, node structure, parser logic, and export functions.
* `test_formulas.py`: Assignment submission script. Generates BDDs for Q3, Q4, and custom test cases.
* `submission_outputs/`: Directory where the generated results (.txt, .dot, .png) are saved.

## ⚙️ Prerequisites & Installation

To generate the visual graphs, you need **Graphviz** installed on your system.

### 1. Install Graphviz (System Tool)
* **macOS:**
    ```bash
    brew install graphviz
    ```
* **Ubuntu/Debian:**
    ```bash
    sudo apt-get install graphviz
    ```
* **Windows:**
    Download the installer from [Graphviz.org](https://graphviz.org/download/) and ensure the `bin` folder is added to your system PATH.

### 2. Install Python Dependencies
Install the Python wrapper for Graphviz:
```bash
pip3 install graphviz
```

## 🚀 Usage

### Running the Assignment Tests
Run the main test script to process the formulas defined in the assignment:

```bash
python3 test_formulas.py
```
This will create a `submission_outputs` folder containing the visual and textual representations of the BDDs.

### Using as a Library
You can use the `build_robdd` function in your own scripts:

```python
from robdd import build_robdd

# Define your formula and variable ordering
formula = "(A -> B) & A"
ordering = ["A", "B"]

# Generate BDD and save output to 'my_result' (.png/.txt/.dot)
robdd, root_node = build_robdd(formula, ordering, "my_result")

print(f"Root node index: {root_node}")
```

## 🤖 AI Use Disclosure
I utilized an AI assistant (Gemini) to assist in the development of the Python BDD package. Specifically, I used the AI to:
* Refactor the initial BDD class structure to support parsing of complex boolean formulas.
* Implement the "Dot" export functionality to visualize the BDDs using Graphviz.
* Create an abstraction layer in the test script to map LTL temporal operators into boolean variables.

I manually verified the code's correctness by testing it against known tautologies (such as the Transitivity law), confirming that the resulting BDD correctly reduced to the generic 'True' terminal node.
