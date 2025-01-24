from LexicalAnalyzer import LexicalAnalyzer

analyzer = LexicalAnalyzer()


input_code = """
#include <iostream>
using namespace std;
int main() {
    int x, y = 10;
    while (y > 0) {
        cin >> x;
        y = y - 1;
        cout << "Value: " << x;
    }
    return 0;
}
"""

print(analyzer.analyze(input_code))