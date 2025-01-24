class CFG:
    def __init__(self):
        self.rules = {}
        self.start = "Start"
        self.fill()
        pass


    def add_production(self,variable,production):
        if variable not in self.rules:
            self.rules[variable] = []

        if isinstance(production,str):
            self.rules[variable].extend(production.split())
        elif isinstance(production,list):
            self.productions[variable].extend([p.split() for p in production])


    def display(self):
        for variable, rules in self.productions.items():
            rules_str = " | ".join([" ".join(rule) for rule in rules])
            print(f"{variable} -> {rules_str}")


    def fill(self):
        self.set_start_symbol("Start")
        self.add_production("Start", ["S N M"])
        self.add_production("S", ["#include S", "ε"])
        self.add_production("N", ["using namespace std ;", "ε"])
        self.add_production("M", ["int main ( ) { T V }"])
        self.add_production("T", ["Id T", "Loop T", "Input T", "Output T", "ε"])
        self.add_production("Id", ["int L", "float L"])
        self.add_production("L", ["identifier Assign Z"])
        self.add_production("Assign", ["= Operation", "ε"])
        self.add_production("Z", [";"])
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
        self.add_production("C", ['"sum="', "number", "string", "identifier"])
        self.add_production("H", ["<< C H", "ε"])
        self.add_production("V", ["return 0 ;", "ε"])
    