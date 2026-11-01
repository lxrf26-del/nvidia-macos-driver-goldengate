#!/usr/bin/env python3
import os
import sys
import plistlib

class MacOS27Patcher:
    def __init__(self, plist_path):
        self.plist_path = plist_path
        self.config = None

    def load_config(self):
        """Loads and parses the OpenCore config.plist file."""
        if not os.path.exists(self.plist_path):
            print(f"[-] Error: Target plist not found at {self.plist_path}")
            return False
        try:
            with open(self.plist_path, 'rb') as f:
                self.config = plistlib.load(f)
            print("[+] Successfully loaded config.plist")
            return True
        except Exception as e:
            print(f"[-] Failed to parse plist: {e}")
            return False

    def save_config(self):
        """Writes the modified configuration back to disk."""
        try:
            with open(self.plist_path, 'wb') as f:
                plistlib.dump(self.config, f)
            print("[+] Successfully wrote modifications to config.plist")
            return True
        except Exception as e:
            print(f"[-] Failed to write plist: {e}")
            return False

    def patch_amfi_and_bootargs(self):
        """Core AMFI Override Logic: Forces boot arguments for macOS 27 compatibility."""
        print("[*] Running AMFI and boot-args patcher...")
        try:
            # Navigate to NVRAM -> Add -> 7C436110-AB2A-4BBB-A880-FE41995C9F82
            nvram_add = self.config['NVRAM']['Add']['7C436110-AB2A-4BBB-A880-FE41995C9F82']
            boot_args = nvram_add.get('boot-args', '')
            
            # Convert to list of arguments for clean filtering
            args_list = boot_args.split()
            
            # Remove existing conflicting args if present
            args_list = [arg for arg in args_list if not arg.startswith('amfi=') and arg != '-amfi_off']
            
            # Inject macOS 27 Specific Overrides
            # amfi=0x1 allowing necessary configuration alongside custom kext patching
            # -v for verbose debugging of early kernel panics
            args_list.extend(['amfi=0x1', '-v', 'ipc_control_port_options=0'])
            
            # Reconstruct string
            new_boot_args = ' '.join(args_list)
            nvram_add['boot-args'] = new_boot_args
            print(f"[+] Updated boot-args to: {new_boot_args}")
            return True
        except KeyError as e:
            print(f"[-] Missing standard OpenCore structure for NVRAM boot-args: {e}")
            return False

    def patch_graphics_device_properties(self):
        """Core Graphics Patcher Logic: Injects early shims for the NVIDIA GSP/Metal handshake."""
        print("[*] Running Graphics Framebuffer & GSP initialization patcher...")
        try:
            # DeviceProperties -> Add
            dev_props = self.config.setdefault('DeviceProperties', {}).setdefault('Add', {})
            
            # Standard primary PCI path for GPU (Adjust if targeting secondary slots)
            pci_gpu_path = "PciRoot(0x0)/Pci(0x1,0x0)/Pci(0x0,0x0)"
            gpu_props = dev_props.setdefault(pci_gpu_path, {})
            
            # Injecting necessary overrides to signal the NullMoth driver framework
            gpu_props['disable-metal-beta'] = bytes([0x00, 0x00, 0x00, 0x00]) # Force enable Metal 3
            gpu_props['gsp-firmware-mode'] = bytes([0x01, 0x00, 0x00, 0x00])  # Force GSP offload mode
            gpu_props['macos27-shim-active'] = bytes([0x01, 0x00, 0x00, 0x00]) # Custom identifier for your fork
            
            print(f"[+] Successfully injected macOS 27 graphics descriptors into {pci_gpu_path}")
            return True
        except Exception as e:
            print(f"[-] Failed to patch DeviceProperties: {e}")
            return False

    def run_all(self):
        if self.load_config():
            amfi_ok = self.patch_amfi_and_bootargs()
            gfx_ok = self.patch_graphics_device_properties()
            if amfi_ok or gfx_ok:
                self.save_config()

if __name__ == "__main__":
    # Point this to your active development EFI's config.plist
    target_plist = "EFI/OC/config.plist" 
    
    patcher = MacOS27Patcher(target_plist)
    patcher.run_all()
