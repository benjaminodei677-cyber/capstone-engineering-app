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
# 2. PREMIUM SaaS CSS INJECTION
# ==========================================
st.markdown("""
    <style>
    /* Import Premium SaaS Font: Plus Jakarta Sans */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Premium Gradient Headings */
    h1 {
        background: -webkit-linear-gradient(45deg, #00E5FF, #4364F7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }
    h2, h3 {
        color: #F8FAFC !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }

    /* Main Background Pattern (Subtle grid) */
    .stApp {
        background-color: #0B0F19;
        background-image: radial-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(11, 15, 25, 0.8) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Executive Floating Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #111827, #0B0F19);
        border: 1px solid rgba(0, 229, 255, 0.2);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(0, 229, 255, 0.5);
        box-shadow: 0 10px 40px 0 rgba(0, 229, 255, 0.1);
    }
    
    /* High-Grade Glowing Action Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00E5FF 0%, #0052D4 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: 700;
        letter-spacing: 0.5px;
        transition: all 0.4s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 82, 212, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 229, 255, 0.4);
    }
    
    /* Sleek Input Fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 1px solid #1F2937;
        background-color: #111827;
        color: #F8FAFC;
    }
    
    /* File Uploader Customization */
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(17, 24, 39, 0.6);
        border: 2px dashed rgba(0, 229, 255, 0.4);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #00E5FF;
        background-color: rgba(0, 229, 255, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("### 🌊 KNUST-01")
    st.caption("DEEPWATER ENGINEERING SUITE")
    st.divider()
    
    page = st.radio(
        "SYSTEM NAVIGATION",
        ["Module A: Pipe Flow Analyser", 
         "Module B: Heat Transfer Calculator", 
         "Module C: Data Dashboard"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("© 2026 Subsea Thermodynamics")

# ==========================================
# 4. MAIN APP HEADER
# ==========================================
st.title("Fluid & Thermodynamic Analytics")
st.markdown("---")

# ==========================================
# PLOTLY THEME CONFIG (To make charts look expensive)
# ==========================================
def apply_premium_chart_style(fig):
    fig.update_layout(
        font_family="Plus Jakarta Sans",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#94A3B8",
        xaxis=dict(showgrid=True, gridcolor='#1F2937', gridwidth=1, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='#1F2937', gridwidth=1, zeroline=False),
        margin=dict(l=20, r=20, t=40, b=20),
        hoverlabel=dict(bgcolor="#111827", font_size=14, font_family="Plus Jakarta Sans", bordercolor="#334155")
    )
    return fig

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

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Calculate Flow Properties"):
        try:
            vel = current_pipe.velocity(Q)
            re = current_pipe.reynolds_number(current_fluid, Q)
            f = current_pipe.friction_factor(current_fluid, Q)
            dp = current_pipe.pressure_drop(current_fluid, Q)
            
            st.markdown("<br>", unsafe_allow_html=True)
            r_col1, r_col2, r_col3, r_col4 = st.columns(4)
            r_col1.metric("Velocity", f"{vel:.2f} m/s")
            r_col2.metric("Reynolds Number", f"{re:.0f}")
            r_col3.metric("Friction Factor", f"{f:.4f}")
            r_col4.metric("Pressure Drop", f"{dp/1000:.2f} kPa")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Pressure Drop Analysis")
            q_values = np.linspace(0.01, Q * 2, 40) # Increased resolution for smooth curve
            dp_values = [current_pipe.pressure_drop(current_fluid, q) / 1000 for q in q_values]
            
            df_plot = pd.DataFrame({"Flow Rate (m³/s)": q_values, "Pressure Drop (kPa)": dp_values})
            fig = px.line(df_plot, x="Flow Rate (m³/s)", y="Pressure Drop (kPa)")
            
            # Premium Chart Styling
            fig.update_traces(
                line=dict(color='#00E5FF', width=3), 
                fill='tozeroy', 
                fillcolor='rgba(0, 229, 255, 0.1)'
            )
            fig = apply_premium_chart_style(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            csv = df_plot.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Plot Data (CSV)", data=csv, file_name='pipe_flow_data.csv', mime='text/csv')
            
        except Exception as e:
            st.error(f"Error in calculation: {e}")

# ==========================================
# MODULE B: HEAT TRANSFER CALCULATOR
# ==========================================
elif page == "Module B: Heat Transfer Calculator":
    st.header("Thermal Analytics Engine")
    
    st.subheader("1. Steady-State Conduction")
    st.write("Fourier's Law heat transfer profile for single-layer structures.")
    
    c1, c2, c3 = st.columns(3)
    k = c1.number_input("Thermal Conductivity (W/m·K)", min_value=0.01, value=0.6)
    area = c2.number_input("Wall Area (m²)", min_value=0.1, value=10.0)
    thickness = c3.number_input("Wall Thickness (m)", min_value=0.01, value=0.2)
    
    c4, c5 = st.columns(2)
    T_hot = c4.number_input("Hot Temp (°C)", value=30.0)
    T_cold = c5.number_input("Cold Temp (°C)", value=10.0)
    
    if st.button("Simulate Conduction"):
        q = fourier_conduction(k, area, thickness, T_hot, T_cold)
        st.success(f"**Heat Transfer Rate:** {q:.2f} Watts")

    st.markdown("---")
    
    st.subheader("2. Dynamic Cooling Simulation")
    st.write("Newton's Law of Cooling trajectory.")
    
    nc1, nc2, nc3 = st.columns(3)
    T0 = nc1.slider("Initial Temp (°C)", 0.0, 200.0, 100.0)
    T_inf = nc2.slider("Ambient Temp (°C)", 0.0, 50.0, 20.0)
    r = nc3.slider("Cooling Constant (1/s)", 0.001, 0.1, 0.05, step=0.001)
    
    t_max = st.slider("Simulation Time Horizon (s)", 10, 300, 100)
    times = np.linspace(0, t_max, 100)
    temps = newtons_cooling(T0, T_inf, r, times)
    
    df_cooling = pd.DataFrame({"Time (s)": times, "Temperature (°C)": temps})
    fig2 = px.line(df_cooling, x="Time (s)", y="Temperature (°C)")
    
    # Premium Chart Styling
    fig2.update_traces(
        line=dict(color='#F43F5E', width=3), # Sleek Rose/Red line
        fill='tozeroy', 
        fillcolor='rgba(244, 63, 94, 0.1)'
    )
    fig2.add_hline(y=T_inf, line_dash="dash", line_color="#00E5FF", annotation_text="Ambient Threshold", annotation_font_color="#00E5FF")
    fig2 = apply_premium_chart_style(fig2)
    
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# MODULE C: ROCK & FLUID DATA DASHBOARD
# ==========================================
elif page == "Module C: Data Dashboard":
    st.header("Reservoir Data Analytics")
    st.write("Upload dataset for advanced visualization and statistical breakdown.")
    
    uploaded_file = st.file_uploader("Drop CSV file here", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Telemetry linked successfully.")
            
            st.subheader("Raw Telemetry")
            st.dataframe(df.head(), use_container_width=True)
            
            st.markdown("---")
            
            cols = df.columns.tolist()
            st.subheader("Visual Analytics")
            
            filter_col = st.selectbox("Target Parameter:", cols)
            min_val = float(df[filter_col].min())
            max_val = float(df[filter_col].max())
            
            cutoff = st.slider(f"Filter Threshold ({filter_col})", min_val, max_val, min_val)
            filtered_df = df[df[filter_col] >= cutoff]
            
            st.caption(f"Yield: {len(filtered_df)} of {len(df)} samples active.")
            
            if len(cols) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    hist_fig = px.histogram(filtered_df, x=filter_col, title=f"Density Dist: {filter_col}")
                    hist_fig.update_traces(marker_color='#4364F7', marker_line_color='#0B0F19', marker_line_width=1, opacity=0.8)
                    hist_fig = apply_premium_chart_style(hist_fig)
                    st.plotly_chart(hist_fig, use_container_width=True)
                    
                with col2:
                    x_axis = st.selectbox("X-Axis (Independent)", cols, index=0)
                    y_axis = st.selectbox("Y-Axis (Dependent)", cols, index=1 if len(cols)>1 else 0)
                    scatter_fig = px.scatter(filtered_df, x=x_axis, y=y_axis, title=f"Correlation: {y_axis} vs {x_axis}")
                    scatter_fig.update_traces(marker=dict(size=8, color='#00E5FF', line=dict(width=1, color='#FFFFFF')))
                    scatter_fig = apply_premium_chart_style(scatter_fig)
                    st.plotly_chart(scatter_fig, use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            csv_filtered = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Export Filtered Dataset", data=csv_filtered, file_name='filtered_telemetry.csv', mime='text/csv')
            
        except Exception as e:
            st.error(f"System failure processing file: {e}")
    else:
        st.info("System standing by. Please inject CSV telemetry data to initialize.")