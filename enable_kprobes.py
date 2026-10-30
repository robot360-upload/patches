from pathlib import Path

config = Path("arch/arm64/configs/vendor/gta4l-common.config")

if not config.is_file():
    raise FileNotFoundError(f"Config not found: {config}")

options = {
    "CONFIG_KPROBES": "y",
    "CONFIG_KRETPROBES": "y",
    "CONFIG_KPROBE_EVENTS": "y",
    "CONFIG_KSU": "y",
    "CONFIG_KSU_KPROBES_HOOK": "y",
}

lines = config.read_text().splitlines()

# Remove existing assignments and disabled entries.
lines = [
    line for line in lines
    if not any(
        line.startswith(f"{key}=") or
        line == f"# {key} is not set"
        for key in options
    )
]

# Append the requested configuration.
lines.extend([""] + [
    f"{key}={value}" for key, value in options.items()
])

config.write_text("\n".join(lines) + "\n")

print("Updated KernelSU-Next Kprobes configuration:")
for key, value in options.items():
    print(f"{key}={value}")
