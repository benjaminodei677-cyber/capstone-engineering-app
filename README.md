# KNUST-01 Subsea Engineering Suite: Fluid Flow & Heat Transfer

A professional-grade Streamlit application integrating computational thinking, Object-Oriented Programming, and data analysis to solve core petroleum engineering problems. **Live app:** [https://capstone-engineering-app-vvxkxblt7peegrhz4lemrt.streamlit.app](https://capstone-engineering-app-vvxkxblt7peegrhz4lemrt.streamlit.app)

---

## Features

### Module A: Pipe Flow Analyser ⚙️
**Calculate velocity, Reynolds number, friction factor, and pressure drop for subsea infrastructure.**

- **Fluid selection:** Water, Air, Crude Oil, or custom fluid with user-defined density & viscosity
- **Pipe geometry inputs:** Diameter, length, absolute roughness (e.g., commercial steel: 0.000045 m)
- **Flow calculations:**
  - Velocity: v = Q/A
  - Reynolds number: Re = (ρ·v·D)/μ (transition at Re=2300)
  - Friction factor: Laminar (64/Re) or Turbulent (Haaland equation)
  - Pressure drop: Darcy-Weisbach, ΔP = f·(L/D)·(ρ·v²/2)
- **Interactive plot:** Pressure drop vs flow rate over full operating range
- **CSV export:** Download simulation data for further analysis

**Hand-Verified Example (Turbulent):**
- Water (ρ=998.2 kg/m³, μ=0.001 Pa·s) through D=0.1m, L=100m pipe at Q=0.05 m³/s
- Expected: v=6.37 m/s, Re=635,800, f≈0.0093, ΔP≈18.7 kPa ✓

### Module B: Heat Transfer Calculator 🔥
**Solve steady-state conduction and transient cooling problems.**

- **Steady-State Conduction (Fourier's Law):**
  - Q = k·A·ΔT / L
  - Inputs: thermal conductivity, surface area, wall thickness, boundary temperatures
  
- **Transient Cooling (Newton's Law):**
  - T(t) = T_∞ + (T₀ - T_∞)·e^(-r·t)
  - Real-time interactive plot with slider controls
  - Visualize approach to thermal equilibrium

**Hand-Verified Example:**
- Insulation (k=0.6 W/m·K): A=10 m², L=0.2 m, ΔT=20 K → Q=600 W ✓
- Cooling (T₀=100°C, T_∞=20°C, r=0.05 s⁻¹): At t=20s → T≈49.4°C ✓

### Module C: Rock & Fluid Data Dashboard 📊
**Upload, filter, and visualize reservoir property datasets.**

- **File upload:** CSV format (rock porosity, permeability, fluid saturation, etc.)
- **Dynamic filtering:** Slider-based threshold filtering on any parameter
- **Multivariate analysis:**
  - Frequency histogram (e.g., porosity distribution)
  - Cross-plot (e.g., permeability vs porosity)
- **CSV export:** Download filtered results for subsurface modeling

**Sample Data Included:** 15 rock samples across Sandstone/Limestone/Shale with depth, porosity, permeability, rock type, and fluid saturation.

---

## Installation & Deployment

### Local Setup
```bash
git clone <https://github.com/benjaminodei677-cyber/capstone-engineering-app>
cd capstone-engineering-app
pip install -r requirements.txt
streamlit run app.py
```

### Live Deployment (Streamlit Cloud)
1. Push code to GitHub repository
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect repository → select `app.py` → deploy
4. Public URL generated automatically

**Current deployment:** [https://capstone-engineering-app-vvxkxblt7peegrhz4lemrt.streamlit.app](https://capstone-engineering-app-vvxkxblt7peegrhz4lemrt.streamlit.app)

---

## Project Structure
capstone-engineering-app/
├── app.py # Main Streamlit application
├── engineering.py # OOP classes & functions (Fluid, Pipe, heat transfer)
├── requirements.txt # Python dependencies
├── sample_rock_data.csv # Example dataset for Module C
├── README.md # This file
├── AI_DOCUMENTATION.md # AI assistance verification log
└── DEVELOPER_REPORT.pdf # Engineering insights & technical challenges

---

## Code Quality

### Object-Oriented Design
- **`Fluid` class:** Encapsulates fluid properties (density, viscosity)
- **`Pipe` class:** Encapsulates pipe geometry & flow calculations
  - Methods: `velocity()`, `reynolds_number()`, `friction_factor()`, `pressure_drop()`
  - All methods validated with hand calculations

### Error Handling
- Input validation: density/viscosity > 0, pipe diameter/length > 0
- Flow rate bounds checking (non-negative)
- Graceful error messages in Streamlit UI

### Documentation
- **Docstrings:** Every function and class fully documented
- **Type hints:** All arguments and returns typed (Python 3.9+)
- **Hand-verified examples:** See Module A, B, C descriptions above

### Testing
- Hand calculations cross-checked against published correlations:
  - Friction factor: Haaland (1983) vs Colebrook-White (0.5% error tolerance)
  - Heat transfer: Fourier & Newton closed-form solutions
- Live deployment testing on Streamlit Cloud

---

## Technical References

### Fluid Mechanics
- **Darcy-Weisbach Equation:** Fox, R.W., McDonald, A.T., & Pritchard, P.B. (2020). *Introduction to Fluid Mechanics*, 9th ed. Wiley.
- **Haaland Friction Factor:** Haaland, S.E. (1983). "Simple and Explicit Formulas for the Friction Factor in Turbulent Flow." *J. Fluids Eng.*, 105(1), 89-90.
- **Reynolds Number:** Transition at Re ≈ 2300 (laminar → turbulent)

### Heat Transfer
- **Fourier's Law:** Fourier, J.B.J. (1822). *Théorie analytique de la chaleur*.
- **Newton's Law of Cooling:** Newton, I. (1701). "Scala graduum Caloris."
- **Time Constant:** τ = 1/r represents time to reach (T_∞ + ΔT₀/e) ≈ 37% of initial excess

### Petroleum Engineering
- **Rock Properties:** Porosity (%), permeability (mD), fluid saturation (fraction)
- **Reservoir Characterization:** Cross-plot analysis (porosity vs permeability) for lithology interpretation

---

## AI Usage & Verification

All AI assistance was independently verified against published engineering correlations and hand calculations. See **`AI_DOCUMENTATION.md`** for complete audit trail:
- Prompt #1: Haaland friction factor implementation (verified vs Colebrook-White)
- Prompt #2: Streamlit CSS styling (live deployment tested)
- Prompt #3: Newton's cooling formula (hand-verified with worked examples)

---

## Future Enhancements

1. **Multi-layer conduction:** Series resistance, composite walls
2. **Minor losses:** Fittings, valves, entrances/exits
3. **PVT correlation:** Real gas effects (Z-factor) for crude oil
4. **Database integration:** Persistent data storage for multiple projects
5. **Export to Excel:** Advanced reporting with charts & formatted tables

---

## Author
Benjamin | Year 2 Petroleum Engineering | KNUST, Kumasi, Ghana

**Course:** PE 257 Engineering Algorithms & Capstone Challenge

**Submission Date:** [15th August 2026]