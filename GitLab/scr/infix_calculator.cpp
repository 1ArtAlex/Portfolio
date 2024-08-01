#include "infix_calculator.h"

#include <utility>

InfixCalculator::InfixCalculator(std::string expr) {
    expression = std::move(expr);
}


float InfixCalculator::infix_calculate() {
    std::string expr = convert(expression);
    Calculator calc = Calculator(expr);
    return calc.calculate();
}

// returns priority of operators
int InfixCalculator::priority(char c) {
    switch (c) {
        case '*':
        case '/':
            return 3;
        case '+':
        case '-':
            return 2;
        case '(':
            return 1;
        default:
            return -1;
    }
}

std::string InfixCalculator::convert(std::string expr) {
    Stack s = Stack<char>();
    Queue q = Queue<std::string>();

    for (int i = 0; i < expr.length(); i++) {
        // empty chars should be skipped
        if (expr[i] == ' ') {
            continue;
        }
        // if operator was met
        if ((std::string("-+*/").find(expr[i]) != std::string::npos)) {
            if (s.isEmpty() || s.peek() == '(') {
                s.push(expr[i]);
                continue;
            }
            if (priority(expr[i]) > priority(s.peek())) {
                s.push(expr[i]);
            } else {
                while (!s.isEmpty() && priority(expr[i]) <= priority(s.peek()) && s.peek() != '(') {
                    q.enqueue(std::string(1, s.pop()));
                }

                s.push(expr[i]);
            }
        } else if (expr[i] == '(') {
            s.push(expr[i]);
        } else if (expr[i] == ')') {
            if (!s.isEmpty()) {
                while (s.peek() != '(') {
                    q.enqueue(std::string(1, s.pop()));
                }
                s.pop();
            } else {
                throw std::invalid_argument("Expression has problems with brackets");
            }
        } else {
            std::string fullNumber;
            for (int j = i; j < expr.length(); j++) {
                if (std::string("0123456789+-*/.() ").find(expr[j]) == std::string::npos) {
                    throw std::invalid_argument("Expression contains invalid characters");
                }
                if (isdigit(expr[j]) || expr[j] == '.') {
                    fullNumber += expr[j];
                } else {
                    i = j - 1;
                    break;
                }
                if (j == expr.length() - 1) {
                    i = j;
                }
            }
            q.enqueue(fullNumber);
        }
    }

    while (!s.isEmpty()) {
        q.enqueue(std::string(1, s.pop()));
    }

    // convert queue to string
    std::string result;
    int q_size = q.size();
    for (int i = 0; i < q_size; i++) {
        result += q.dequeue() + " ";
    }

    return result;
}
