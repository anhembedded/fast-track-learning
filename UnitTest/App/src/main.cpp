#include "calculator/calculator.h"
#include <iomanip>
#include <iostream>


int main() {
  calculator::Calculator calc;

  std::cout << "=== Calculator Demo Application ===" << std::endl;
  std::cout << std::endl;

  // Basic operations
  std::cout << "Basic Operations:" << std::endl;
  std::cout << "  10 + 5 = " << calc.add(10, 5) << std::endl;
  std::cout << "  10 - 5 = " << calc.subtract(10, 5) << std::endl;
  std::cout << "  10 * 5 = " << calc.multiply(10, 5) << std::endl;
  std::cout << "  10 / 5 = " << std::fixed << std::setprecision(2)
            << calc.divide(10, 5) << std::endl;
  std::cout << std::endl;

  // Advanced operations
  std::cout << "Advanced Operations:" << std::endl;
  std::cout << "  2^8 = " << calc.power(2, 8) << std::endl;
  std::cout << "  5! = " << calc.factorial(5) << std::endl;
  std::cout << "  17 % 5 = " << calc.modulo(17, 5) << std::endl;
  std::cout << "  gcd(48, 18) = " << calc.gcd(48, 18) << std::endl;
  std::cout << "  lcm(12, 18) = " << calc.lcm(12, 18) << std::endl;
  std::cout << "  isPrime(29) = " << (calc.isPrime(29) ? "true" : "false")
            << std::endl;
  std::cout << std::endl;

  // Error handling demonstration
  std::cout << "Error Handling:" << std::endl;
  try {
    std::cout << "  Attempting division by zero..." << std::endl;
    calc.divide(10, 0);
  } catch (const std::invalid_argument &e) {
    std::cout << "  Caught exception: " << e.what() << std::endl;
  }

  try {
    std::cout << "  Attempting factorial of negative number..." << std::endl;
    calc.factorial(-5);
  } catch (const std::invalid_argument &e) {
    std::cout << "  Caught exception: " << e.what() << std::endl;
  }

  try {
    std::cout << "  Attempting modulo by zero..." << std::endl;
    calc.modulo(10, 0);
  } catch (const std::invalid_argument &e) {
    std::cout << "  Caught exception: " << e.what() << std::endl;
  }

  std::cout << std::endl;
  std::cout << "=== Demo Complete ===" << std::endl;

  return 0;
}
