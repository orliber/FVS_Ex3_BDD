"""
Assignment Submission Script
Includes inputs for Questions 1, 3, and 4.
"""
import os
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

def main():
    # ==========================================
    # Part (b): Formulas from Assignment 3
    # ==========================================
    
    # --- Question 3a ---
    # Original: F(q & H~p) | G(p -> XFr)
    # Abstraction: We treat complex temporal terms as atomic variables
    # Let A = "F(q & H~p)"
    # Let B = "G(p -> XFr)"
    # This might be too abstract. Let's try slightly deeper:
    # Var 1: F_q_and_H_not_p
    # Var 2: G_p_implies_XFr
    run_test(
        "Q3a_Abstract", 
        "A | B", 
        ["A", "B"]
    )

    # --- Question 3b ---
    # Original: G(p -> (q U (r & Fs)))
    # Since this is a massive temporal formula, the Boolean BDD 
    # of the outer structure is just a single variable if we don't break it down.
    # However, let's assume we want to visualize the inner logic:
    # p -> (q U (r & F_s))
    # We map: U_expr = q U (r & Fs)
    run_test(
        "Q3b_InnerLogic",
        "p -> U_expr",
        ["p", "U_expr"]
    )

    # --- Question 4 (The Game) ---
    # Phi = Phi1 -> ~Phi2
    # Phi1 = G(p -> Xq)
    # Phi2 = G(p | q)
    
    # 1. High level abstraction (Phi1 -> ~Phi2)
    run_test(
        "Q4_HighLevel",
        "Phi1 -> ~Phi2",
        ["Phi1", "Phi2"]
    )
    
    # 2. Trying to capture the boolean structure inside the temporal operators
    # Let's verify the boolean core of Phi1: p -> Xq
    # Variables: p, X_q (Next q)
    run_test(
        "Q4_Phi1_Core",
        "p -> X_q",
        ["p", "X_q"]
    )
    
    # Let's verify the boolean core of Phi2: p | q
    run_test(
        "Q4_Phi2_Core",
        "p | q",
        ["p", "q"]
    )

    # ==========================================
    # Part (c): Custom Formula
    # ==========================================
    # A complex boolean formula: (A -> B) & (B -> C) -> (A -> C)
    # This is Transitivity, should be a Tautology (Resulting BDD should be just True terminal)
    run_test(
        "Custom_Transitivity",
        "(A -> B) & (B -> C) -> (A -> C)",
        ["A", "B", "C"]
    )
    
    # Another example: XOR implemented as (A | B) & ~(A & B)
    run_test(
        "Custom_XOR",
        "(A | B) & ~(A & B)",
        ["A", "B"]
    )

if __name__ == "__main__":
    main()