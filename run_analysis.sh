#!/bin/bash

# Pythia8 Hadronization Analysis Pipeline
# This script runs the complete analysis pipeline:
# 1. Generates hadronization events using Pythia8
# 2. Analyzes the momentum data
# 3. Creates visualization plots

set -e  # Exit on any error

echo "=========================================="
echo "Pythia8 Hadronization Analysis Pipeline"
echo "=========================================="

# Check if we're in the correct directory
if [ ! -f "main.cc" ] || [ ! -f "plot_momenta.py" ]; then
    echo "Error: Please run this script from the hadron directory containing main.cc and plot_momenta.py"
    exit 1
fi

# Check if the executable exists
if [ ! -f "hadron_simulation" ]; then
    echo "Error: hadron_simulation executable not found. Please compile main.cc first."
    echo "Run: g++ main.cc -o hadron_simulation \`pythia8-config --cxxflags --libs\`"
    exit 1
fi

# Activate conda environment
echo "Activating conda environment 'fcc'..."
# Use conda run to execute commands in the environment
CONDA_RUN="conda run -n fcc"

# Set Pythia8 data path
echo "Setting Pythia8 data path..."
export PYTHIA8DATA="$HOME/pythia8/share/Pythia8/xmldoc"

# Verify environment
echo "Verifying environment..."
if ! $CONDA_RUN python --version &> /dev/null; then
    echo "Error: Python not found in fcc environment"
    exit 1
fi

if ! command -v pythia8-config &> /dev/null; then
    echo "Error: pythia8-config not found. Check PATH."
    exit 1
fi

echo "Environment check passed."

# Step 1: Run hadronization simulation
echo ""
echo "=========================================="
echo "Step 1: Running hadronization simulation"
echo "=========================================="

echo "Generating 10 hadronization events..."
./hadron_simulation > simulation_output.log 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Simulation completed successfully"
else
    echo "✗ Simulation failed. Check simulation_output.log for details."
    exit 1
fi

# Check if momentum data was generated
if [ ! -f "momentum_data.csv" ]; then
    echo "✗ Error: momentum_data.csv was not generated"
    exit 1
fi

echo "✓ Momentum data saved to momentum_data.csv"

# Step 2: Run momentum analysis
echo ""
echo "=========================================="
echo "Step 2: Analyzing momentum distributions"
echo "=========================================="

echo "Running Python analysis script..."
$CONDA_RUN python plot_momenta.py > analysis_output.log 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Analysis completed successfully"
else
    echo "✗ Analysis failed. Check analysis_output.log for details."
    exit 1
fi

# Check if plots were generated
if [ ! -f "momentum_analysis.png" ]; then
    echo "✗ Error: momentum_analysis.png was not generated"
    exit 1
fi

echo "✓ Analysis plots saved to momentum_analysis.png"

# Step 3: Summary
echo ""
echo "=========================================="
echo "Pipeline completed successfully!"
echo "=========================================="

echo "Generated files:"
echo "  - momentum_data.csv: Raw momentum data"
echo "  - momentum_analysis.png: Analysis plots"
echo "  - simulation_output.log: Simulation log"
echo "  - analysis_output.log: Analysis log"

echo ""
echo "Summary of results:"
echo "  Events generated: $(grep -c "^Event [0-9]:" simulation_output.log 2>/dev/null || echo "N/A")"
echo "  Particles analyzed: $(wc -l < momentum_data.csv)"
echo "  Plot file size: $(ls -lh momentum_analysis.png | awk '{print $5}')"

echo ""
echo "To view the plots, open momentum_analysis.png in an image viewer."
echo "=========================================="