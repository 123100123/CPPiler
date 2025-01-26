import re

class NonRecursivePredictiveParser:
    def __init__(self, parse_table, start_symbol):
        self.parse_table = parse_table
        self.start_symbol = start_symbol

    def parse(self, input_tokens, output_file="productions_used.txt"):
        stack = ["$"]
        stack.append(self.start_symbol)
        input_tokens.append("$")  # Add end marker to input tokens

        productions_used = []
        cursor = 0

        with open(output_file, "w") as f:
            while stack:
                top = stack.pop()
                current_token = input_tokens[cursor]

                if top == "$":
                    if current_token == "$":
                        # Successfully parsed all input
                        print(f"Parsing completed.Productions saved to '{output_file}'.")
                        return productions_used
                    else:
                        raise ValueError(f"Unexpected token '{current_token}' at the end of input.")

                elif top == current_token:  # Terminal match
                    cursor += 1

                elif top in self.parse_table:  # Non-terminal match
                    if current_token in self.parse_table[top]:
                        production = self.parse_table[top][current_token]
                        f.write(f"{top} -> {' '.join(production)}\n")  # Write transition in specified format
                        productions_used.append(f"{top} -> {' '.join(production)}")
                        # Handle epsilon productions (skip adding to stack)
                        if production != ["ε"]:
                            stack.extend(reversed(production))
                    else:
                        raise ValueError(f"No rule for '{top}' with input '{current_token}' in parse table.")

                else:
                    raise ValueError(f"Unexpected symbol '{top}' on stack.")

            if cursor != len(input_tokens) - 1:
                raise ValueError("Input not fully parsed.")

        return productions_used
