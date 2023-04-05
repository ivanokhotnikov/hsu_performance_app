# HSU performance app

The repository contains the code for a [streamlit web app](https://hsu-performance.hydreco.uk) running at Google Cloud Platform. Given the hydro-mechanical inputs to the HSU (oil type, its temperature, pump speed, charge and discharge pressure), calculations of the HSU mechanical outputs (motor speed, torque and power) as well as of the missing input mechanical parameters (pump torque, power) are performed and displayed. The computations are performed with both volumetric and mechanical efficiencies being taken into account. The HSU max displacement is 440 cc/rev, its max swash angle is at 18&deg;. These max design parameters (displacement and swash angle) are not adjustable.

## Get started locally

### Set virtual environment
```
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip setuptools
```

### Install requirements
```
pip install -r requirements.txt
```

### Run app on localhost
```
streamlit run app.py
```