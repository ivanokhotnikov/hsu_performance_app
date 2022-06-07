import numpy as np
import pandas as pd
from joblib import load


class HST:
    """Creates the HST object.

    Attributes
    ----------
    displ: int
        The displacement of an axial-piston machine in cc/rev
    swash: int, optional
        The maxi swash angle of the axial piston machine in degrees, default 18 degrees when optional.
    pistons: int, optional
        The number of piston in a machine, default 9 when optional.
    oil: {'15w40', '5w30', '10w40'}, optional
        The oil choice from the dictionary of available oils, default '15w40'. Each oil is a dictionary with the following structure: {'visc_kin': float, 'density': float, 'visc_dyn': float, 'bulk': float}. Here 'visc_kin' is the kinematic viscosity of the oil in cSt, 'density' is its density in kg/cub.m, 'visc_dyn' is the dynamic viscosity in Pa s, 'bulk' is the oil bulk modulus in bar. All properties are at 100C.
    engine: {'engine_1', 'engine_2'}, optional
        The engine choice from the dictionary of engines, default 'engine_1'. Each engine is a dictionary with the following structure: {'speed': list, 'torque': list, 'power': list}. Lists must be of the same length.
    input_gear_ratio: float, optional
        The gear ratio of a gear train connecting the HST with an engine, default 0.75, which corresponds to a reduction gear set.
    max_power_input: int, optional
        The maximum mechanical power in kW the HST is meant to transmit, i.e. to take as an input, default 682 kW.
    """

    def __init__(self,
                 displ,
                 swash=18,
                 pistons=9,
                 oil='SAE 15W40',
                 oil_temp=100,
                 engine='engine_1',
                 input_gear_ratio=.75,
                 max_power_input=680):
        self.displ = displ
        self.swash = swash
        self.pistons = pistons
        self.oil = oil
        self.oil_temp = oil_temp
        self.oil_bulk = 15000
        self.engine = engine
        self.input_gear_ratio = input_gear_ratio
        self.max_power_input = max_power_input
        self.read_oil()

    def read_oil(self):
        """Loads oil data from GitHub repository"""
        self.oil_data = pd.read_csv(f'oils/{self.oil}.csv', index_col=0)

    def load_engines(self):
        """Loads the dictionary of available engines.

        For each key - engine name, the value is a dictionary with a performance curve and pivot speeds. A performance curve is in a form lists of engine speed in rpm, torque in Nm and power in kW.
        """
        return {
            'engine_1': {
                'speed': [
                    1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900,
                    2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900,
                    3000
                ],
                'torque': [
                    1350, 1450, 1550, 1650, 1800, 1975, 2200, 2450, 2750, 3100,
                    3100, 3100, 3100, 3022, 2944, 2849, 2757, 2654, 2200, 1800,
                    0
                ],
                'power': [
                    141.372, 167.028, 194.779, 224.624, 263.894, 310.232,
                    368.614, 436.158, 518.363, 616.799, 649.262, 681.726,
                    714.189, 727.865, 739.908, 745.866, 750.652, 750.401,
                    645.074, 546.637, 0
                ],
                'pivot speed':
                2700
            },
            'engine_2': {
                'speed': [
                    600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500,
                    1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400
                ],
                'torque': [
                    1000, 1100, 1450, 1750, 2100, 2400, 2600, 2950, 3100, 3300,
                    3400, 3500, 3400, 3300, 3200, 3000, 2800, 2600, 0
                ],
                'power': [
                    62.8319, 80.634, 121.475, 164.934, 219.911, 276.46,
                    326.726, 401.6, 454.484, 518.363, 569.675, 623.083,
                    640.885, 656.593, 670.206, 659.734, 645.074, 626.224, 0
                ],
                'pivot speed':
                2200
            },
            'engine_3': {
                'speed': [
                    1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700,
                    2800, 2900, 3000, 3100, 3200
                ],
                'torque': [
                    4270, 4458, 4558, 4439, 4350, 4250, 4144, 4033, 3891, 3703,
                    3459, 3183, 2817, 871
                ],
                'power': [
                    805, 887, 955, 994, 1023, 1048, 1068, 1085, 1098, 1100,
                    1086, 1050, 1000, 914, 292
                ],
                'pivot speed':
                2700
            },
            'engine_4': {
                'speed': [
                    1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900,
                    2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900,
                    3000
                ],
                'torque': [
                    1750, 1850, 2000, 2200, 2500, 2850, 3250, 3675, 4125, 4600,
                    4600, 4600, 4600, 4460, 4320, 4180, 4040, 3890, 3300, 2700,
                    0
                ],
                'power': [
                    183, 213, 251, 299, 366, 448, 544, 654, 777, 915, 963,
                    1011, 1059, 1074, 1085, 1094, 1099, 1099, 967, 820, 0
                ],
                'pivot speed':
                2700
            }
        }

    def compute_sizes(self, k1=.75, k2=.91, k3=.48, k4=.93, k5=.95):
        """Defines the basic sizes of the pumping group of an axial piston machine in metres. Updates the `sizes` attribute.

        Parameters
        ----------
        k1, k2, k3, k4, k5: float, optional
            Design balances, default k1 = .75, k2 = .91, k3 = .48, k4 = .93, k5 = .95

        """
        dia_piston = (4 * self.displ * 1e-6 * k1 /
                      (self.pistons**2 * np.tan(np.radians(self.swash))))**(1 /
                                                                            3)
        area_piston = np.pi * dia_piston**2 / 4
        pcd = self.pistons * dia_piston / (np.pi * k1)
        stroke = pcd * np.tan(np.radians(self.swash))
        min_engagement = 1.4 * dia_piston
        kidney_area = k3 * area_piston
        kidney_width = 2 * (np.sqrt(dia_piston**2 +
                                    (np.pi - 4) * kidney_area) -
                            dia_piston) / (np.pi - 4)
        land_width = k2 * self.pistons * area_piston / \
            (np.pi * pcd) - kidney_width
        rad_ext_int = (pcd + kidney_width) / 2
        rad_ext_ext = rad_ext_int + land_width
        rad_int_ext = (pcd - kidney_width) / 2
        rad_int_int = rad_int_ext - land_width
        area_shoe = k4 * area_piston / np.cos(np.radians(self.swash))
        rad_ext_shoe = np.pi * pcd * k5 / (2 * self.pistons)
        rad_int_shoe = np.sqrt(rad_ext_shoe**2 - area_shoe / np.pi)
        self.sizes = {
            'd': dia_piston,
            'Ap': area_piston,
            'D': pcd,
            'h': stroke,
            'eng': min_engagement,
            'rbo': rad_ext_int,
            'Rbo': rad_ext_ext,
            'Rbi': rad_int_ext,
            'rbi': rad_int_int,
            'rs': rad_int_shoe,
            'Rs': rad_ext_shoe
        }

    def compute_speed_limit(self):
        """Defines the pump speed limit."""
        reg_model = load('regression_models/pump_speed.joblib')
        self.pump_speed_limit = [
            reg_model.predict(self.displ) + i
            for i in (-reg_model.test_rmse_, 0, reg_model.test_rmse_)
        ]

    def compute_eff(self,
                    speed_pump,
                    pressure_discharge,
                    pressure_charge=25.0,
                    A=.17,
                    Bp=1.0,
                    Bm=.5,
                    Cp=.001,
                    Cm=.005,
                    D=125,
                    h1=20e-6,
                    h2=20e-6,
                    h3=20e-6,
                    eccentricity=1):
        """Defines efficiencies and performance characteristics of the HST made of same-displacement axial-piston machines.

        Parameters
        ----------
        speed_pump: int
            The HST input, or pump, speed in rpm.
        pressure_discharge: float
            The discharge pressures in bar.
        pressure_charge: float, optional
            The charge pressure in bar, default 25 bar.
        A, Bp, Bm, Cp, Cm, D: float, optional
            Coefficients in the efficiency model, default A = .17, Bp = 1.0, Bm = .5, Cp = .001, Cm = .005, D = 125.
        h1, h2, h3: float, optional
            Clearances in m, default h1 = 15e-6, h2 = 15e-6, h3 = 25e-6.
        eccentricity: float, optional
            Eccentricity ratio of a psiton in a bore, default 1.

        Returns
        --------
        out: dict
            The dictionary containing as values efficiencies of each machine as well as of HST in per cents. The dictionary structure is as following:
            {'pump': {'volumetric': float, 'mechanical': float, 'total': float},
            'motor': {'volumetric': float, 'mechanical': float, 'total': float},
            'hst': {'volumetric': float, 'mechanical': float, 'total': float}}
        """
        leak_block = np.pi * h1**3 * (
            pressure_discharge * np.ceil(self.pistons / 2) + pressure_charge *
            np.floor(self.pistons / 2)) * 1e5 / self.pistons * (
                1 / np.log(self.sizes['Rbo'] / self.sizes['rbo']) +
                1 / np.log(self.sizes['Rbi'] / self.sizes['rbi'])
            ) / (6 * self.oil_data.loc[self.oil_temp]['Dyn. Viscosity'] * 1e-3)
        leak_shoes = self.pistons * np.pi * h2**3 * (
            pressure_discharge * np.ceil(self.pistons / 2) + pressure_charge *
            np.floor(self.pistons / 2)) * 1e5 / self.pistons / (
                6 * self.oil_data.loc[self.oil_temp]['Dyn. Viscosity'] * 1e-3 *
                np.log(self.sizes['Rs'] / self.sizes['rs']))
        leak_piston = np.array([
            np.pi * self.sizes['d'] * h3**3 *
            (pressure_discharge * np.ceil(self.pistons / 2) +
             pressure_charge * np.floor(self.pistons / 2)) * 1e5 /
            self.pistons * (1 + 1.5 * eccentricity**3) *
            (1 / (self.sizes['eng'] +
                  self.sizes['h'] * np.sin(np.pi * (ii) / self.pistons))) /
            (12 * self.oil_data.loc[self.oil_temp]['Dyn. Viscosity'] * 1e-3)
            for ii in np.arange(self.pistons)
        ])
        leak_pistons = sum(leak_piston)
        leak_total = sum((leak_block, leak_shoes, leak_pistons))

        th_flow_rate_pump = speed_pump * self.displ / 6e7
        vol_pump = (1 -
                    (pressure_discharge - pressure_charge) / self.oil_bulk -
                    leak_total / th_flow_rate_pump) * 100
        vol_motor = (1 - leak_total / th_flow_rate_pump) * 100
        vol_hst = vol_pump * vol_motor * 1e-2
        mech_pump = (
            1 - A * np.exp(
                -Bp * self.oil_data.loc[self.oil_temp]['Dyn. Viscosity'] *
                speed_pump /
                (self.swash *
                 (pressure_discharge * 1e5 - pressure_charge * 1e5) * 1e-5)) -
            Cp * np.sqrt(self.oil_data.loc[self.oil_temp]['Dyn. Viscosity'] *
                         speed_pump /
                         (self.swash *
                          (pressure_discharge * 1e5 - pressure_charge * 1e5) *
                          1e-5)) - D /
            (self.swash *
             (pressure_discharge * 1e5 - pressure_charge * 1e5) * 1e-5)) * 100
        mech_motor = (
            1 - A * np.exp(
                -Bm * self.oil_data.loc[self.oil_temp]['Dyn. Viscosity'] *
                speed_pump * vol_hst * 1e-2 /
                (self.swash *
                 (pressure_discharge * 1e5 - pressure_charge * 1e5) * 1e-5)) -
            Cm * np.sqrt(self.oil_data.loc[self.oil_temp]['Dyn. Viscosity'] *
                         speed_pump * vol_hst * 1e-2 /
                         (self.swash *
                          (pressure_discharge * 1e5 - pressure_charge * 1e5) *
                          1e-5)) - D /
            (self.swash *
             (pressure_discharge * 1e5 - pressure_charge * 1e5) * 1e-5)) * 100
        mech_hst = mech_pump * mech_motor * 1e-2
        total_pump = vol_pump * mech_pump * 1e-2
        total_motor = vol_motor * mech_motor * 1e-2
        total_hst = total_pump * total_motor * 1e-2
        torque_pump = (pressure_discharge * 1e5 - pressure_charge * 1e5) * \
            self.displ * 1e-6 / (2 * np.pi * mech_pump * 1e-2)
        torque_motor = (pressure_discharge * 1e5 - pressure_charge * 1e5) * self.displ * \
            1e-6 / (2 * np.pi * mech_pump * 1e-2) * (mech_hst * 1e-2)
        power_pump = torque_pump * speed_pump * np.pi / 30 * 1e-3
        power_motor = power_pump * total_hst * 1e-2
        speed_motor = speed_pump * vol_hst * 1e-2
        self.performance = {
            'pump': {
                'speed': speed_pump,
                'torque': torque_pump,
                'power': power_pump
            },
            'motor': {
                'speed': speed_motor,
                'torque': torque_motor,
                'power': power_motor
            },
            'delta': {
                'speed': speed_pump - speed_motor,
                'torque': torque_pump - torque_motor,
                'power': power_pump - power_motor
            },
            'charge pressure': pressure_charge,
            'discharge pressure': pressure_discharge,
            'leakage': {
                'block': leak_block,
                'shoes': leak_shoes,
                'pistons': leak_pistons,
                'total': leak_total
            },
        }
        self.efficiencies = {
            'pump': {
                'volumetric': vol_pump,
                'mechanical': mech_pump,
                'total': total_pump
            },
            'motor': {
                'volumetric': vol_motor,
                'mechanical': mech_motor,
                'total': total_motor
            },
            'hst': {
                'volumetric': vol_hst,
                'mechanical': mech_hst,
                'total': total_hst
            }
        }

    def compute_loads(self, pressure_discharge, pressure_charge=25.0):
        """Calculates steady state, pressure-induced structural loads in the HST Forces in kN, torques in Nm.

        Parameters
        ----------
        pressure_discharge: float
            The discharge pressure in bar
        pressure_charge: float, optional
            The charge pressure in bar, default 25.0 bar.
        """
        self.shaft_radial = (np.ceil(self.pistons / 2) * pressure_discharge +
                             np.floor(self.pistons / 2) * pressure_charge
                             ) * 1e5 * self.sizes['Ap'] * np.tan(
                                 np.radians(self.swash)) / 1e3
        self.swash_hp_x = np.ceil(self.pistons / 2) * \
            pressure_discharge * 1e5 * self.sizes['Ap'] / 1e3
        self.swash_lp_x = np.floor(self.pistons / 2) * \
            pressure_charge * 1e5 * self.sizes['Ap'] / 1e3
        self.swash_hp_z = self.swash_hp_x * np.tan(np.radians(self.swash))
        self.swash_lp_z = self.swash_lp_x * np.tan(np.radians(self.swash))
        self.motor_hp = np.ceil(self.pistons / 2) * pressure_discharge * \
            1e5 * self.sizes['Ap'] / np.cos(np.radians(self.swash)) / 1e3
        self.motor_lp = np.floor(self.pistons / 2) * pressure_charge * \
            1e5 * self.sizes['Ap'] / np.cos(np.radians(self.swash)) / 1e3
        self.shaft_torque = self.performance['pump']['torque']

    def compute_control_flow(self):
        CONTROL_PISTON_DIA = 72.08e-3
        CONTROL_PISTON_STROKE = 144.26e-3
        DESTROKE_TIME = 0.8
        self.control_flow = np.pi * CONTROL_PISTON_DIA**2 / 4 * CONTROL_PISTON_STROKE / 2 / DESTROKE_TIME
