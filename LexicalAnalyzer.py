import re

class LexicalAnalyzer:
    token_patterns = [
        # Reserved words (including #include, using, namespace, std, etc.)
        (r"\b(?:int|float|void|return|if|while|cin|cout|continue|break|include|using|namespace|std|main)\b", "RESERVEDWORD"),

        # Include directive (ignore anything after #include)
        (r"#include.*", "INCLUDE"),

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

                    if token_type == "INCLUDE":
                        tokens.append("#include")  # Ignore anything after #include
                    elif token_type == "IDENTIFIER":
                        tokens.append("identifier")
                    elif token_type == "NUMBER":
                        tokens.append("number")
                    elif token_type == "STRING":
                        tokens.append("string")
                    else:
                        tokens.append(lexeme)

                    position = match.end()
                    break

            if not match:
                if line[position].isspace():
                    position += 1  # Skip whitespace
                else:
                    raise ValueError(f"Unexpected character: {line[position]}")

        return tokens

    def missing_semicolon(self, line: str) -> bool:
        line = line.strip()

        if not line:
            return False

        exceptions = [
            "if", "else", "while", "for", "switch", "case", "default",
            "{", "}",
            "#include"
        ]

        for exception in exceptions:
            if line.startswith(exception):
                return False

        if "(" in line and ")" in line:
            return False

        if line.endswith(";"):
            return False

        return True
    

    def get_tokens(self, code):
        tokens = []
        missing_semicolon_lines = []
        
        for _,line in enumerate(code.split("\n")):
            if self.missing_semicolon(line):
                missing_semicolon_lines.append(_+1)

            tokens.extend(self.analyze(line))
        
        self.tokens = tokens
        self.semicolon_errors = missing_semicolon_lines

        return tokens

