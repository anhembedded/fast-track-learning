# IntelliSense Configuration Guide

## Vấn đề đã được Fix

Trước đây, IntelliSense báo lỗi `'calculator/calculator.h' file not found` mặc dù project build thành công. Đây là do IntelliSense chưa được cấu hình đúng để hiểu cấu trúc CMake project.

## Giải pháp đã áp dụng

### 1. **compile_commands.json**
- File này chứa tất cả compile commands cho mọi file trong project
- CMake tự động generate khi configure với flag `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON`
- IntelliSense đọc file này để hiểu include paths, defines, và compiler flags

### 2. **VSCode Configuration**
Đã tạo 2 files trong `.vscode/`:

#### `.vscode/c_cpp_properties.json`
- Cấu hình C++ IntelliSense
- Chỉ định sử dụng `compile_commands.json`
- Set C++ standard là C++17

#### `.vscode/settings.json`
- Tự động configure CMake khi mở project
- Luôn export `compile_commands.json` khi configure
- Sử dụng CMake Tools làm configuration provider

### 3. **Build Script**
File `build.ps1` tự động:
- Configure CMake với compile commands export
- Copy `compile_commands.json` về root directory
- Build project

## Cách sử dụng

### Lần đầu setup hoặc sau khi thay đổi CMakeLists.txt:
```powershell
.\build.ps1
```

### Hoặc thủ công:
```powershell
# Configure
cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

# Copy compile_commands.json
Copy-Item build\compile_commands.json .

# Build
cmake --build build
```

### Reload IntelliSense trong VSCode:
1. Nhấn `Ctrl+Shift+P`
2. Gõ "C/C++: Reload IntelliSense Database"
3. Hoặc đơn giản là reload window: "Developer: Reload Window"

## Tại sao cần compile_commands.json?

CMake là build system generator - nó không trực tiếp compile code mà tạo ra build files (Makefiles, Visual Studio projects, etc.). IntelliSense cần biết:
- Include paths nào được sử dụng
- Defines nào được set
- Compiler flags nào được áp dụng

File `compile_commands.json` chứa tất cả thông tin này cho mọi source file trong project.

## Troubleshooting

### IntelliSense vẫn báo lỗi sau khi configure?
1. Reload IntelliSense: `Ctrl+Shift+P` → "C/C++: Reload IntelliSense Database"
2. Restart VSCode
3. Xóa folder `build/` và chạy lại `.\build.ps1`

### compile_commands.json không được tạo?
- Đảm bảo CMake version >= 3.5
- Kiểm tra flag `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` được set

### Include paths vẫn không đúng?
- Kiểm tra `target_include_directories()` trong CMakeLists.txt
- Đảm bảo sử dụng `PUBLIC` hoặc `INTERFACE` scope cho include directories
