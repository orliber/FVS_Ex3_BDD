import os
import re
import sys
from typing import Dict, Set, Tuple, Optional, List
from dataclasses import dataclass

# Try to import graphviz for auto-image generation, handle if missing
try:
    import graphviz
    HAS_GRAPHVIZ = True
except ImportError:
    HAS_GRAPHVIZ = False

@dataclass(frozen=True)
class BDDNode:
    """Represents a node in the BDD"""
    var: Optional[str]       # Variable name (None for terminal nodes)
    low: Optional[int]       # Index of low child (False branch)
    high: Optional[int]      # Index of high child (True branch)
    is_terminal: bool = False
    value: Optional[bool] = None  # For terminal nodes

    def __hash__(self):
        return hash((self.var, self.low, self.high, self.is_terminal, self.value))

class ROBDD:
    """ROBDD Constructor and Manager"""

    def __init__(self, variable_order: List[str]):
        self.variable_order = variable_order
        self.var_to_level = {var: i for i, var in enumerate(variable_order)}
        self.nodes: List[BDDNode] = []
        self.node_map: Dict[BDDNode, int] = {}

        # Terminal nodes (0=False, 1=True)
        self.terminal_false = self._create_node(None, None, None, True, False)
        self.terminal_true = self._create_node(None, None, None, True, True)

    def _create_node(self, var, low, high, is_terminal=False, value=None) -> int:
        node = BDDNode(var, low, high, is_terminal, value)
        if node in self.node_map:
            return self.node_map[node]
        idx = len(self.nodes)
        self.nodes.append(node)
        self.node_map[node] = idx
        return idx

    def make_node(self, var: str, low: int, high: int) -> int:
        # Reduction rule: if high and low are same, return child
        if low == high:
            return low
        return self._create_node(var, low, high)

    # ============================
    # Parsing Logic
    # ============================
    def parse_formula(self, formula: str) -> int:
        # Remove spaces
        formula = formula.replace(" ", "")
        self.tokens = self._tokenize(formula)
        self.pos = 0
        root = self._parse_iff()
        if self.pos != len(self.tokens):
            raise ValueError(f"Unexpected trailing tokens: {self.tokens[self.pos:]}")
        return root

    def _tokenize(self, formula: str) -> List[str]:
        tokens = []
        i = 0
        while i < len(formula):
            char = formula[i]
            if char in "()&|~^":  # Added ^ for XOR
                tokens.append(char)
                i += 1
            elif formula[i: i + 2] == "->":
                tokens.append("->")
                i += 2
            elif formula[i: i + 3] == "<->":
                tokens.append("<->")
                i += 3
            # Allow alphanumerics and underscores for variable names (e.g., X_q, Phi_1)
            elif char.isalnum() or char == "_":
                j = i
                while j < len(formula) and (formula[j].isalnum() or formula[j] == "_"):
                    j += 1
                tokens.append(formula[i:j])
                i = j
            else:
                # Skip unknown characters or raise error
                i += 1
        return tokens

    # Recursive Descent Parser
    def _parse_iff(self) -> int:
        left = self._parse_implies()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == "<->":
            self.pos += 1
            right = self._parse_implies()
            # A <-> B is (A -> B) & (B -> A)
            l_to_r = self._build_implies(left, right)
            r_to_l = self._build_implies(right, left)
            left = self._build_and(l_to_r, r_to_l)
        return left

    def _parse_implies(self) -> int:
        left = self._parse_xor()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == "->":
            self.pos += 1
            right = self._parse_xor()
            left = self._build_implies(left, right)
        return left

    def _parse_xor(self) -> int:
        """Parse XOR operations (^)"""
        left = self._parse_or()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == "^":
            self.pos += 1
            right = self._parse_or()
            left = self._build_xor(left, right)
        return left

    def _parse_or(self) -> int:
        left = self._parse_and()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == "|":
            self.pos += 1
            right = self._parse_and()
            left = self._build_or(left, right)
        return left

    def _parse_and(self) -> int:
        left = self._parse_not()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == "&":
            self.pos += 1
            right = self._parse_not()
            left = self._build_and(left, right)
        return left

    def _parse_not(self) -> int:
        if self.pos < len(self.tokens) and self.tokens[self.pos] == "~":
            self.pos += 1
            return self._build_not(self._parse_not())
        return self._parse_atom()

    def _parse_atom(self) -> int:
        if self.pos >= len(self.tokens):
            raise ValueError("Unexpected end of formula")
        token = self.tokens[self.pos]
        
        if token == "(":
            self.pos += 1
            node = self._parse_iff()
            if self.pos >= len(self.tokens) or self.tokens[self.pos] != ")":
                raise ValueError("Missing closing parenthesis")
            self.pos += 1
            return node
        
        if token[0].isalnum() or token[0] == "_":
            self.pos += 1
            return self._build_variable(token)
            
        raise ValueError(f"Unexpected token: {token}")

    # ============================
    # BDD Operations
    # ============================
    def _build_variable(self, var: str) -> int:
        if var not in self.var_to_level:
            # Auto-add variable if missing? Better to raise error to enforce ordering.
            raise ValueError(f"Variable '{var}' not in declared variable order: {self.variable_order}")
        return self.make_node(var, self.terminal_false, self.terminal_true)

    def _build_not(self, node_idx: int) -> int:
        node = self.nodes[node_idx]
        if node.is_terminal:
            return self.terminal_false if node.value else self.terminal_true
        
        low = self._build_not(node.low)
        high = self._build_not(node.high)
        return self.make_node(node.var, low, high)

    def _build_and(self, idx1: int, idx2: int) -> int:
        if idx1 == self.terminal_false or idx2 == self.terminal_false:
            return self.terminal_false
        if idx1 == self.terminal_true: return idx2
        if idx2 == self.terminal_true: return idx1

        n1, n2 = self.nodes[idx1], self.nodes[idx2]
        lvl1 = self.var_to_level.get(n1.var, float('inf'))
        lvl2 = self.var_to_level.get(n2.var, float('inf'))

        if lvl1 == lvl2:
            low = self._build_and(n1.low, n2.low)
            high = self._build_and(n1.high, n2.high)
            return self.make_node(n1.var, low, high)
        elif lvl1 < lvl2:
            low = self._build_and(n1.low, idx2)
            high = self._build_and(n1.high, idx2)
            return self.make_node(n1.var, low, high)
        else:
            low = self._build_and(idx1, n2.low)
            high = self._build_and(idx1, n2.high)
            return self.make_node(n2.var, low, high)

    def _build_or(self, idx1: int, idx2: int) -> int:
        # De Morgan: A | B = ~(~A & ~B)
        return self._build_not(self._build_and(self._build_not(idx1), self._build_not(idx2)))

    def _build_implies(self, idx1: int, idx2: int) -> int:
        # A -> B = ~A | B
        return self._build_or(self._build_not(idx1), idx2)

    def _build_xor(self, idx1: int, idx2: int) -> int:
        """Build XOR operation: A XOR B = (A | B) & ~(A & B)
        Equivalently: (A & ~B) | (~A & B)"""
        # Using: A XOR B = (A & ~B) | (~A & B)
        left_part = self._build_and(idx1, self._build_not(idx2))
        right_part = self._build_and(self._build_not(idx1), idx2)
        return self._build_or(left_part, right_part)

    # ============================
    # Export
    # ============================
    def export(self, root: int, filename_base: str):
        # 1. Text Export
        with open(f"{filename_base}.txt", "w") as f:
            f.write(f"ROBDD for variables: {self.variable_order}\n")
            f.write(f"Root: {root}\n")
            f.write(f"Total nodes: {len(self.nodes)}\n\n")
            f.write("Node Table:\n")
            for i, node in enumerate(self.nodes):
                if node.is_terminal:
                    f.write(f"  {i}: Terminal({node.value})\n")
                else:
                    f.write(f"  {i}: if {node.var} then {node.high} else {node.low}\n")
        
        # 2. DOT Export
        dot_path = f"{filename_base}.dot"
        with open(dot_path, "w") as f:
            f.write("digraph ROBDD {\n")
            f.write("  rankdir=TB;\n")
            f.write("  node [shape=circle];\n")
            
            # Terminal nodes
            f.write('  0 [label="0", shape=box, style=filled, fillcolor=lightcoral];\n')
            f.write('  1 [label="1", shape=box, style=filled, fillcolor=lightgreen];\n')
            
            visited = set()
            def visit(n_idx):
                if n_idx in visited: return
                visited.add(n_idx)
                node = self.nodes[n_idx]
                if not node.is_terminal:
                    f.write(f'  {n_idx} [label="{node.var}"];\n')
                    f.write(f'  {n_idx} -> {node.low} [label="0", style=dashed, color=red];\n')
                    f.write(f'  {n_idx} -> {node.high} [label="1", style=solid, color=blue];\n')
                    visit(node.low)
                    visit(node.high)
            
            visit(root)
            f.write("}\n")
        
        # 3. Image Generation (Optional)
        if HAS_GRAPHVIZ:
            try:
                src = graphviz.Source.from_file(dot_path)
                src.render(filename_base, format='png', cleanup=True)
                print(f"Generated image: {filename_base}.png")
            except Exception as e:
                print(f"Graphviz installed but failed to render: {e}")
        else:
            print(f"Graphviz not installed. Run manually: dot -Tpng {dot_path} -o {filename_base}.png")

def build_robdd(formula: str, var_order: List[str], output_prefix: str):
    """Main entry point to build and export an ROBDD"""
    robdd = ROBDD(var_order)
    root = robdd.parse_formula(formula)
    robdd.export(root, output_prefix)
    return robdd, root