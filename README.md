# ROBDD Constructor - Python Package

A simple Python package for constructing and visualizing **Reduced Ordered Binary Decision Diagrams (ROBDDs)**.

This project was prepared for an assignment that requires:
- A GitHub repository with the implementation
- Output files (text or images) for the given formulas
- Output files for at least one additional formula
- A short explanation of testing and (if relevant) AI usage disclosure

---

## Project Structure

Recommended structure:

robdd-package/
├── robdd.py
├── test_formulas.py
├── README.md
└── examples/
└── expected_outputs.md

- **robdd.py**: main ROBDD implementation + exporter
- **test_formulas.py**: test suite + assignment formulas runner
- **examples/expected_outputs.md**: optional reference notes/examples

---

## Features

- ✅ Builds **ROBDD** from boolean formulas
- ✅ Supports operators:
  - AND: `&`
  - OR: `|`
  - NOT: `~`
  - IMPLIES: `->`
  - IFF: `<->`
- ✅ Reduction rules:
  - Removes redundant nodes where `low == high`
  - Shares identical nodes using a unique table (hash-consing)
- ✅ Exports:
  - Text format (`.txt`)
  - Graphviz DOT format (`.dot`) for visualization
- ✅ Custom variable ordering

---

## Requirements

- Python 3.7+
- Graphviz (optional, only if you want PNG images)

### Install Graphviz

**macOS**
```bash
brew install graphviz
Ubuntu/Debian
sudo apt-get install graphviz
Windows
Install from Graphviz official installer, then verify dot works in terminal.
Quick Start
1) Run a simple example
python3 robdd.py
This will run the examples in the __main__ section (if you kept them).
2) Run the full test suite
python3 test_formulas.py
This generates multiple output files:
output_*.txt
output_*.dot
Usage
Build a ROBDD and export outputs
from robdd import build_robdd

robdd, root = build_robdd(
    formula="A & B",
    variable_order=["A", "B"],
    output_prefix="my_bdd"
)

print("Root:", root)
print("Nodes:", len(robdd.nodes))
This creates:
my_bdd.txt
my_bdd.dot
Create an image (PNG) from DOT
dot -Tpng my_bdd.dot -o my_bdd.png
Formula Syntax
Variables
Single-letter or multi-character names:
A, B, x1, var_name
Operators
Operation	Symbol	Example
AND	&	A & B
OR	`	`
NOT	~	~A
IMPLIES	->	A -> B
IFF	<->	A <-> B
Parentheses
Use parentheses for grouping:
(A | B) & C
~(A & B) | (C -> D)
Algorithm Overview
The ROBDD construction uses:
Parsing
Recursive-descent parser that converts a formula string into BDD operations.
Ordered construction
Variable ordering is fixed by variable_order.
Reduction
Eliminate nodes where low == high
Reuse identical nodes (var, low, high) using a unique table (hash-consing)
Operations
AND built using Shannon-style recursion on top variable
OR derived by De Morgan: A | B = ~(~A & ~B)
IMPLIES: A -> B = ~A | B
IFF: A <-> B = (A -> B) & (B -> A)
Outputs
Text output (.txt)
Contains:
root node index
total nodes count
variable order
list of nodes with (var, low, high) or terminal values
DOT output (.dot)
Can be visualized with Graphviz:
Circles = decision nodes
Boxes = terminals (0/1)
Dashed edges = 0-branch (false/low)
Solid edges = 1-branch (true/high)
Assignment: Where to place the given formulas
Open test_formulas.py and edit the function:
def test_assignment3_formulas():
    # Replace examples with the actual assignment formulas
    verify_formula("...", ["..."])
For each formula required by the assignment:
run verify_formula(formula, var_order)
keep the generated .txt and .dot files as your “outputs”
Also add one additional formula of your own (as required).
Testing and Correctness Verification
Recommended verification methods:
Sanity checks
Tautology examples should reduce to terminal 1
A | ~A
Contradiction examples should reduce to terminal 0
A & ~A
Known identities
De Morgan:
~(A & B) should match ~A | ~B (same computed function)
Implication:
A -> B equals ~A | B
Reduction properties
No node should remain with low == high
Identical nodes should be reused (unique table)
If you want a stronger test: add a truth-table evaluator and compare the BDD evaluation against the formula for all assignments (2^n).
(Not required by your current code, but it’s the strongest correctness check.)
AI Usage Disclosure (Template)
If you used an AI assistant, include something like this in your submission:
Tools used
(Example) Claude / ChatGPT
What AI helped with
Explaining ROBDD reduction rules (unique table, eliminating redundant nodes)
Suggesting parser structure (recursive descent)
Suggesting test cases (tautology/contradiction, De Morgan)
How I verified correctness
Ran a suite of tests (basic operators + tautologies + identities)
Checked reduction properties (no redundant nodes, node reuse)
Generated DOT graphs and manually inspected a few small examples
Submission Checklist
 Code pushed to GitHub
 README.md included
 Output files for all assignment formulas (.txt/.dot/optional .png)
 Output files for one additional custom formula
 Testing explanation included
 AI usage disclosure included (if relevant)
