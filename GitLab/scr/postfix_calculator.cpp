#include "postfix_calculator.h"
#include <utility>

Calculator::Calculator(std::string expr) {
    expression = std::move(expr);
}

float Calculator::operate(char operation, float n1, float n2) {
    switch (operation) {
        case '+':
            return n1 + n2;
        case '-':
            return n1 - n2;
        case '*':
            return n1 * n2;
        case '/':
            if (n2 == 0) throw std::runtime_error("Division by zero");
                return n1 / n2;
        default:
            throw std::invalid_argument("Wrong operation given");
    }
}

float Calculator::calculate() {
    //LinkedList::SinglyLinkedList<float> result = LinkedList::SinglyLinkedList<float>();
    Stack<float> numbers = Stack<float>();
    for (int i = 0; i < expression.length(); i++) {
        if (expression[i] == ' ' || expression[i] == '\n') {
            continue;
        } else if (std::string("-+*/").find(expression[i]) != std::string::npos) {
            if (numbers.size() < 2) {
                throw std::invalid_argument("Expressions contains too many operators");
            }
            float n1 = numbers.pop();
            float n2 = numbers.pop();
            float res = operate(expression[i], n2, n1);
            numbers.push(res);
        } else {
            std::string fullNumber;
            for (int j = i; j < expression.length(); j++) {
                if (std::string("0123456789+-*/. ").find(expression[i]) == std::string::npos) {
                    throw std::invalid_argument("Expression has problems with brackets");
                }
                if (isdigit(expression[j]) || expression[j] == '.') {
                    fullNumber += expression[j];
                } else {
                    i = j;
                    break;
                }
            }
            float n = std::stof(fullNumber);
            numbers.push(n);
        }
    }
    if (numbers.size() != 1) {
        throw std::invalid_argument("Expression contains too many operands");
    }
    float answer = numbers.pop();
    return answer;
}
