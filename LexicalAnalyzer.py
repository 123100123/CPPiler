import re

class LexicalAnalyzer:
    token_patterns = [
        # Reserved words (including #include, using, namespace, std, etc.)
        (r"\b(?:int|float|void|return|if|while|cin|cout|continue|break|using|namespace|std|main)\b", "RESERVEDWORD"),
        
        # Include directive (capture #include but ignore content in <> or "")
        (r"#include\b", "RESERVEDWORD"),
        
        # Strings (anything between quotation marks)
        (r'\".*?\"', "STRING"),
        
        # Identifiers (letters followed by letters or digits)
        (r"[a-zA-Z][a-zA-Z0-9]*", "IDENTIFIER"),
        
        # Numbers (one or more digits)
        (r"[0-9]+", "NUMBER"),
        
        # Symbols (single and multi-character operators)
        (r"\+\+|--|\+=|-=|\*=|/=|==|!=|>=|<=|&&|\|\||<<|>>", "SYMBOL"),
        (r"[+\-*/=><!&|;,:\[\]{}()\|]", "SYMBOL"),
    ]

    def __init__(self):
        self.compiled_patterns = self.compile_patterns()

    def compile_patterns(self):
        return [(re.compile(pattern), token_type) for pattern, token_type in self.token_patterns]

    def analyze(self, line):
        tokens = []
        position = 0

        while position < len(line):
            match = None
            for token_compiler, token_type in self.compiled_patterns:
                match = token_compiler.match(line, position)
                if match:
                    lexeme = match.group(0)

                    # Store both the token type and its value
                    if token_type == "IDENTIFIER":
                        tokens.append((token_type.lower(), lexeme))
                    elif token_type == "NUMBER":
                        tokens.append((token_type.lower(), int(lexeme)))
                    elif token_type == "STRING":
                        tokens.append((token_type.lower(), lexeme)) 
                    else:
                        tokens.append((token_type, lexeme))

                    position = match.end()
                    break

            if not match:
                if line[position].isspace():
                    position += 1  # Skip whitespace
                else:
                    raise ValueError(f"Unexpected character: {line[position]}")

        return tokens

    def get_tokens(self, code):
        tokens = []
        for line in code.split("\n"):
            # Replace entire #include line with just #include
            line = re.sub(r'#include\s*[<"].*?[>"]', '#include', line)
            tokens.extend(self.analyze(line))
        return tokens
