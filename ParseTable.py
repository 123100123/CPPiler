import re
from collections import defaultdict
from tabulate import tabulate

class CFG:
    def __init__(self):
        self.rules = {}
        self.start = "Start"
        self.fill()
        self.first = {}
        self.follow = {}

    def add_production(self, variable, production):
        if variable not in self.rules:
            self.rules[variable] = []

        if isinstance(production, str):
            self.rules[variable].append(production.split())
        elif isinstance(production, list):
            self.rules[variable].extend([p.split() for p in production])

    def display(self):
        for variable, rules in self.rules.items():
            rules_str = " | ".join([" ".join(rule) for rule in rules])

    def fill(self):
        self.add_production("Start", ["S N M"])
        self.add_production("S", ["INCLUDE S", "ε"])
        self.add_production("N", ["using namespace std ;", "ε"])
        self.add_production("M", ["int main ( ) { T V }"])
        self.add_production("T", ["Id T", "Loop T", "Input T", "Output T", "ε"])
        self.add_production("Id", ["int L", "float L"])
        self.add_production("L", ["identifier Assign Z"])
        self.add_production("Assign", ["= Operation", "ε"])
        self.add_production("Z", [";", ", identifier Assign Z"])
        self.add_production("Operation", ["number P", "identifier P"])
        self.add_production("P", ["O W P", "ε"])
        self.add_production("O", ["+", "-", "*"])
        self.add_production("W", ["number", "identifier"])
        self.add_production("Loop", ["while ( Expression ) { T }"])
        self.add_production("Expression", ["Operation K Operation"])
        self.add_production("K", ["==", ">=", "<=", "!="])
        self.add_production("Input", ["cin >> identifier F ;"])
        self.add_production("F", [">> identifier F", "ε"])
        self.add_production("Output", ["cout << C H ;"])
        self.add_production("C", ["\"sum=\"", "number", "string", "identifier"])
        self.add_production("H", ["<< C H", "ε"])
        self.add_production("V", ["return 0 ;", "ε"])

    def calculate_first(self):
        self.first = {non_terminal: set() for non_terminal in self.rules}

        changed = True
        while changed:
            changed = False
            for variable, productions in self.rules.items():
                for production in productions:
                    for symbol in production:
                        if symbol not in self.rules:  # Terminal
                            if symbol not in self.first[variable]:
                                self.first[variable].add(symbol)
                                changed = True
                            break
                        else:  # Non-terminal
                            before = len(self.first[variable])
                            self.first[variable].update(self.first[symbol] - {"ε"})
                            if "ε" in self.first[symbol]:
                                continue
                            after = len(self.first[variable])
                            if before != after:
                                changed = True
                            break
                    else:  # Add epsilon if all symbols allow epsilon
                        if "ε" not in self.first[variable]:
                            self.first[variable].add("ε")
                            changed = True

    def calculate_follow(self):
        self.follow = {non_terminal: set() for non_terminal in self.rules}
        self.follow[self.start].add("$")

        changed = True
        while changed:
            changed = False
            for variable, productions in self.rules.items():
                for production in productions:
                    follow_temp = self.follow[variable].copy()
                    for symbol in reversed(production):
                        if symbol in self.rules:  # Non-terminal
                            before = len(self.follow[symbol])
                            self.follow[symbol].update(follow_temp)
                            after = len(self.follow[symbol])
                            if before != after:
                                changed = True
                            if "ε" in self.first[symbol]:
                                follow_temp.update(self.first[symbol] - {"ε"})
                            else:
                                follow_temp = self.first[symbol].copy()
                        else:  # Terminal
                            follow_temp = {symbol}

    def construct_parse_table(self):
        self.calculate_first()
        self.calculate_follow()

        parse_table = defaultdict(lambda: defaultdict(lambda: []))

        for variable, productions in self.rules.items():
            for production in productions:
                for terminal in self.first_of_sequence(production):
                    if terminal != "ε":
                        parse_table[variable][terminal] = production
                if "ε" in self.first_of_sequence(production):
                    for terminal in self.follow[variable]:
                        parse_table[variable][terminal] = production

        return parse_table

    def first_of_sequence(self, sequence):
        result = set()
        for symbol in sequence:
            if symbol not in self.rules:  # Terminal
                result.add(symbol)
                break
            result.update(self.first[symbol] - {"ε"})
            if "ε" not in self.first[symbol]:
                break
        else:
            result.add("ε")
        return result

cfg = CFG()

parse_table = cfg.construct_parse_table()

# Save parse table to file in the specified format
output_file = "generated_parse_table.txt"
specified_order = ["Start", "S", "N", "M", "T", "Id", "L", "Assign", "Z", "Operation", "P", "O", "W", "Loop", "Expression", "K", "Input", "F", "Output", "C", "H", "V"]
terminals = ["#include", "using", "namespace", "std", ";", "int", "main", "(", ")", "{", "}", "return", "number", "float", "identifier", ",", "+", "-", "*", "=", "==", ">=", "<=", "!=", "while", "cin", ">>", "cout", "<<", "string", "$"]

headers = ["Non-Terminal"] + terminals
rows = []
for nt in specified_order:
    row = [nt] + [f"[{', '.join(parse_table[nt][t])}]" if parse_table[nt][t] else "[]" for t in terminals]
    rows.append(row)

with open(output_file, "w") as f:
    f.write(tabulate(rows, headers=headers, tablefmt="grid"))

print(f"Parse table saved to {output_file}.")

# Function for Non-Recursive Predictive Parsing
def non_recursive_predictive_parse(parse_table, start_symbol, input_tokens):
    stack = ["$"]
    stack.append(start_symbol)
    input_tokens.append("$")  # End marker for input tokens

    productions_used = []
    cursor = 0

    while stack:
        top = stack.pop()
        current_token = input_tokens[cursor]

        if top == "$":
            if current_token == "$":
                return productions_used
            else:
                raise ValueError(f"Unexpected token '{current_token}' at the end of input.")

        elif top == current_token:  # Match terminal
            cursor += 1

        elif top in parse_table:  # Non-terminal
            if current_token in parse_table[top]:
                production = parse_table[top][current_token]
                if production:  # Apply production
                    productions_used.append(f"{top} -> {' '.join(production)}")
                    # Skip epsilon productions
                    if production != ["ε"]:
                        stack.extend(reversed(production))
            else:
                raise ValueError(f"No rule for '{top}' with input '{current_token}' in parse table.")

        else:
            raise ValueError(f"Unexpected symbol '{top}' on stack.")

    if cursor != len(input_tokens) - 1:
        raise ValueError("Input not fully parsed.")

    return productions_used


# Example input tokens
input_tokens = [
    "INCLUDE", "using", "namespace", "std", ";",
    "int", "main", "(", ")", "{",
    "int", "identifier", "=", "number", ";",
    "return", "0", ";", "}"
]

# Perform parsing
try:
    productions = non_recursive_predictive_parse(parse_table, "Start", input_tokens)
    with open("productions_used.txt", "w") as f:
        f.write("\n".join(productions))
    print("Parsing completed. Productions saved to 'productions_used.txt'.")
except ValueError as e:
    print(f"Parsing error: {e}")
