# UnitTest Project

A modern CMake project demonstrating best practices for organizing C++ applications with libraries and unit tests.

## Project Structure

```
UnitTest/
├── CMakeLists.txt              # Root CMake configuration
├── lib/                        # Calculator library (business logic)
│   ├── CMakeLists.txt
│   ├── include/
│   │   └── calculator/
│   │       └── calculator.h
│   └── src/
│       └── calculator.cpp
├── App/                        # Application executable
│   ├── CMakeLists.txt
│   └── src/
│       └── main.cpp
├── Tests/                      # Unit tests
│   ├── CMakeLists.txt
│   └── test_calculator.cpp
└── build/                      # Build directory (gitignored)
```

## Features

- **Modern CMake (3.14+)**: Uses modern CMake practices with target-based configuration
- **Separation of Concerns**: Library code separated from application code
- **Comprehensive Testing**: GoogleTest integration with automatic test discovery
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Configurable Build**: Options for tests and library type (shared/static)

## Building the Project

### Prerequisites

- CMake 3.14 or higher
- C++17 compatible compiler (MSVC, GCC, Clang)
- Internet connection (for downloading GoogleTest)

### Build Commands

#### Windows (PowerShell)

```powershell
# Create and navigate to build directory
mkdir build -Force
cd build

# Configure the project
cmake ..

# Build the project
cmake --build .

# Run tests
ctest --output-on-failure

# Run the application
.\bin\calculator.exe
```

#### Linux/macOS

```bash
# Create and navigate to build directory
mkdir -p build
cd build

# Configure the project
cmake ..

# Build the project
cmake --build .

# Run tests
ctest --output-on-failure

# Run the application
./bin/calculator
```

## Build Options

- `BUILD_TESTS`: Enable/disable building tests (default: ON)
  ```bash
  cmake .. -DBUILD_TESTS=OFF
  ```

- `BUILD_SHARED_LIBS`: Build shared libraries instead of static (default: OFF)
  ```bash
  cmake .. -DBUILD_SHARED_LIBS=ON
  ```

- `CMAKE_BUILD_TYPE`: Set build type (Debug/Release)
  ```bash
  cmake .. -DCMAKE_BUILD_TYPE=Release
  ```

## Project Components

### Library (`lib/`)

The calculator library contains the core business logic:
- Basic operations: add, subtract, multiply, divide
- Advanced operations: power, factorial
- Error handling for invalid inputs

### Application (`App/`)

A demonstration application that uses the calculator library to showcase its functionality.

### Tests (`Tests/`)

Comprehensive unit tests using GoogleTest:
- 20+ test cases
- Coverage of all library functions
- Edge case testing
- Exception handling verification

## CMake Best Practices Demonstrated

1. **Target-based Configuration**: Uses `target_*` commands instead of global variables
2. **Modern Target Properties**: Proper use of `PUBLIC`, `PRIVATE`, `INTERFACE`
3. **Generator Expressions**: For build/install interface separation
4. **Alias Targets**: Consistent naming with `UnitTest::calculator`
5. **Organized Output**: Separate directories for binaries and libraries
6. **Conditional Building**: Optional test building
7. **Automatic Test Discovery**: Using `gtest_discover_tests()`
8. **Cross-platform Compiler Warnings**: Using generator expressions

## Running Tests

After building, you can run tests in several ways:

```bash
# Run all tests
ctest

# Run tests with verbose output
ctest --output-on-failure

# Run tests with extra verbosity
ctest -V

# Run specific test
ctest -R CalculatorTest
```

## Adding New Features

### Adding a New Function to the Library

1. Add declaration in `lib/include/calculator/calculator.h`
2. Add implementation in `lib/src/calculator.cpp`
3. Add tests in `Tests/test_calculator.cpp`
4. Rebuild and run tests

### Adding a New Test File

1. Create new test file in `Tests/`
2. Add to `Tests/CMakeLists.txt`:
   ```cmake
   target_sources(calculator_tests PRIVATE new_test.cpp)
   ```

## License

This is a demonstration project for educational purposes.
