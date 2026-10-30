from pathlib import Path

config = Path("arch/arm64/configs/vendor/gta4l-common.config")

if not config.is_file():
    raise FileNotFoundError(config)

options = {
    "CONFIG_KPROBES": "y",
    "CONFIG_KRETPROBES": "y",
    "CONFIG_KPROBE_EVENTS": "y",
    "CONFIG_KSU": "y",
    "CONFIG_KSU_MANUAL_HOOK": None,
    "CONFIG_KSU_KPROBES_HOOK": "y",
}

lines = config.read_text().splitlines()

lines = [
    line for line in lines
    if not any(
        line.startswith(f"{key}=")
        or line == f"# {key} is not set"
        for key in options
    )
]

lines.append("")

for key, value in options.items():
    if value is None:
        lines.append(f"# {key} is not set")
    else:
        lines.append(f"{key}={value}")

config.write_text("\n".join(lines) + "\n")

print("Updated KernelSU Kprobes configuration.")
