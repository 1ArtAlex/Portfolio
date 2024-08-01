#include "infix_calculator.h"
#include <gtest/gtest.h>

TEST(CalculatorTest, Addition) {
    InfixCalculator calc("3 + 4");
    EXPECT_EQ(calc.infix_calculate(), 7);
}

TEST(CalculatorTest, Subtraction) {
    InfixCalculator calc("10 - 5");
    EXPECT_EQ(calc.infix_calculate(), 5);
}

TEST(CalculatorTest, Multiplication) {
    InfixCalculator calc("2 * 3");
    EXPECT_EQ(calc.infix_calculate(), 6);
}

TEST(CalculatorTest, Division) {
    InfixCalculator calc("8 / 2");
    EXPECT_EQ(calc.infix_calculate(), 4);
}

TEST(CalculatorTest, Parentheses) {
    InfixCalculator calc("(2 + 3) * 4");
    EXPECT_EQ(calc.infix_calculate(), 20);
}

TEST(CalculatorTest, Priority) {
    InfixCalculator calc("2 + 3 * 4");
    EXPECT_EQ(calc.infix_calculate(), 14);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
