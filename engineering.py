import math
import numpy as np

# ==========================================
# MODULE A: PIPE FLOW CALCULATOR
# ==========================================

class Fluid:
    """
    Represents a fluid with specific physical properties.
    """
    def __init__(self, name: str, density: float, dynamic_viscosity: float):
        """
        Initializes a Fluid object.
        
        Args:
            name (str): The name of the fluid (e.g., 'Water', 'Air').
            density (float): Fluid density in kg/m^3.
            dynamic_viscosity (float): Dynamic viscosity in Pa.s (kg/m.s).
        """
        if density <= 0 or dynamic_viscosity <= 0:
            raise ValueError("Density and viscosity must be strictly positive values.")
        
        self.name = name
        self.density = density
        self.mu = dynamic_viscosity


class Pipe:
    """
    Represents a circular pipe for fluid flow calculations.
    """
    def __init__(self, diameter: float, length: float, roughness: float):
        """
        Initializes a Pipe object.
        
        Args:
            diameter (float): Internal pipe diameter in meters.
            length (float): Length of the pipe in meters.
            roughness (float): Absolute pipe roughness in meters.
        """
        if diameter <= 0 or length <= 0:
            raise ValueError("Pipe diameter and length must be strictly positive.")
        if roughness < 0:
            raise ValueError("Pipe roughness cannot be negative.")
            
        self.D = diameter
        self.L = length
        self.epsilon = roughness

    def area(self) -> float:
        """Calculates the cross-sectional area of the pipe in m^2."""
        return math.pi * (self.D ** 2) / 4.0

    def velocity(self, flow_rate: float) -> float:
        """
        Calculates the average fluid velocity in m/s.
        
        Args:
            flow_rate (float): Volumetric flow rate in m^3/s.
        """
        if flow_rate < 0:
            raise ValueError("Flow rate cannot be negative.")
        return flow_rate / self.area()

    def reynolds_number(self, fluid: Fluid, flow_rate: float) -> float:
        """Calculates the dimensionless Reynolds number."""
        v = self.velocity(flow_rate)
        return (fluid.density * v * self.D) / fluid.mu

    def friction_factor(self, fluid: Fluid, flow_rate: float) -> float:
        """
        Calculates the Darcy friction factor.
        Uses 64/Re for laminar flow and the Haaland equation for turbulent flow.
        """
        if flow_rate == 0:
            return 0.0
            
        Re = self.reynolds_number(fluid, flow_rate)
        
        if Re < 2300:
            # Laminar flow
            return 64.0 / Re
        else:
            # Turbulent flow (Haaland Equation)
            term1 = (self.epsilon / self.D) / 3.7
            term2 = 6.9 / Re
            inv_sqrt_f = -1.8 * math.log10(term1**1.11 + term2)
            return (1.0 / inv_sqrt_f) ** 2

    def pressure_drop(self, fluid: Fluid, flow_rate: float) -> float:
        """
        Calculates the pressure drop across the pipe using the Darcy-Weisbach equation.
        
        Returns:
            float: Pressure drop in Pascals (Pa).
        """
        if flow_rate == 0:
            return 0.0
            
        f = self.friction_factor(fluid, flow_rate)
        v = self.velocity(flow_rate)
        
        # Darcy-Weisbach Equation
        delta_p = f * (self.L / self.D) * (fluid.density * (v ** 2)) / 2.0
        return delta_p


# ==========================================
# MODULE B: HEAT TRANSFER CALCULATOR
# ==========================================

def fourier_conduction(k: float, area: float, thickness: float, T_hot: float, T_cold: float) -> float:
    """
    Calculates the steady-state heat transfer rate through a flat wall 
    using Fourier's Law of Heat Conduction.
    
    Args:
        k (float): Thermal conductivity of the wall material (W/m.K).
        area (float): Cross-sectional area perpendicular to heat flow (m^2).
        thickness (float): Thickness of the wall (m).
        T_hot (float): Temperature of the hot side (C or K).
        T_cold (float): Temperature of the cold side (C or K).
        
    Returns:
        float: Heat transfer rate (Watts).
    """
    if thickness <= 0:
        raise ValueError("Wall thickness must be greater than zero.")
    if k < 0 or area < 0:
        raise ValueError("Thermal conductivity and area must be non-negative.")
        
    return (k * area * (T_hot - T_cold)) / thickness


def newtons_cooling(T0: float, T_inf: float, r: float, times: np.ndarray) -> np.ndarray:
    """
    Calculates the temperature of an object over time using Newton's Law of Cooling.
    
    Args:
        T0 (float): Initial temperature of the object.
        T_inf (float): Ambient/surrounding temperature.
        r (float): Cooling rate constant (1/s).
        times (np.ndarray): NumPy array of time values.
        
    Returns:
        np.ndarray: Array of temperatures corresponding to the input times.
    """
    if r < 0:
        raise ValueError("Cooling rate constant 'r' cannot be negative.")
        
    return T_inf + (T0 - T_inf) * np.exp(-r * times)