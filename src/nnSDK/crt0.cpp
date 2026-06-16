namespace nn {
namespace svc {
void ExitProcess(void);
} // namespace svc
} // namespace nn

void nninitRegion(void);
void nninitLocale(void);
void nninitSystem(void);
void nninitStartUp(void);
void __cpp_initialize__aeabi_(void);
void nninitCallStaticInitializers(void);
void nninitSetup(void);
void nnMain(void);

#pragma arm
__asm void __ctr_start() {
    // clang-format off

    PRESERVE8
    bl __cpp(nninitRegion)                 // Region
    bl __cpp(nninitLocale)                 // Locale
    bl __cpp(nninitSystem)                 // System
    bl __cpp(nninitStartUp)                // Startup
    blx __cpp(__cpp_initialize__aeabi_)    // Initialize CPP ARM
    bl __cpp(nninitCallStaticInitializers) // Static Initializer Manager
    bl __cpp(nninitSetup)                  // Initializes Setup
    bl __cpp(nnMain)                       // Main Application Loop
    b __cpp(nn::svc::ExitProcess)          // Exit Process if needed

    // clang-format on
}
