# EV_analysis
## Install dependencies

### Instal envEV virtual environment
Assuming an Anaconda Python distribution: 
Open Anaconda Prompt, navigate to the EV repo folder, and run

    python install_envEV.py

If Anaconda is not installed, install Anaconda.

## Activate EV

    conda activate envEV

## Update envEV
Make sure envEV is not active, if it is run

    conda deactivate

Rerun the installer script by running

    python install_envEV.py

## EV_app

### Run EV_app

    streamlit run EV_app.py

