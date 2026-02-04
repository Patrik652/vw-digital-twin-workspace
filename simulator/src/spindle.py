"""Spindle physics model for the CNC simulator."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class BearingGeometry:
    """Rolling element bearing geometry for frequency calculations."""

    ball_diameter_mm: float = 8.0
    pitch_diameter_mm: float = 40.0
    contact_angle_deg: float = 15.0
    num_balls: int = 8


@dataclass(frozen=True)
class Spindle:
    """Spindle dynamics with thermal expansion and bearing frequencies."""

    thermal_expansion_coeff_per_c: float = 11.7e-6
    base_vibration_mm_s: float = 0.3
    bearing_geometry: BearingGeometry = BearingGeometry()

    def power_kw(self, rpm: float, torque_nm: float) -> float:
        """Compute spindle power (kW) from RPM and torque.

        Formula: P = (2π × RPM × Torque) / 60000
        """

        return (2.0 * math.pi * rpm * torque_nm) / 60000.0

    def thermal_expansion_mm(self, length_mm: float, delta_temp_c: float) -> float:
        """Compute thermal expansion in mm for a given length and ΔT."""

        return length_mm * self.thermal_expansion_coeff_per_c * delta_temp_c

    def bearing_frequencies_hz(self, rpm: float) -> dict[str, float]:
        """Calculate bearing defect frequencies in Hz.

        Returns BPFO, BPFI, BSF, and FTF based on geometry.
        """

        fr = rpm / 60.0
        geom = self.bearing_geometry
        cos_theta = math.cos(math.radians(geom.contact_angle_deg))
        d_over_d = geom.ball_diameter_mm / geom.pitch_diameter_mm

        bpfo = (geom.num_balls / 2.0) * fr * (1.0 - d_over_d * cos_theta)
        bpfi = (geom.num_balls / 2.0) * fr * (1.0 + d_over_d * cos_theta)
        bsf = (
            (geom.pitch_diameter_mm / geom.ball_diameter_mm)
            * fr
            * (1.0 - (d_over_d * cos_theta) ** 2)
        )
        ftf = 0.5 * fr * (1.0 - d_over_d * cos_theta)

        return {"BPFO": bpfo, "BPFI": bpfi, "BSF": bsf, "FTF": ftf}

    def vibration_mm_s(self, wear_percent: float) -> float:
        """Estimate vibration severity as bearing wear increases.

        Uses an exponential model to reflect accelerated vibration growth.
        """

        wear = max(0.0, min(100.0, wear_percent)) / 100.0
        vibration = self.base_vibration_mm_s * math.exp(3.0 * wear)
        return min(vibration, 10.0)
