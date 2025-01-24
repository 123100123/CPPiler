class CFG:
    def __init__(self):
        self.rules = {}
        self.start = "Start"
        self.fill()
        self.first = {}
        pass


    def add_production(self,variable,production):
        if variable not in self.rules:
            self.rules[variable] = []

        if isinstance(production,str):
            self.rules[variable].extend(production.split())
        elif isinstance(production,list):
            self.rules[variable].extend([p.split() for p in production])


    def display(self):
        for variable, rules in self.rules.items():
            rules_str = " | ".join([" ".join(rule) for rule in rules])
            print(f"{variable} -> {rules_str}")


    def fill(self):
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
        

    def calculate_first(self):
        self.first = {non_terminal: set() for non_terminal in self.rules}
        
        changed = True
        while changed:
            changed = False
            for variable, productions in self.rules.items():
                for production in productions:
                    for symbol in production:
                        if symbol not in self.rules:  # reached a terminal
                            if symbol not in self.first[variable]:
                                self.first[variable].add(symbol)
                                changed = True
                            break
                        else:  # reached a variable
                            before = len(self.first[variable])
                            self.first[variable].update(self.first[symbol] - {"ε"})
                            if "ε" in self.first[symbol]:
                                continue
                            after = len(self.first[variable])
                            if before != after:
                                changed = True
                            break
                    else:  # no terminals were found so we have to add ε as an elemnt if the first
                        if "ε" not in self.first[variable]:
                            self.first[variable].add("ε")
                            changed = True


