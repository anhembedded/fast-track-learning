# CMake Quick Reference Guide

## Common Build Commands

### Initial Configuration
```powershell
# Create build directory
mkdir build -Force
cd build

# Configure with default generator
cmake ..

# Configure with specific generator
cmake .. -G "MinGW Makefiles"
cmake .. -G "Ninja"
cmake .. -G "Visual Studio 17 2022"

# Configure with build type
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake .. -DCMAKE_BUILD_TYPE=Debug
```

### Building
```powershell
# Build all targets
cmake --build .

# Build specific target
cmake --build . --target calculator
cmake --build . --target calculator_tests

# Build with specific configuration (for multi-config generators)
cmake --build . --config Release

# Parallel build
cmake --build . -j 8
```

### Testing
```powershell
# Run all tests
ctest

# Run tests with output on failure
ctest --output-on-failure

# Run tests verbosely
ctest -V

# Run specific test
ctest -R CalculatorTest.AddPositiveNumbers

# Run tests in parallel
ctest -j 8
```

### Cleaning
```powershell
# Clean build artifacts
cmake --build . --target clean

# Complete clean (remove build directory)
cd ..
Remove-Item -Path build -Recurse -Force
```

## Project-Specific Options

### Build Options
```powershell
# Disable tests
cmake .. -DBUILD_TESTS=OFF

# Enable shared libraries
cmake .. -DBUILD_SHARED_LIBS=ON

# Combine options
cmake .. -DBUILD_TESTS=ON -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Release
```

## Useful CMake Commands

### Information
```powershell
# List available generators
cmake --help

# Show CMake version
cmake --version

# Show cache variables
cmake -L

# Show cache variables with help
cmake -LH
```

### Reconfiguration
```powershell
# Reconfigure (from build directory)
cmake ..

# Force reconfigure
cmake .. --fresh
```

## Directory Structure After Build

```
build/
├── bin/                        # Executables
│   ├── calculator.exe         # Main application
│   └── calculator_tests.exe   # Test executable
├── lib/                        # Libraries
│   ├── libcalculator.a        # Calculator library
│   ├── libgtest.a             # GoogleTest library
│   └── libgtest_main.a        # GoogleTest main
└── CMakeFiles/                 # CMake internal files
```

## Workflow Examples

### Development Workflow
```powershell
# 1. Make code changes
# 2. Build
cmake --build build

# 3. Run tests
ctest --test-dir build --output-on-failure

# 4. Run application
.\build\bin\calculator.exe
```

### Clean Build
```powershell
# Remove old build
Remove-Item -Path build -Recurse -Force

# Fresh configure and build
mkdir build -Force
cd build
cmake ..
cmake --build .
ctest --output-on-failure
```

### Release Build
```powershell
mkdir build-release -Force
cd build-release
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

## Troubleshooting

### Generator Mismatch
If you see "Does not match the generator used previously":
```powershell
# Clean the build directory
Remove-Item -Path build/* -Recurse -Force
# Or create a new build directory
mkdir build-new
```

### Compiler Not Found
```powershell
# Specify compiler explicitly
cmake .. -DCMAKE_CXX_COMPILER=g++
cmake .. -DCMAKE_CXX_COMPILER=clang++
```

### Cache Issues
```powershell
# Remove CMake cache
Remove-Item build/CMakeCache.txt
Remove-Item -Path build/CMakeFiles -Recurse -Force
cmake build
```

## Best Practices

1. **Always use out-of-source builds** (build directory separate from source)
2. **Use `cmake --build .`** instead of calling make/ninja directly
3. **Use `ctest`** instead of running test executables directly
4. **Keep build directories in .gitignore**
5. **Use CMake presets** for complex configurations (CMakePresets.json)
6. **Run tests after every build** to catch regressions early
