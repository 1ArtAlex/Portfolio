#pragma once

#include "postfix_calculator.h"
#include "queue.h"

class InfixCalculator {
private:
    std::string expression;

    static std::string convert(std::string expr);

    static int priority(char c);

public:
    explicit InfixCalculator(std::string);

    float infix_calculate();
};
