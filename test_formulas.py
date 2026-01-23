"""
Assignment Submission Script
Includes inputs for Questions 1a, 1b, and 1c.
"""
import os
import shutil
from robdd import build_robdd

def run_test(name, formula, var_order):
    print(f"\n--- Processing: {name} ---")
    print(f"Formula: {formula}")
    output_dir = "submission_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Sanitize filename
    safe_name = name.replace(" ", "_").replace(".", "")
    path = os.path.join(output_dir, safe_name)
    
    robdd, root = build_robdd(formula, var_order, path)
    print(f"Nodes created: {len(robdd.nodes)}")
    print(f"Output saved to {path}.txt/dot/png")
    
    # Display if result is tautology or contradiction
    if root == robdd.terminal_true:
        print("Result: TAUTOLOGY (always True)")
    elif root == robdd.terminal_false:
        print("Result: CONTRADICTION (always False)")

def main():
    # ==========================================
    # Clean output directory at start
    # ==========================================
    output_dir = "submission_outputs"
    
    # Remove the directory and all its contents if it exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"Cleared previous outputs from {output_dir}/")
    
    # Create fresh output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created fresh output directory: {output_dir}/\n")
    print("=" * 60)
    
    # ==========================================
    # Question 1a: (a & ~c) | (b ⊕ d)
    # ==========================================
    # XOR (⊕) is implemented as: b ⊕ d = (b | d) & ~(b & d)
    # Or equivalently: (b & ~d) | (~b & d)
    
    run_test(
        "Q1a_Formula",
        "(a & ~c) | (b ^ d)",
        ["a", "b", "c", "d"]
    )
    
    # Test with different variable orderings to show impact
    run_test(
        "Q1a_Alt_Order1",
        "(a & ~c) | (b ^ d)",
        ["a", "c", "b", "d"]
    )
    
    run_test(
        "Q1a_Alt_Order2",
        "(a & ~c) | (b ^ d)",
        ["b", "d", "a", "c"]
    )

    # ==========================================
    # Question 1b: At least 3 of x1,x2,x3,x4,x5 are true
    # ==========================================
    # This is a majority function (threshold-3 out of 5)
    # We need to enumerate all combinations where >= 3 variables are true
    
    # Method 1: Explicit enumeration (clearer but verbose)
    # All combinations of exactly 3, 4, or 5 variables being true
    formula_1b_explicit = (
        # Exactly 3 true
        "(x1 & x2 & x3 & ~x4 & ~x5) | "
        "(x1 & x2 & ~x3 & x4 & ~x5) | "
        "(x1 & x2 & ~x3 & ~x4 & x5) | "
        "(x1 & ~x2 & x3 & x4 & ~x5) | "
        "(x1 & ~x2 & x3 & ~x4 & x5) | "
        "(x1 & ~x2 & ~x3 & x4 & x5) | "
        "(~x1 & x2 & x3 & x4 & ~x5) | "
        "(~x1 & x2 & x3 & ~x4 & x5) | "
        "(~x1 & x2 & ~x3 & x4 & x5) | "
        "(~x1 & ~x2 & x3 & x4 & x5) | "
        # Exactly 4 true
        "(x1 & x2 & x3 & x4 & ~x5) | "
        "(x1 & x2 & x3 & ~x4 & x5) | "
        "(x1 & x2 & ~x3 & x4 & x5) | "
        "(x1 & ~x2 & x3 & x4 & x5) | "
        "(~x1 & x2 & x3 & x4 & x5) | "
        # All 5 true
        "(x1 & x2 & x3 & x4 & x5)"
    )
    
    run_test(
        "Q1b_AtLeast3of5",
        formula_1b_explicit,
        ["x1", "x2", "x3", "x4", "x5"]
    )
    
    # Test with different variable ordering
    run_test(
        "Q1b_Alt_Order",
        formula_1b_explicit,
        ["x5", "x4", "x3", "x2", "x1"]
    )

    # ==========================================
    # Question 1c: x > y where x and y are 3-bit numbers
    # ==========================================
    # x = x1*4 + x2*2 + x3*1 (x1 is MSB, x3 is LSB)
    # y = y1*4 + y2*2 + y3*1 (y1 is MSB, y3 is LSB)
    
    # x > y can be built hierarchically:
    # x > y iff:
    #   x1 > y1, OR
    #   x1 = y1 AND x2 > y2, OR
    #   x1 = y1 AND x2 = y2 AND x3 > y3
    
    # Simplified:
    # (x1 & ~y1) | 
    # (~(x1 ^ y1) & x2 & ~y2) |
    # (~(x1 ^ y1) & ~(x2 ^ y2) & x3 & ~y3)
    
    formula_1c = (
        "(x1 & ~y1) | "
        "((~(x1 ^ y1)) & x2 & ~y2) | "
        "((~(x1 ^ y1)) & (~(x2 ^ y2)) & x3 & ~y3)"
    )
    
    run_test(
        "Q1c_Comparison",
        formula_1c,
        ["x1", "y1", "x2", "y2", "x3", "y3"]
    )
    
    # Test with different variable ordering (interleaved)
    run_test(
        "Q1c_Alt_Order1",
        formula_1c,
        ["x1", "x2", "x3", "y1", "y2", "y3"]
    )
    
    # Test with another ordering
    run_test(
        "Q1c_Alt_Order2",
        formula_1c,
        ["y1", "x1", "y2", "x2", "y3", "x3"]
    )

    # ==========================================
    # Additional custom formulas
    # ==========================================
    
    # Example 1: Transitivity (Tautology)
    run_test(
        "Custom_Transitivity",
        "(A -> B) & (B -> C) -> (A -> C)",
        ["A", "B", "C"]
    )
    
    # Example 2: XOR formula
    run_test(
        "Custom_XOR",
        "(A | B) & ~(A & B)",
        ["A", "B"]
    )
    
    # Example 3: Half Adder (sum and carry)
    # Sum = A XOR B, Carry = A AND B
    run_test(
        "Custom_HalfAdder_Sum",
        "A ^ B",
        ["A", "B"]
    )

if __name__ == "__main__":
    main()