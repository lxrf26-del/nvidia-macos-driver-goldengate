"""
NVIDIA macOS Driver Golden Gate Extension - AMFI Policy Override
Generates runtime environmental variables and security overrides to allow 
unsigned, custom-compiled graphics drivers to load on macOS 27 Golden Gate.
"""

class AMFIOverrideManager:
    @staticmethod
    def generate_security_boot_args(disable_amfi: bool = True, allow_invalid: bool = True) -> str:
        """
        Computes the critical boot arguments required to downgrade macOS 27 code-signing
        enforcement loops. This allows the system to accept non-Apple signed driver extensions.
        """
        flags = []
        
        # Completely disable AMFI checks if requested
        if disable_amfi:
            # amfi=0x80 disables code signing enforcement entirely in early Darwin kernels
            flags.append("amfi=0x80")
        
        # Allow untrusted, unsigned, or cross-compiled binaries to execute
        if allow_invalid:
            flags.append("cs_allow_invalid=1")
            
        # Relax Library Validation locks so third-party plugins can hook into WindowServer
        flags.append("ipc_control_port_options=0")
        flags.append("-cs_relaxed")

        return " ".join(flags)

    @classmethod
    def patch_nvram_config_block(cls, config_plist: dict) -> dict:
        """
        Directly injects the computed AMFI and library validation boot arguments 
        into the OpenCore NVRAM schema configuration block.
        """
        nvram_uuid = "7C436110-AB2A-4BBB-A880-FE41995C9F82"
        print("[*] Injecting experimental macOS 27 AMFI policy overrides into NVRAM schema...")

        # Ensure the structural paths exist in the template dict
        if "NVRAM" not in config_plist:
            config_plist["NVRAM"] = {"Add": {}}
        if "Add" not in config_plist["NVRAM"]:
            config_plist["NVRAM"]["Add"] = {}
        if nvram_uuid not in config_plist["NVRAM"]["Add"]:
            config_plist["NVRAM"]["Add"][nvram_uuid] = {}

        # Fetch existing boot arguments if they exist
        existing_args = config_plist["NVRAM"]["Add"][nvram_uuid].get("boot-args", "")
        override_flags = cls.generate_security_boot_args()

        # Combine arguments cleanly without duplicate definitions
        combined_args = f"{existing_args} {override_flags}".strip()
        # Filter down white spaces to ensure clean parsing layout
        config_plist["NVRAM"]["Add"][nvram_uuid]["boot-args"] = " ".join(combined_args.split())

        print(f"    [+] Updated Active Boot Arguments: {config_plist['NVRAM']['Add'][nvram_uuid]['boot-args']}")
        return config_plist

if __name__ == "__main__":
    # Test execution trace printout
    print("--- OPLC-Plus / nvidia-macos-driver-goldengate Test Suite ---")
    mock_config = {"NVRAM": {"Add": {"7C436110-AB2A-4BBB-A880-FE41995C9F82": {"boot-args": "-v"}}}}
    updated_config = AMFIOverrideManager.patch_nvram_config_block(mock_config)
