import streamlit as st
from hst import HST

st.set_page_config(page_title='HSU Performance', page_icon='fav.png')


def main():
    st.title('Modeled HSU Performance')
    with st.sidebar:
        st.header('Inputs')
        oil = st.selectbox('Oil', ('SAE 15W40', 'SAE 5W30', 'SAE 30'))
        oil_temp = st.number_input('Oil temperature', 0, 100, 100, 10)
        hsu = HST(440, oil=oil, oil_temp=oil_temp)
        hsu.compute_sizes()
        speed_pump = st.number_input('Pump speed, rpm:', 100, 5000, 2025)
        pressure_charge = st.number_input('Charge pressure, bar:', 10, 50, 25)
        pressure_discharge = st.number_input('Discharge pressure, bar:', 40,
                                             1000, 472)
    hsu.compute_eff(speed_pump, pressure_discharge, pressure_charge)
    hsu.compute_control_flow()
    st.header('HSU Performance')
    st.subheader('Pump')
    col1, col2, col3 = st.columns(3)
    col1.metric('Speed, rpm', f"{hsu.performance['pump']['speed']:.2f}")
    col2.metric('Torque, Nm', f"{hsu.performance['pump']['torque']:.2f}")
    col3.metric('Power, kW', f"{hsu.performance['pump']['power']:.2f}")
    st.subheader('Motor')
    col1, col2, col3 = st.columns(3)
    col1.metric('Speed, rpm', f"{hsu.performance['motor']['speed']:.2f}")
    col2.metric('Torque, Nm', f"{hsu.performance['motor']['torque']:.2f}")
    col3.metric('Power, kW', f"{hsu.performance['motor']['power']:.2f}")
    st.header('Efficiencies')
    st.subheader('Pump')
    col1, col2, col3 = st.columns(3)
    col1.metric('Volumetric, %',
                f"{hsu.efficiencies['pump']['volumetric']:.2f}")
    col2.metric('Mechanical, %',
                f"{hsu.efficiencies['pump']['mechanical']:.2f}")
    col3.metric('Total, %', f"{hsu.efficiencies['pump']['total']:.2f}")
    st.subheader('Motor')
    col1, col2, col3 = st.columns(3)
    col1.metric('Volumetric, %',
                f"{hsu.efficiencies['motor']['volumetric']:.2f}")
    col2.metric('Mechanical, %',
                f"{hsu.efficiencies['motor']['mechanical']:.2f}")
    col3.metric('Total, %', f"{hsu.efficiencies['motor']['total']:.2f}")
    st.subheader('HSU')
    col1, col2, col3 = st.columns(3)
    col1.metric('Volumetric, %',
                f"{hsu.efficiencies['hst']['volumetric']:.2f}")
    col2.metric('Mechanical, %',
                f"{hsu.efficiencies['hst']['mechanical']:.2f}")
    col3.metric('Total, %', f"{hsu.efficiencies['hst']['total']:.2f}")
    st.header('Leakages')
    st.subheader('Pump/Motor')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Block, lpm', f"{hsu.performance['leakage']['block']*6e4:.2f}")
    col2.metric('Shoes, lpm', f"{hsu.performance['leakage']['shoes']*6e4:.2f}")
    col3.metric('Pistons, lpm',
                f"{hsu.performance['leakage']['pistons']*6e4:.2f}")
    col4.metric('Total, lpm', f"{hsu.performance['leakage']['total']*6e4:.2f}")
    st.subheader('HSU')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Block, lpm',
                f"{hsu.performance['leakage']['block']*6e4*2:.2f}")
    col2.metric('Shoes, lpm',
                f"{hsu.performance['leakage']['shoes']*6e4*2:.2f}")
    col3.metric('Pistons, lpm',
                f"{hsu.performance['leakage']['pistons']*6e4*2:.2f}")
    col4.metric('Total, lpm',
                f"{hsu.performance['leakage']['total']*6e4*2:.2f}")
    st.header('Charge flow')
    col1, col2, col3 = st.columns(3)
    col1.metric('Continuous, lpm',
                f"{hsu.performance['leakage']['total']*6e4*2:.2f}")
    col2.metric('Control, lpm', f"{hsu.control_flow*6e4*2:.2f}")
    col3.metric(
        'Transient, lpm',
        f"{(hsu.performance['leakage']['total']*2 + hsu.control_flow)*6e4:.2f}"
    )


if __name__ == "__main__":
    main()