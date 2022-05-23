import streamlit as st
from hst import HST


def main():
    st.set_page_config(page_title='HSU Performance', page_icon='fav.png')
    st.title('Modeled HSU Performance')
    st.header('Inputs')
    oil = st.selectbox('Oil', ('SAE 15W40', 'SAE 5W30', 'SAE 30'))
    oil_temp = st.number_input('Oil temperature', 0, 100, 100, 10)
    hsu = HST(440, oil=oil, oil_temp=oil_temp)
    hsu.compute_sizes()
    speed_pump = st.number_input('Pump speed, rpm:', 100, 5000, 2025)
    pressure_charge = st.number_input('Charge pressure, bar:', 10, 50, 25)
    pressure_discharge = st.number_input('Discharge pressure, bar:', 40, 1000,
                                         472)
    hsu.compute_eff(speed_pump, pressure_discharge, pressure_charge)
    st.header('Pump')
    col1, col2, col3 = st.columns(3)
    col1.metric('Speed, rpm', f"{hsu.performance['pump']['speed']:.2f}")
    col2.metric('Torque, Nm', f"{hsu.performance['pump']['torque']:.2f}")
    col3.metric('Power, kW', f"{hsu.performance['pump']['power']:.2f}")
    st.header('Motor')
    col1, col2, col3 = st.columns(3)
    col1.metric('Speed, rpm', f"{hsu.performance['motor']['speed']:.2f}")
    col2.metric('Torque, Nm', f"{hsu.performance['motor']['torque']:.2f}")
    col3.metric('Power, kW', f"{hsu.performance['motor']['power']:.2f}")
    with st.expander('Show efficiencies'):
        st.header('Pump')
        col1, col2, col3 = st.columns(3)
        col1.metric('Volumetric, %',
                    f"{hsu.efficiencies['pump']['volumetric']:.2f}")
        col2.metric('Mechanical, %',
                    f"{hsu.efficiencies['pump']['mechanical']:.2f}")
        col3.metric('Total, %', f"{hsu.efficiencies['pump']['total']:.2f}")
        st.header('Motor')
        col1, col2, col3 = st.columns(3)
        col1.metric('Volumetric, %',
                    f"{hsu.efficiencies['motor']['volumetric']:.2f}")
        col2.metric('Mechanical, %',
                    f"{hsu.efficiencies['motor']['mechanical']:.2f}")
        col3.metric('Total, %', f"{hsu.efficiencies['motor']['total']:.2f}")
        st.header('HSU')
        col1, col2, col3 = st.columns(3)
        col1.metric('Volumetric, %',
                    f"{hsu.efficiencies['hst']['volumetric']:.2f}")
        col2.metric('Mechanical, %',
                    f"{hsu.efficiencies['hst']['mechanical']:.2f}")
        col3.metric('Total, %', f"{hsu.efficiencies['hst']['total']:.2f}")


if __name__ == "__main__":
    main()