#pragma once

#include <string>
#include "stack.h"

class Calculator {
private:
    std::string expression;

    static float operate(char, float, float);

public:
    explicit Calculator(std::string);

    float calculate();
};
