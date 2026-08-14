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
# 2. INSPIRATION-DRIVEN SAAS CSS INJECTION
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    #MainMenu, header, footer {visibility: hidden;}
    
    /* Deep Immersive Obsidian Background with Ambient Glows */
    .stApp {
        background-color: #030712;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(0, 229, 255, 0.04) 0%, transparent 45%),
            radial-gradient(circle at 85% 85%, rgba(16, 185, 129, 0.03) 0%, transparent 45%);
        background-attachment: fixed;
    }
    
    /* Futuristic Typography Headings */
    h1 {
        background: linear-gradient(135deg, #FFFFFF 30%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -1.5px;
    }
    h2, h3 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    /* High-Contrast Distinct Sidebar */
    [data-testid="stSidebar"] {
        background-color: #080c14 !important;
        border-right: 2px solid rgba(0, 229, 255, 0.25) !important;
        box-shadow: 5px 0 25px rgba(0, 0, 0, 0.8);
    }
    
    /* Ensure sidebar text and navigation options are ultra-clear */
    [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {
        color: #F8FAFC !important;
    }
    
    /* Executive Bento Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, rgba(17, 24, 39, 0.8), rgba(11, 15, 25, 0.9));
        border: 1px solid rgba(0, 229, 255, 0.15);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        border-color: rgba(0, 229, 255, 0.4);
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0, 229, 255, 0.1);
    }
    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: linear-gradient(to bottom, #00E5FF, #2563EB);
    }
    
    /* High-Grade Glowing Action Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00E5FF 0%, #2563EB 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 700;
        letter-spacing: 0.5px;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 15px 35px rgba(0, 229, 255, 0.4);
    }
    
    /* Input Styling */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background-color: rgba(17, 24, 39, 0.7);
        color: #F8FAFC;
    }
    
    /* File Uploader Card */
    [data-testid="stFileUploadDropzone"] {
        background-color: rgba(17, 24, 39, 0.5);
        border: 2px dashed rgba(0, 229, 255, 0.3);
        border-radius: 16px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #00E5FF;
        background-color: rgba(0, 229, 255, 0.04);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("### 🌊 KNUST-01")
    st.caption("DEEPWATER SUBSEA ENGINE")
    st.divider()
    
    page = st.radio(
        "SYSTEM MODULES",
        ["Module A: Pipe Flow Analyser", 
         "Module B: Heat Transfer Calculator", 
         "Module C: Data Dashboard"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("Secured Subsea Telemetry v2.4")

# ==========================================
# 4. MAIN APP HEADER
# ==========================================
st.title("Fluid & Thermodynamic Analytics")
st.markdown("---")

# ==========================================
# PREMIUM CHART CONFIGURATION HELPER
# ==========================================
def apply_enterprise_chart_style(fig):
    fig.update_layout(
        font_family="Plus Jakarta Sans",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#94A3B8",
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', gridwidth=1, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', gridwidth=1, zeroline=False),
        margin=dict(l=20, r=20, t=40, b=20),
        hoverlabel=dict(bgcolor="#111827", font_size=13, font_family="Plus Jakarta Sans", bordercolor="rgba(0,229,255,0.2)")
    )
    return fig

# ==========================================
# MODULE A: PIPE FLOW ANALYSER
# ==========================================
if page == "Module A: Pipe Flow Analyser":
    st.header("Fluid Flow & Pipe Analyser")
    st.write("Simulate multi-phase fluid dynamics and pressure gradients across subsea infrastructure.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Fluid Characteristics")
        fluid_choice = st.selectbox("Select Fluid Medium", ["Water", "Air", "Crude Oil (Light)", "Custom"])
        
        if fluid_choice == "Water":
            rho, mu = 998.2, 1.002e-3
        elif fluid_choice == "Air":
            rho, mu = 1.204, 1.825e-5
        elif fluid_choice == "Crude Oil (Light)":
            rho, mu = 850.0, 1.500e-2
        else:
            rho = st.number_input("Density (kg/m³)", min_value=0.1, value=1000.0)
            mu = st.number_input("Dynamic Viscosity (Pa·s)", min_value=0.00001, value=0.001, format="%.5f")
            
        st.info(f"**Active Parameters:** Density: {rho} kg/m³ | Viscosity: {mu} Pa·s")
        current_fluid = Fluid(fluid_choice, rho, mu)

    with col2:
        st.subheader("2. Infrastructure Geometry")
        D = st.number_input("Pipe Diameter (m)", min_value=0.01, value=0.1)
        L = st.number_input("Pipe Length (m)", min_value=1.0, value=100.0)
        roughness = st.number_input("Absolute Roughness (m)", min_value=0.0, value=0.000045, format="%.6f")
        Q = st.number_input("Volumetric Flow Rate (m³/s)", min_value=0.0, value=0.05)
        
        current_pipe = Pipe(D, L, roughness)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Execute Flow Simulation"):
        try:
            vel = current_pipe.velocity(Q)
            re = current_pipe.reynolds_number(current_fluid, Q)
            f = current_pipe.friction_factor(current_fluid, Q)
            dp = current_pipe.pressure_drop(current_fluid, Q)
            
            st.markdown("<br>", unsafe_allow_html=True)
            r_col1, r_col2, r_col3, r_col4 = st.columns(4)
            r_col1.metric("Flow Velocity", f"{vel:.2f} m/s")
            r_col2.metric("Reynolds Number", f"{re:.0f}")
            r_col3.metric("Friction Factor", f"{f:.4f}")
            r_col4.metric("Pressure Drop", f"{dp/1000:.2f} kPa")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Pressure Gradient Trajectory")
            q_values = np.linspace(0.01, Q * 2, 50)
            dp_values = [current_pipe.pressure_drop(current_fluid, q) / 1000 for q in q_values]
            
            df_plot = pd.DataFrame({"Flow Rate (m³/s)": q_values, "Pressure Drop (kPa)": dp_values})
            fig = px.line(df_plot, x="Flow Rate (m³/s)", y="Pressure Drop (kPa)")
            
            fig.update_traces(
                line=dict(color='#00E5FF', width=3),
                fill='tozeroy',
                fillcolor='rgba(0, 229, 255, 0.08)'
            )
            fig = apply_enterprise_chart_style(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            csv = df_plot.to_csv(index=False).encode('utf-8')
            st.download_button(label="Export Simulation Matrix (CSV)", data=csv, file_name='pipe_flow_telemetry.csv', mime='text/csv')
            
        except Exception as e:
            st.error(f"Computation exception: {e}")

# ==========================================
# MODULE B: HEAT TRANSFER CALCULATOR
# ==========================================
elif page == "Module B: Heat Transfer Calculator":
    st.header("Thermal Analytics Engine")
    
    st.subheader("1. Steady-State Conduction Profiles")
    st.write("Fourier's Law heat flux modeling across single-layer structural boundaries.")
    
    c1, c2, c3 = st.columns(3)
    k = c1.number_input("Thermal Conductivity (W/m·K)", min_value=0.01, value=0.6)
    area = c2.number_input("Surface Area (m²)", min_value=0.1, value=10.0)
    thickness = c3.number_input("Barrier Thickness (m)", min_value=0.01, value=0.2)
    
    c4, c5 = st.columns(2)
    T_hot = c4.number_input("Hot Boundary Temp (°C)", value=30.0)
    T_cold = c5.number_input("Cold Boundary Temp (°C)", value=10.0)
    
    if st.button("Compute Conduction Flux"):
        q = fourier_conduction(k, area, thickness, T_hot, T_cold)
        st.success(f"**Steady-State Heat Transfer Rate:** {q:.2f} Watts")

    st.markdown("---")
    
    st.subheader("2. Transient Thermal Decay")
    st.write("Newton's Law of Cooling simulation framework.")
    
    nc1, nc2, nc3 = st.columns(3)
    T0 = nc1.slider("Initial Temperature (°C)", 0.0, 200.0, 100.0)
    T_inf = nc2.slider("Ambient Reference (°C)", 0.0, 50.0, 20.0)
    r = nc3.slider("Decay Constant (1/s)", 0.001, 0.1, 0.05, step=0.001)
    
    t_max = st.slider("Horizon Duration (s)", 10, 300, 100)
    times = np.linspace(0, t_max, 100)
    temps = newtons_cooling(T0, T_inf, r, times)
    
    df_cooling = pd.DataFrame({"Time (s)": times, "Temperature (°C)": temps})
    fig2 = px.line(df_cooling, x="Time (s)", y="Temperature (°C)")
    
    fig2.update_traces(
        line=dict(color='#F43F5E', width=3),
        fill='tozeroy',
        fillcolor='rgba(244, 63, 94, 0.08)'
    )
    fig2.add_hline(y=T_inf, line_dash="dash", line_color="#00E5FF", annotation_text="Ambient Equilibrum", annotation_font_color="#00E5FF")
    fig2 = apply_enterprise_chart_style(fig2)
    
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# MODULE C: ROCK & FLUID DATA DASHBOARD
# ==========================================
elif page == "Module C: Data Dashboard":
    st.header("Reservoir Telemetry Dashboard")
    st.write("Ingest multivariate datasets for cluster mapping and performance analytics.")
    
    uploaded_file = st.file_uploader("Upload Telemetry Feed (CSV)", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Telemetry link established successfully.")
            
            st.subheader("Stream Snapshot")
            st.dataframe(df.head(), use_container_width=True)
            
            st.markdown("---")
            
            cols = df.columns.tolist()
            st.subheader("Multivariate Filtering Matrix")
            
            filter_col = st.selectbox("Primary Target Parameter:", cols)
            min_val = float(df[filter_col].min())
            max_val = float(df[filter_col].max())
            
            cutoff = st.slider(f"Threshold Limit ({filter_col})", min_val, max_val, min_val)
            filtered_df = df[df[filter_col] >= cutoff]
            
            st.caption(f"Active Nodes: {len(filtered_df)} of {len(df)} records verified.")
            
            if len(cols) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    hist_fig = px.histogram(filtered_df, x=filter_col, title=f"Frequency Dist: {filter_col}")
                    hist_fig.update_traces(marker_color='#2563EB', marker_line_color='#030712', marker_line_width=1, opacity=0.85)
                    hist_fig = apply_enterprise_chart_style(hist_fig)
                    st.plotly_chart(hist_fig, use_container_width=True)
                    
                with col2:
                    x_axis = st.selectbox("X-Axis Vector", cols, index=0)
                    y_axis = st.selectbox("Y-Axis Vector", cols, index=1 if len(cols)>1 else 0)
                    scatter_fig = px.scatter(filtered_df, x=x_axis, y=y_axis, title=f"Cross-Plot: {y_axis} vs {x_axis}")
                    scatter_fig.update_traces(marker=dict(size=8, color='#00E5FF', line=dict(width=1, color='#FFFFFF')))
                    scatter_fig = apply_enterprise_chart_style(scatter_fig)
                    st.plotly_chart(scatter_fig, use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            csv_filtered = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Export Filtered Matrix", data=csv_filtered, file_name='filtered_reservoir_data.csv', mime='text/csv')
            
        except Exception as e:
            st.error(f"Telemetry decoding error: {e}")
    else:
        st.info("System standing by. Awaiting telemetry injection...")