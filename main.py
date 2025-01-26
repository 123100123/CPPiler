from LexicalAnalyzer import LexicalAnalyzer
from ParseTable import CFG, ParseTable
from NonRecursivePredictiveParser import NonRecursivePredictiveParser

# Input code to be tested
input_code = '''
#include <iostream>
using namespace std;
int main(){
    int x;
    int s=0, t=10;
    while (t >= 0){
        cin>>x;
        t = t - 1;
        s = s + x;
    }
    cout<<"sum="<<s;
    return 0;
}
'''

# Step 1: Lexical Analysis
print('Step 1: Lexical Analysis')
analyzer = LexicalAnalyzer()
tokens = analyzer.get_tokens(input_code)  # Retrieve tokens directly as lexemes
print('Generated Tokens:', tokens)

# Step 2: Construct CFG and Parse Table
print('\nStep 2: Constructing CFG and Parse Table')
cfg = CFG()
parse_table_generator = ParseTable(cfg)
parse_table = parse_table_generator.construct_parse_table()

# Save the generated parse table to a file
output_file = 'generated_parse_table.txt'
specified_order = ['Start', 'S', 'N', 'M', 'T', 'V', 'Id', 'L', 'Z', 'Operation', 'P', 'O', 'W', 'Assign', 'Expression', 'K', 'Loop', 'Input', 'F', 'Output', 'H', 'C']
terminals = ['#include', 'using', 'namespace', 'std', ';', 'int', 'main', '(', ')', '{', '}', 'return', 'number', 'float', 'identifier', ',', '+', '-', '*', '=', '==', '>=', '<=', '!=', 'while', 'cin', '>>', 'cout', '<<', 'string', '$']

parse_table_generator.save_to_file(output_file, specified_order, terminals)

# Step 3: Non-Recursive Predictive Parsing
print('\nStep 3: Parsing the input tokens using Non-Recursive Predictive Parser')
parser = NonRecursivePredictiveParser(parse_table, "Start")
try:
    productions_used = parser.parse(tokens, output_file="productions_used.txt")
    print("Parsing completed successfully. Productions saved to 'productions_used.txt'.")
except ValueError as e:
    print(f"Parsing error: {e}")
