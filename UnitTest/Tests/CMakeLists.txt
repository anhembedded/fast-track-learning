# Fetch GoogleTest
include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.14.0
)

# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# Include GoogleTest module
include(GoogleTest)

# Define test executable
add_executable(calculator_tests
    test_calculator.cpp
)

# Link test executable with library and gtest
target_link_libraries(calculator_tests
    PRIVATE
        UnitTest::calculator
        GTest::gtest_main
)

# Compile options
target_compile_options(calculator_tests PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -Wpedantic>
)

# Discover tests
gtest_discover_tests(calculator_tests)
