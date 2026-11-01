# #  nvidia-macos-driver-goldengate

An experimental, developer-focused research fork of the **nullmoth/nvidia-macos-driver** ecosystem, explicitly designed to draft, test, and implement system-level shims for **macOS 27 Golden Gate** compatibility across modern desktop GPUs and legacy Intel hardware.

---

## ⚠️ Upstream Notice & Operational Scope
Mainline development focuses on building full Metal 3 acceleration capabilities over modern Turing, Ampere, Ada Lovelace, and Blackwell GPUs up through macOS 26 Tahoe. 

This independent research fork extends that code tree to explore the low-level kernel changes, Cryptex adjustments, AMFI policy overrides, and vintage Intel mobile VESA fallbacks required to successfully boot initial macOS 27 development seeds on unsupported devices. It is strictly an **Alpha-stage research project** and not a plug-and-play consumer utility.

---

## 🌟 Targeted Hardware Matrices (Phase 1 Support)

Development pathways are compartmentalized into two distinct hardware architectural branches to maximize deployment targets:

### 🎮 1. Modern NVIDIA GPU Branch (Desktop Virtualization)
Bypasses minimum/maximum kernel extension verification restrictions to force null-moth's SPIR-V and Mesa NVK translation layers to bind natively with modern PCIe graphics cards.
* **Target Architectures:** Turing (GTX 16xx / RTX 20xx), Ampere (RTX 30xx), Ada Lovelace (RTX 40xx), and Blackwell (RTX 50xx) series.
* **Strategy:** Overrides driver bundle manifest KPI bounds (`OSBundleLibraries` locked down to `27.0.0`) to load the driver stack past the native macOS 26 software cap.

### 💻 2. Legacy Intel Branch (2015 MacBook Pro Line)
Deactivates core coprocessor hardware checking loops and automates unaccelerated VESA frame buffer safe configurations to safeguard the initialization sequence on vintage Apple laptop hardware.
* **Target Models:** MacBookPro11,4, MacBookPro11,5, and MacBookPro12,1 (Mid/Early 2015 Retina Pros)
* **Strategy:** Injects custom stolen memory parameters and display properties directly into the integrated Intel Iris Pro 5200 controller to prevent panels from permanently dropping to a black screen during phase 1 boot cycles.

---

## 📂 Repository Layout

Custom additions specific to this macOS 27 Golden Gate research branch are organized inside the following clean directory structure:
* `/.github/workflows/release_driver.yml` — Automated universal Linux server pipeline to test and package early deployment zips on the first try.
* `/src/macos27_shims/version_lock.py` — Intercepts bundle manifests and spoofs native Darwin KPI constraints to match macOS 27 requirements.
* `/src/macos27_shims/intel_compatibility.py` — Coordinates device properties injection and VESA safe loops for 2015 MacBook Pros.
* `/src/macos27_shims/amfi_override.py` — Stages environmental arguments to relax code-signing validation loops under updated kernels.

---

## 🛠️ Automated Cloud Compilation

This project leverages automated Ubuntu Linux server workflows to handle mechanical file building. Whenever an official version tag is pushed (e.g., `v3.0.0-alpha-early-27`) or the workflow is triggered manually via the website interface, the runner will automatically compile, zip, and attach the final release distribution asset package straight to the repository page:

```bash
# To clear local Gatekeeper quarantine blocks on an extracted release zip layout:
xattr -cr /Applications/nvidia_goldengate_pkg/
```

---

## ⚠️ Disclaimer
This repository involves heavy manipulation of operating system kernels, driver manifests, and low-level graphics subsystems. Mismatched or incorrect configuration configurations can result in immediate system panics, terminal boot loops, or permanent data loss on target machines. Proceed with absolute caution on external USB testing media only.
