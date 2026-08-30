"""Projects 1-3: first-order decay, Arrhenius kinetics, and A -> B -> C."""

from __future__ import annotations

import csv
import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "cheme-matplotlib-cache"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent / "results" / "projects_1_to_3"
PLOTS = ROOT / "plots"
DATA = ROOT / "data"


def save_csv(path: Path, columns: dict[str, np.ndarray]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(zip(*columns.values()))


def finish_plot(fig: plt.Figure, ax: plt.Axes, path: Path) -> None:
    ax.grid(True, alpha=0.22)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def project_1() -> str:
    c0, k = 1.0, 0.1
    time_s = np.linspace(0, 50, 501)
    concentration = c0 * np.exp(-k * time_s)
    half_life = np.log(2) / k

    save_csv(DATA / "project_1_first_order_decay.csv", {
        "time_s": time_s,
        "concentration_mol_L": concentration,
    })
    fig, ax = plt.subplots(figsize=(8.4, 5))
    ax.plot(time_s, concentration, color="#176B87", linewidth=2.8)
    ax.axvline(half_life, color="#E07A5F", linestyle="--", label=f"Half-life = {half_life:.2f} s")
    ax.set(title="First-Order Reaction Decay", xlabel="Time (s)", ylabel="Concentration of A (mol/L)")
    ax.legend(frameon=False)
    finish_plot(fig, ax, PLOTS / "project_1_first_order_decay.png")
    return f"Project 1: half-life = {half_life:.2f} s"


def project_2() -> str:
    c0, ea, gas_constant, prefactor = 1.0, 50_000.0, 8.314, 1e13
    temperatures = np.array([280.0, 300.0, 320.0, 340.0])
    rates = prefactor * np.exp(-ea / (gas_constant * temperatures))
    time_s = np.linspace(0, 7 / rates.min(), 700)
    profiles = np.array([c0 * np.exp(-rate * time_s) for rate in rates])

    columns = {"time_s": time_s}
    for temperature, profile in zip(temperatures.astype(int), profiles):
        columns[f"concentration_{temperature}K_mol_L"] = profile
    save_csv(DATA / "project_2_arrhenius_temperature.csv", columns)

    fig, ax = plt.subplots(figsize=(8.4, 5))
    colors = ["#264653", "#2A9D8F", "#E9C46A", "#E76F51"]
    for temperature, rate, profile, color in zip(temperatures, rates, profiles, colors):
        ax.plot(time_s * 1e3, profile, color=color, linewidth=2.5,
                label=f"{temperature:.0f} K (k={rate:.2e} 1/s)")
    ax.set(title="Temperature Dependence via Arrhenius Equation", xlabel="Time (ms)",
           ylabel="Concentration of A (mol/L)")
    ax.legend(frameon=False)
    finish_plot(fig, ax, PLOTS / "project_2_arrhenius_temperature.png")
    return f"Project 2: k increases {rates[-1] / rates[0]:.1f}x from 280 K to 340 K"


def project_3() -> str:
    c0, k1, k2 = 1.0, 0.1, 0.05
    time_s = np.linspace(0, 100, 1001)
    ca = c0 * np.exp(-k1 * time_s)
    cb = (k1 / (k2 - k1)) * c0 * (np.exp(-k1 * time_s) - np.exp(-k2 * time_s))
    cc = c0 - ca - cb
    peak_time = np.log(k1 / k2) / (k1 - k2)
    peak_b = (k1 / (k2 - k1)) * c0 * (np.exp(-k1 * peak_time) - np.exp(-k2 * peak_time))

    save_csv(DATA / "project_3_sequential_reaction.csv", {
        "time_s": time_s,
        "A_mol_L": ca,
        "B_mol_L": cb,
        "C_mol_L": cc,
        "mass_balance_mol_L": ca + cb + cc,
    })
    fig, ax = plt.subplots(figsize=(8.4, 5))
    ax.plot(time_s, ca, label="A (reactant)", color="#264653", linewidth=2.5)
    ax.plot(time_s, cb, label="B (intermediate)", color="#E9C46A", linewidth=2.8)
    ax.plot(time_s, cc, label="C (final product)", color="#E76F51", linewidth=2.5)
    ax.scatter([peak_time], [peak_b], color="#9C6644", zorder=5)
    ax.annotate(f"Max B = {peak_b:.3f} mol/L at {peak_time:.2f} s", (peak_time, peak_b),
                xytext=(18, 18), textcoords="offset points", arrowprops={"arrowstyle": "->"})
    ax.set(title="Sequential Reaction: A to B to C", xlabel="Time (s)", ylabel="Concentration (mol/L)")
    ax.legend(frameon=False)
    finish_plot(fig, ax, PLOTS / "project_3_sequential_reaction.png")
    return f"Project 3: B peaks at {peak_b:.3f} mol/L after {peak_time:.2f} s"


if __name__ == "__main__":
    PLOTS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    for result in (project_1(), project_2(), project_3()):
        print(result)
    print(f"Saved results to {ROOT}")


