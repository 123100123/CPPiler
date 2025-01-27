import re

class NonRecursivePredictiveParser:
    def __init__(self, parse_table, start_symbol):
        self.parse_table = parse_table
        self.start_symbol = start_symbol

    def parse(self, input_tokens, output_file="productions_used.txt"):
        # Build a new list of processed tokens
        processed_tokens = []
        for token in input_tokens:
            if isinstance(token, tuple) and token[0] in ["identifier", "number", "string"]:
                processed_tokens.append(token[0])
            elif isinstance(token, tuple):
                processed_tokens.append(token[1])

        print("\After PROCCESSING\n",processed_tokens)
        
        processed_tokens.append("$")

        stack = ["$"]
        stack.append(self.start_symbol)
        cursor = 0

        productions_used = []

        print("\n\nDebugging: Starting Parsing Process\n\n")
        print(f"Initial Stack: {stack}")

        with open(output_file, "w") as f:
            while stack:
                top = stack.pop()
                current_token = processed_tokens[cursor]

                print(f"Top of Stack: {top}")
                print(f"Current Token: {current_token}")
                print(f"Stack after popping: {stack}\n")

                if top == "$":
                    if current_token == "$":
                        # Successfully parsed all input
                        print(f"Parsing completed. Productions saved to '{output_file}'.")
                        return productions_used
                    else:
                        raise ValueError(f"Unexpected token '{current_token}' at the end of input.")

                elif top == current_token:  # Match simple terminal (non-tuple token)
                    print(f"Matched terminal: {top} with input token: {current_token}\n")
                    cursor += 1
                
                elif top in self.parse_table:  # Non-terminal match
                    # Handle non-terminals and apply a production rule
                    token_key = current_token[0] if isinstance(current_token, tuple) else current_token
                    if token_key in self.parse_table[top]:
                        production = self.parse_table[top][token_key]
                        
                        print("\n TOKEN KEY:",token_key)
                        print("\n PROODUCTION:",production)
                        print("\n CURRENT TOKEN:",current_token)
                        
                        print()
                        if (len(production) == 1) and (current_token in ["identifier", "number", "string"]) and (token_key in production):
                            production = current_token[1]
                        
                        f.write(f"{top} -> {' '.join(production)}\n")  # Write transition in specified format
                        
                        production = self.parse_table[top][token_key]
                        
                        # Continuing the Productions as usual
                        productions_used.append(f"{top} -> {' '.join(production)}")
                        print(f"Applied Production: {top} -> {' '.join(production)}\n")
                       
                        # Handle epsilon productions (skip adding to stack)
                        if production != ["ε"]:
                            stack.extend(reversed(production))
                            print(f"Updated Stack after production: {stack}\n")
                    else:
                        raise ValueError(f"No rule for '{top}' with input '{token_key}' in parse table.")

                else:
                    raise ValueError(f"Unexpected symbol '{top}' on stack.")

            if cursor != len(processed_tokens) - 1:
                raise ValueError("Input not fully parsed.")

        return productions_used
