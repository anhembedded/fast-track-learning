# Script to configure and build the project with IntelliSense support
# This ensures compile_commands.json is always up-to-date

Write-Host "Configuring CMake project with compile_commands.json..." -ForegroundColor Cyan

# Configure CMake with compile commands export
cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ CMake configuration successful" -ForegroundColor Green
    
    # Copy compile_commands.json to root for IntelliSense
    if (Test-Path "build\compile_commands.json") {
        Copy-Item -Path "build\compile_commands.json" -Destination "." -Force
        Write-Host "✓ compile_commands.json copied to root directory" -ForegroundColor Green
    }
    
    Write-Host "`nBuilding project..." -ForegroundColor Cyan
    cmake --build build --config Debug
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Build successful" -ForegroundColor Green
    } else {
        Write-Host "✗ Build failed" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✗ CMake configuration failed" -ForegroundColor Red
    exit 1
}
