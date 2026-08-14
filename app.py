import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io
from engineering import Fluid, Pipe, fourier_conduction, newtons_cooling

# ==========================================
# 1. ENTERPRISE PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="KNUST-01 Subsea Engineering Suite",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. PROPRIETARY CSS INJECTION
# ==========================================
st.markdown("""
    <style>
    /* Import modern sleek font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding for a standalone app feel */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Style the Sidebar to look like a premium control panel */
    [data-testid="stSidebar"] {
        border-right: 1px solid #1F2937;
        box-shadow: 2px 0 10px rgba(0,0,0,0.5);
    }
    
    /* Executive Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #111827;
        border: 1px solid #1F2937;
        padding: 5% 5% 5% 10%;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        border-left: 4px solid #00E5FF;
    }
    
    /* High-Grade Action Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(67, 100, 247, 0.4);
        color: white;
        border: none;
    }
    
    /* File Uploader Customization */
    [data-testid="stFileUploadDropzone"] {
        background-color: #111827;
        border: 2px dashed #374151;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.title("KNUST-01")
    st.caption("Deepwater Engineering Suite v2.0")
    st.divider()
    
    page = st.radio(
        "SYSTEM NAVIGATION",
        ["Module A: Pipe Flow Analyser", 
         "Module B: Heat Transfer Calculator", 
         "Module C: Data Dashboard"]
    )
    
    st.divider()
    st.caption("© 2026 Subsea Thermodynamics Dept.")

# ==========================================
# 4. MAIN APP HEADER
# ==========================================
st.title("Fluid & Thermodynamic Analytics")
st.markdown("---")

# ==========================================
# MODULE A: PIPE FLOW ANALYSER
# ==========================================
if page == "Module A: Pipe Flow Analyser":
    st.header("Fluid Flow & Pipe Analyser")
    st.write("Calculate fluid properties and pressure drop across a pipe system.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Fluid Properties")
        fluid_choice = st.selectbox("Select Fluid", ["Water", "Air", "Crude Oil (Light)", "Custom"])
        
        if fluid_choice == "Water":
            rho, mu = 998.2, 1.002e-3
        elif fluid_choice == "Air":
            rho, mu = 1.204, 1.825e-5
        elif fluid_choice == "Crude Oil (Light)":
            rho, mu = 850.0, 1.500e-2
        else:
            rho = st.number_input("Density (kg/m³)", min_value=0.1, value=1000.0)
            mu = st.number_input("Dynamic Viscosity (Pa·s)", min_value=0.00001, value=0.001, format="%.5f")
            
        st.info(f"**Using Density:** {rho} kg/m³ | **Viscosity:** {mu} Pa·s")
        current_fluid = Fluid(fluid_choice, rho, mu)

    with col2:
        st.subheader("2. Pipe Geometry & Flow")
        D = st.number_input("Pipe Diameter (m)", min_value=0.01, value=0.1)
        L = st.number_input("Pipe Length (m)", min_value=1.0, value=100.0)
        roughness = st.number_input("Pipe Roughness (m)", min_value=0.0, value=0.000045, format="%.6f")
        Q = st.number_input("Flow Rate (m³/s)", min_value=0.0, value=0.05)
        
        current_pipe = Pipe(D, L, roughness)

    st.markdown("---")
    
    if st.button("Calculate Flow Properties"):
        try:
            vel = current_pipe.velocity(Q)
            re = current_pipe.reynolds_number(current_fluid, Q)
            f = current_pipe.friction_factor(current_fluid, Q)
            dp = current_pipe.pressure_drop(current_fluid, Q)
            
            st.subheader("Results")
            r_col1, r_col2, r_col3, r_col4 = st.columns(4)
            r_col1.metric("Velocity", f"{vel:.2f} m/s")
            r_col2.metric("Reynolds Number", f"{re:.0f}")
            r_col3.metric("Friction Factor", f"{f:.4f}")
            r_col4.metric("Pressure Drop", f"{dp/1000:.2f} kPa")
            
            st.subheader("Pressure Drop vs. Flow Rate")
            q_values = np.linspace(0.01, Q * 2, 20)
            dp_values = [current_pipe.pressure_drop(current_fluid, q) / 1000 for q in q_values]
            
            df_plot = pd.DataFrame({"Flow Rate (m³/s)": q_values, "Pressure Drop (kPa)": dp_values})
            fig = px.line(df_plot, x="Flow Rate (m³/s)", y="Pressure Drop (kPa)", markers=True)
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#F0F4F8")
            st.plotly_chart(fig, use_container_width=True)
            
            csv = df_plot.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Plot Data as CSV", data=csv, file_name='pipe_flow_data.csv', mime='text/csv')
            
        except Exception as e:
            st.error(f"Error in calculation: {e}")

# ==========================================
# MODULE B: HEAT TRANSFER CALCULATOR
# ==========================================
elif page == "Module B: Heat Transfer Calculator":
    st.header("Heat Transfer Calculator")
    
    st.subheader("1. Steady-State Conduction (Flat Wall)")
    st.write("Calculates heat transfer through a single-layer wall using Fourier's Law.")
    
    c1, c2, c3 = st.columns(3)
    k = c1.number_input("Thermal Conductivity (W/m·K)", min_value=0.01, value=0.6)
    area = c2.number_input("Wall Area (m²)", min_value=0.1, value=10.0)
    thickness = c3.number_input("Wall Thickness (m)", min_value=0.01, value=0.2)
    
    c4, c5 = st.columns(2)
    T_hot = c4.number_input("Hot Temp (°C)", value=30.0)
    T_cold = c5.number_input("Cold Temp (°C)", value=10.0)
    
    if st.button("Calculate Conduction"):
        q = fourier_conduction(k, area, thickness, T_hot, T_cold)
        st.success(f"**Heat Transfer Rate:** {q:.2f} Watts")

    st.markdown("---")
    
    st.subheader("2. Newton's Law of Cooling")
    st.write("Predicts how fast an object cools down in a given environment.")
    
    nc1, nc2, nc3 = st.columns(3)
    T0 = nc1.slider("Initial Temp (°C)", 0.0, 200.0, 100.0)
    T_inf = nc2.slider("Ambient Temp (°C)", 0.0, 50.0, 20.0)
    r = nc3.slider("Cooling Rate Constant (1/s)", 0.001, 0.1, 0.05, step=0.001)
    
    t_max = st.slider("Simulation Time (seconds)", 10, 300, 100)
    times = np.linspace(0, t_max, 100)
    temps = newtons_cooling(T0, T_inf, r, times)
    
    df_cooling = pd.DataFrame({"Time (s)": times, "Temperature (°C)": temps})
    fig2 = px.line(df_cooling, x="Time (s)", y="Temperature (°C)", title="Cooling Curve")
    fig2.add_hline(y=T_inf, line_dash="dash", annotation_text="Ambient Temp", annotation_position="bottom right")
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#F0F4F8")
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# MODULE C: ROCK & FLUID DATA DASHBOARD
# ==========================================
elif page == "Module C: Data Dashboard":
    st.header("Data Dashboard")
    st.write("Upload a CSV file containing rock/fluid data to view statistics and charts.")
    
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            
            st.subheader("Data Summary")
            st.dataframe(df.head())
            st.write(df.describe())
            
            st.markdown("---")
            
            cols = df.columns.tolist()
            
            st.subheader("Interactive Filtering & Visualization")
            filter_col = st.selectbox("Select column to filter by:", cols)
            min_val = float(df[filter_col].min())
            max_val = float(df[filter_col].max())
            
            cutoff = st.slider(f"Minimum {filter_col}", min_val, max_val, min_val)
            filtered_df = df[df[filter_col] >= cutoff]
            
            st.write(f"Showing **{len(filtered_df)}** of **{len(df)}** samples.")
            
            if len(cols) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    hist_fig = px.histogram(filtered_df, x=filter_col, title=f"Distribution of {filter_col}")
                    hist_fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#F0F4F8")
                    st.plotly_chart(hist_fig, use_container_width=True)
                    
                with col2:
                    x_axis = st.selectbox("X-Axis", cols, index=0)
                    y_axis = st.selectbox("Y-Axis", cols, index=1 if len(cols)>1 else 0)
                    scatter_fig = px.scatter(filtered_df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                    scatter_fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#F0F4F8")
                    st.plotly_chart(scatter_fig, use_container_width=True)
            
            csv_filtered = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Filtered Data (CSV)", data=csv_filtered, file_name='filtered_data.csv', mime='text/csv')
            
        except Exception as e:
            st.error(f"Error processing file. Please ensure it is a valid CSV. Detail: {e}")
    else:
        st.info("Awaiting CSV file upload. Please generate or upload a dataset to begin.")