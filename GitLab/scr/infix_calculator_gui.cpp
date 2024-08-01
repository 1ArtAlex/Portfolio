#include "infix_calculator_gui.h"

void run() {
    while (true) {
        std::cout << "Enter expression or type EXIT to stop: " << std::endl;
        std::string expr;
        std::getline(std::cin, expr);
        if (expr == "EXIT") {
            break;
        }
        InfixCalculator inf_calc = InfixCalculator(expr);
        try {
            std::cout << inf_calc.infix_calculate() << std::endl;
        }
        catch (std::invalid_argument &e) {
            std::cout << "Oops, something went wrong, try again" << std::endl;
            std::cerr << e.what() << '\n';
        }
    }
}
