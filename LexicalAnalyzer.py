import re

class LexicalAnalyzer:
    token_patterns = [                  # re patterns for the analyze
    (r"[a-zA-Z_][a-zA-Z0-9_]*", "IDENTIFIER"),  
    (r"\d+", "NUMBER"),                         
    (r"\+\+|--|\+=|-=|\*=|/=|==|!=|>=|<=|&&|\|\|", "OPERATOR"),  
    (r"[+\-*/=><!&|;,\[\]{}()]", "SYMBOL"),     
    (r"\".*?\"", "STRING"),                     
    (r"#include|int|float|void|return|if|while|cin|cout|continue|break|using|namespace|std|main", "RESERVEDWORD"),  
    ]

    def __init__(self):
        self.compiled_patterns = self.compile_patterns()

    def compile_patterns(self): # creates an re compiler for each pattern, adding it to a list along with the pattern itself
        compiled_patterns = [(re.compile(token),case) for token, case in self.token_patterns]
        return compiled_patterns

    def analyze(self,line): # Returns the tokens of each input line 
        tokens = []
        position = 0

        while position < len(line):
            match = None
            for token_compiler, token in self.compiled_patterns:
                match = token_compiler.match(line,position)

                if match:
                    lexeme = match.group(0)
                    tokens.append((token,lexeme))
                    position = match.end()
                    break
            
            if not match:
                if line[position].isspace():
                    position += 1
        
        return tokens
                    

    def get_tokens(self,code:str): # line by line checking of tokens 
        tokens = []
        for line in code.split("\n"):
            res = self.analyze(line)
            
            tokens.extend(res)
        
        return tokens

