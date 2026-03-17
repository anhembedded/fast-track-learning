#include "calculator/calculator.h"
#include <gtest/gtest.h>


// Test fixture for Calculator tests
class CalculatorTest : public ::testing::Test {
protected:
  calculator::Calculator calc;
};

// ========== Basic Operations Tests ==========

TEST_F(CalculatorTest, AddPositiveNumbers) {
  EXPECT_EQ(calc.add(5, 3), 8);
  EXPECT_EQ(calc.add(10, 20), 30);
}

TEST_F(CalculatorTest, AddNegativeNumbers) {
  EXPECT_EQ(calc.add(-5, -3), -8);
  EXPECT_EQ(calc.add(-10, 5), -5);
}

TEST_F(CalculatorTest, AddZero) {
  EXPECT_EQ(calc.add(0, 0), 0);
  EXPECT_EQ(calc.add(5, 0), 5);
  EXPECT_EQ(calc.add(0, 5), 5);
}

TEST_F(CalculatorTest, SubtractPositiveNumbers) {
  EXPECT_EQ(calc.subtract(10, 5), 5);
  EXPECT_EQ(calc.subtract(20, 15), 5);
}

TEST_F(CalculatorTest, SubtractNegativeNumbers) {
  EXPECT_EQ(calc.subtract(-5, -3), -2);
  EXPECT_EQ(calc.subtract(5, -3), 8);
}

TEST_F(CalculatorTest, MultiplyPositiveNumbers) {
  EXPECT_EQ(calc.multiply(5, 3), 15);
  EXPECT_EQ(calc.multiply(10, 10), 100);
}

TEST_F(CalculatorTest, MultiplyByZero) {
  EXPECT_EQ(calc.multiply(5, 0), 0);
  EXPECT_EQ(calc.multiply(0, 5), 0);
}

TEST_F(CalculatorTest, MultiplyNegativeNumbers) {
  EXPECT_EQ(calc.multiply(-5, 3), -15);
  EXPECT_EQ(calc.multiply(-5, -3), 15);
}

TEST_F(CalculatorTest, DividePositiveNumbers) {
  EXPECT_DOUBLE_EQ(calc.divide(10, 5), 2.0);
  EXPECT_DOUBLE_EQ(calc.divide(15, 3), 5.0);
}

TEST_F(CalculatorTest, DivideWithRemainder) {
  EXPECT_DOUBLE_EQ(calc.divide(10, 3), 10.0 / 3.0);
  EXPECT_DOUBLE_EQ(calc.divide(7, 2), 3.5);
}

TEST_F(CalculatorTest, DivideByZeroThrowsException) {
  EXPECT_THROW(calc.divide(10, 0), std::invalid_argument);
  EXPECT_THROW(calc.divide(-5, 0), std::invalid_argument);
}

// ========== Advanced Operations Tests ==========

TEST_F(CalculatorTest, PowerPositiveExponent) {
  EXPECT_EQ(calc.power(2, 3), 8);
  EXPECT_EQ(calc.power(5, 2), 25);
  EXPECT_EQ(calc.power(10, 0), 1);
}

TEST_F(CalculatorTest, PowerZeroBase) {
  EXPECT_EQ(calc.power(0, 5), 0);
  EXPECT_EQ(calc.power(0, 0), 1);
}

TEST_F(CalculatorTest, PowerNegativeBase) {
  EXPECT_EQ(calc.power(-2, 3), -8);
  EXPECT_EQ(calc.power(-2, 2), 4);
}

TEST_F(CalculatorTest, PowerNegativeExponentThrowsException) {
  EXPECT_THROW(calc.power(2, -3), std::invalid_argument);
}

TEST_F(CalculatorTest, FactorialPositiveNumbers) {
  EXPECT_EQ(calc.factorial(0), 1);
  EXPECT_EQ(calc.factorial(1), 1);
  EXPECT_EQ(calc.factorial(5), 120);
  EXPECT_EQ(calc.factorial(6), 720);
}

TEST_F(CalculatorTest, FactorialNegativeNumberThrowsException) {
  EXPECT_THROW(calc.factorial(-1), std::invalid_argument);
  EXPECT_THROW(calc.factorial(-5), std::invalid_argument);
}

TEST_F(CalculatorTest, ModuloBasicCases) {
  EXPECT_EQ(calc.modulo(17, 5), 2);
  EXPECT_EQ(calc.modulo(20, 4), 0);
}

TEST_F(CalculatorTest, ModuloWithNegativeNumbers) {
  EXPECT_EQ(calc.modulo(-17, 5), -2);
  EXPECT_EQ(calc.modulo(17, -5), 2);
}

TEST_F(CalculatorTest, ModuloByZeroThrowsException) {
  EXPECT_THROW(calc.modulo(10, 0), std::invalid_argument);
}

TEST_F(CalculatorTest, GcdBasicCases) {
  EXPECT_EQ(calc.gcd(48, 18), 6);
  EXPECT_EQ(calc.gcd(7, 13), 1);
}

TEST_F(CalculatorTest, GcdHandlesZeroAndNegativeValues) {
  EXPECT_EQ(calc.gcd(0, 10), 10);
  EXPECT_EQ(calc.gcd(-48, 18), 6);
  EXPECT_EQ(calc.gcd(-48, -18), 6);
}

TEST_F(CalculatorTest, LcmBasicCases) {
  EXPECT_EQ(calc.lcm(12, 18), 36);
  EXPECT_EQ(calc.lcm(7, 13), 91);
}

TEST_F(CalculatorTest, LcmHandlesZeroAndNegativeValues) {
  EXPECT_EQ(calc.lcm(0, 10), 0);
  EXPECT_EQ(calc.lcm(-12, 18), 36);
}

TEST_F(CalculatorTest, IsPrimeBasicCases) {
  EXPECT_TRUE(calc.isPrime(2));
  EXPECT_TRUE(calc.isPrime(3));
  EXPECT_TRUE(calc.isPrime(29));
}

TEST_F(CalculatorTest, IsPrimeNonPrimeCases) {
  EXPECT_FALSE(calc.isPrime(-7));
  EXPECT_FALSE(calc.isPrime(0));
  EXPECT_FALSE(calc.isPrime(1));
  EXPECT_FALSE(calc.isPrime(9));
  EXPECT_FALSE(calc.isPrime(100));
}

// ========== Edge Cases Tests ==========

TEST_F(CalculatorTest, LargeNumbers) {
  EXPECT_EQ(calc.add(1000000, 2000000), 3000000);
  EXPECT_EQ(calc.multiply(1000, 1000), 1000000);
}

TEST_F(CalculatorTest, ChainedOperations) {
  int result = calc.add(10, 5);
  result = calc.multiply(result, 2);
  result = calc.subtract(result, 10);
  EXPECT_EQ(result, 20);
}

// Main function to run all tests
int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
