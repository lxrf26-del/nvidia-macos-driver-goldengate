"""
NVIDIA macOS Driver Golden Gate Extension - Intel Hardware Compatibility Matrix
Maps legacy non-NVIDIA assets for 2015 MacBook Pro targets to safeguard 
early boot cycles under macOS 27 Golden Gate.
"""

class IntelMacCompatibility:
    TARGET_MODELS = {
        "MacBookPro11,4": {"display": "Intel Iris Pro 5200 (Integrated)", "platform": "Haswell"},
        "MacBookPro11,5": {"display": "AMD Radeon R9 M370X / Iris Pro", "platform": "Haswell/Broadwell"},
        "MacBookPro12,1": {"display": "Intel Iris Graphics 6100", "platform": "Broadwell"}
    }

    @classmethod
    def get_iris_pro_properties(cls, smbios_id: str) -> dict:
        """
        Generates the device properties injection map for Intel Iris Pro hardware.
        Forces the macOS 27 WindowServer into an unaccelerated VESA fallback path
        to prevent early kernel panics before full graphics acceleration is patched.
        """
        if smbios_id not in cls.TARGET_MODELS:
            return {}

        print(f"[+] Generating Intel fallback parameters for target hardware: {cls.TARGET_MODELS[smbios_id]['display']}")
        return {
            "PPCI0@0/AppleACPIPCI/IGPU@2": {
                "model": f"{cls.TARGET_MODELS[smbios_id]['display']} (Golden Gate Fallback)",
                "framebuffer-patch-enable": [0x01, 0x00, 0x00, 0x00],
                "framebuffer-stolenmem": [0x00, 0x00, 0x30, 0x01],  # Fixes DVMT allocation limits
                "disable-metal-accel": [0x01, 0x00, 0x00, 0x00]     # Safeguards display output on early seeds
            }
        }

    @classmethod
    def get_intel_boot_args(cls, smbios_id: str) -> str:
        """Appends environmental variables required to relax graphics validation on 2015 MacBooks."""
        if smbios_id in cls.TARGET_MODELS:
            return "-igfxvesa-no-egpu modern_framebuffer=1 restore_driverkit=1"
        return ""
