from LexicalAnalyzer import LexicalAnalyzer
from ParseTable import CFG, ParseTable
from NonRecursivePredictiveParser import NonRecursivePredictiveParser
from ParseTree import ParseTree

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

# Lexical Analysis
analyzer = LexicalAnalyzer(input_code)

if analyzer.semicolon_errors:
    print("missing semicolon, line: ",end=" ")
    print(*analyzer.semicolon_errors,sep=", ")

if analyzer.wrong_allocations:
    print(*analyzer.wrong_allocations,sep="\n")

if analyzer.wrong_allocations or analyzer.semicolon_errors:
    exit()
else:
    print("No errors found!")

tokens = analyzer.tokens

# Construct CFG and Parse Table
cfg = CFG()
parse_table_generator = ParseTable(cfg)
parse_table = parse_table_generator.construct_parse_table()

# Save the generated parse table to a file
output_file = 'generated_parse_table.txt'
specified_order = ['Start', 'S', 'N', 'M', 'T', 'V', 'Id', 'L', 'Z', 'Operation', 'P', 'O', 'W', 'Assign', 'Expression', 'K', 'Loop', 'Input', 'F', 'Output', 'H', 'C']
terminals = ['#include', 'using', 'namespace', 'std', ';', 'int', 'main', '(', ')', '{', '}', 'return', 'number', 'float', 'identifier', ',', '+', '-', '*', '=', '==', '>=', '<=', '!=', 'while', 'cin', '>>', 'cout', '<<', 'string', '$']

parse_table_generator.save_to_file(output_file, specified_order, terminals)

# Non-Recursive Predictive Parsing
parser = NonRecursivePredictiveParser(parse_table, "Start")
productions_used = parser.parse(tokens, output_file="productions_used.txt")

# Build and Display Parse Tree
parse_tree = ParseTree("Start")
parse_tree.build_from_productions(productions_used,specified_order+["identifier" , "string" , "number"])
parse_tree.visualize(output_file="parse_tree", format="png")