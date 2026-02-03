# High-Temperature Superconductor Experiment

## Overview

This project implements automated data acquisition and analysis for high-temperature superconductor characterization. The experiment measures phase-dependent lock-in amplifier responses and temperature-dependent resistance to identify superconducting transitions.

## Experiment Description

The setup uses GPIB-controlled instruments to perform two primary measurements:

1. **Phase Sweep**: The lock-in amplifier phase is swept from 1° to 400° while recording the output voltage and sample resistance. This characterizes the phase response of the sample in superconducting and non-superconducting states.

2. **Temperature Calibration**: Four-wire resistance measurements are used to calibrate temperature. The calibration uses known points at room temperature (~294 K) and liquid nitrogen temperature (77.4 K) to establish a linear resistance-to-temperature conversion.

## Hardware

- Digital multimeter (DMM) for four-wire resistance measurements
- Lock-in amplifier for phase-sensitive detection
- Function generator for AC excitation
- Prologix GPIB-USB adapter for instrument control

## Software Components

- `GPIB.py`: GPIB communication classes for DMM, lock-in amplifier, and function generator
- `DAQfuncs.py`: Data acquisition functions for phase sweeps and temperature-resistance measurements
- `TempCal.py`: Temperature calibration from resistance measurements
- `plottingfuncs.py`: Visualization functions for experimental data

## Data Files

- `csv/phase_sweep_data*.csv`: Phase sweep measurements
- `csv/temperature-resistance.csv`: Temperature calibration data

## Dependencies

- pandas
- matplotlib
- pyserial
