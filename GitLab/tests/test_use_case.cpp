#include "infix_calculator.h"
#include <gtest/gtest.h>

TEST(UseCaseTest, ComplexExpression) {
    InfixCalculator calc("(1 + 2) * (3 + 4) - 5 / (6 - 1)");
    EXPECT_EQ(calc.infix_calculate(), 20.0);
}


TEST(UseCaseTest, LongExpression) {
    InfixCalculator calc("2 + 3 * 4 - 5 / (6 - 1) + (7 - 3) * 2");
    EXPECT_EQ(calc.infix_calculate(), 21.0);
}

TEST(UseCaseTest, AllOperations) {
    InfixCalculator calc("5 + 3 * (8 - 6) / 2 - 4");
    EXPECT_EQ(calc.infix_calculate(), 4.0);
}

TEST(UseCaseTest, NestedParentheses) {
    InfixCalculator calc("((1 + 4) * (3 + 4)) / (2 + 3)");
    EXPECT_EQ(calc.infix_calculate(), 7);
}

TEST(UseCaseTest, ZeroDivision) {
    InfixCalculator calc("4 / (2 - 2)");
    try {
        calc.infix_calculate();
        FAIL() << "Expected std::runtime_error";
    } catch (const std::runtime_error& err) {
        EXPECT_EQ(err.what(), std::string("Division by zero"));
    } catch (...) {
        FAIL() << "Expected std::runtime_error";
    }
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
