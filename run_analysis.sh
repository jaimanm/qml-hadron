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
if [ ! -f "main.cc" ] || [ ! -f "comprehensive_analysis.py" ]; then
    echo "Error: Please run this script from the hadron directory containing main.cc and comprehensive_analysis.py"
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

# Step 2: Run comprehensive analysis
echo ""
echo "=========================================="
echo "Step 2: Running comprehensive analysis"
echo "=========================================="

echo "Running comprehensive analysis script..."
$CONDA_RUN python comprehensive_analysis.py > comprehensive_analysis.log 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Comprehensive analysis completed successfully"
else
    echo "✗ Analysis failed. Check comprehensive_analysis.log for details."
    exit 1
fi

# Check if plots directory and files were generated
if [ ! -d "plots" ]; then
    echo "✗ Error: plots directory was not created"
    exit 1
fi

plot_count=$(ls plots/*.png 2>/dev/null | wc -l)
if [ "$plot_count" -lt 6 ]; then
    echo "✗ Error: Expected 6 plot files, found $plot_count"
    exit 1
fi

echo "✓ Analysis plots saved to plots/ directory ($plot_count files generated)"

# Step 3: Summary
echo ""
echo "=========================================="
echo "Pipeline completed successfully!"
echo "=========================================="

echo "Generated files:"
echo "  - momentum_data.csv: Raw momentum data"
echo "  - plots/momentum_components.png: Individual momentum distributions"
echo "  - plots/energy_mass_distributions.png: Energy, mass, p_T, η distributions"
echo "  - plots/property_correlations.png: Property correlation scatter plots"
echo "  - plots/particle_type_analysis.png: Particle composition analysis"
echo "  - plots/momentum_3d_visualization.png: 3D momentum space visualization"
echo "  - plots/correlation_matrix.png: Property correlation heatmap"
echo "  - simulation_output.log: Simulation log"
echo "  - comprehensive_analysis.log: Analysis log"

echo ""
echo "Summary of results:"
echo "  Events generated: $(grep -c "^Event [0-9]:" simulation_output.log 2>/dev/null || echo "N/A")"
echo "  Particles analyzed: $(wc -l < momentum_data.csv)"
echo "  Plot files generated: $(ls plots/*.png 2>/dev/null | wc -l)"

echo ""
echo "To view the plots, open the files in the plots/ directory:"
echo "  - momentum_components.png"
echo "  - energy_mass_distributions.png"
echo "  - property_correlations.png"
echo "  - particle_type_analysis.png"
echo "  - momentum_3d_visualization.png"
echo "  - correlation_matrix.png"
echo "=========================================="