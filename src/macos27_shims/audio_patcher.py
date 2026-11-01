"""
NVIDIA macOS Driver Golden Gate Extension - Audio Engine Patcher
Injects layout configurations and device properties for the Cirrus Logic CS4208 
audio controller found on 2015 MacBook Pro models under macOS 27.
"""

class GoldenGateAudioPatcher:
    # 2015 MacBook Pro 15-inch (MacBookPro11,4/11,5) natively uses layout ID 3 for Cirrus CS4208
    NATIVE_LAYOUT_ID = 3

    @classmethod
    def patch_audio_properties(cls, config_plist: dict) -> dict:
        """
        Injects the mandatory layout-id parameters into the Intel High Definition Audio (HDEF)
        device tree node path to activate built-in speakers and headphone jacks.
        """
        hdef_path = "PPCI0@0/AppleACPIPCI/HDEF@1B"
        
        if "DeviceProperties" not in config_plist:
            config_plist["DeviceProperties"] = {"Add": {}}
        if "Add" not in config_plist["DeviceProperties"]:
            config_plist["DeviceProperties"]["Add"] = {}
        if hdef_path not in config_plist["DeviceProperties"]["Add"]:
            config_plist["DeviceProperties"]["Add"][hdef_path] = {}

        # Inject layout-id as a 4-byte Data array (3 -> 03 00 00 00)
        config_plist["DeviceProperties"]["Add"][hdef_path].update({
            "layout-id": [0x03, 0x00, 0x00, 0x00],
            "model": "Cirrus Logic CS4208 HD Audio (OPLC-Plus Injection)",
            "hda-gfx": "onboard-1"
        })
        
        print(f"[+] Injected Cirrus Logic CS4208 Audio Layout-ID: {cls.NATIVE_LAYOUT_ID}")
        return config_plist

    @classmethod
    def get_audio_boot_arg_fallback(cls) -> str:
        """
        Returns the AppleALC fallback boot argument to force layout properties
        if the primary device tree path injection is bypassed by the kernel.
        """
        return f"alcid={cls.NATIVE_LAYOUT_ID}"
