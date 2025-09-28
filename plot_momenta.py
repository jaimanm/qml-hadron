#!/usr/bin/env python3
"""
Pythia Momentum Analysis and 3D Plotting Script

This script reads momentum data from Pythia8 hadronization simulation
and creates various momentum distribution plots including 3D visualizations.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec

def load_momentum_data(filename):
    """
    Load momentum data from CSV file.

    Returns:
        pandas.DataFrame: DataFrame containing momentum data
    """
    # Read the CSV file with proper column names
    column_names = ['Event', 'Particle_ID', 'px', 'py', 'pz', 'E', 'mass']
    df = pd.read_csv(filename, comment='#', names=column_names, header=None)

    # Calculate momentum magnitude
    df['p_mag'] = np.sqrt(df['px']**2 + df['py']**2 + df['pz']**2)

    return df

def create_momentum_plots(df):
    """
    Create various momentum distribution plots.
    """
    fig = plt.figure(figsize=(16, 12))
    gs = gridspec.GridSpec(3, 4, figure=fig)

    # Color map based on particle ID for consistency
    unique_ids = df['Particle_ID'].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_ids)))
    id_to_color = dict(zip(unique_ids, colors))

    # Particle ID labels
    id_labels = {
        211: 'π⁺', -211: 'π⁻', 321: 'K⁺', -321: 'K⁻',
        130: 'K_L⁰', 2212: 'p⁺', -2212: 'p̄⁻',
        2112: 'n⁰', -2112: 'n̄⁰'
    }

    # Plot 1: px distribution
    ax1 = fig.add_subplot(gs[0, 0])
    for pid in unique_ids:
        subset = df[df['Particle_ID'] == pid]
        label = id_labels.get(pid, f'ID:{pid}')
        ax1.hist(subset['px'], bins=20, alpha=0.7, label=label,
                color=id_to_color[pid], edgecolor='black', linewidth=0.5)
    ax1.set_xlabel('p_x (GeV/c)')
    ax1.set_ylabel('Count')
    ax1.set_title('x-Momentum Distribution')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3)

    # Plot 2: py distribution
    ax2 = fig.add_subplot(gs[0, 1])
    for pid in unique_ids:
        subset = df[df['Particle_ID'] == pid]
        label = id_labels.get(pid, f'ID:{pid}')
        ax2.hist(subset['py'], bins=20, alpha=0.7, label=label,
                color=id_to_color[pid], edgecolor='black', linewidth=0.5)
    ax2.set_xlabel('p_y (GeV/c)')
    ax2.set_ylabel('Count')
    ax2.set_title('y-Momentum Distribution')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.grid(True, alpha=0.3)

    # Plot 3: pz distribution
    ax3 = fig.add_subplot(gs[0, 2])
    for pid in unique_ids:
        subset = df[df['Particle_ID'] == pid]
        label = id_labels.get(pid, f'ID:{pid}')
        ax3.hist(subset['pz'], bins=20, alpha=0.7, label=label,
                color=id_to_color[pid], edgecolor='black', linewidth=0.5)
    ax3.set_xlabel('p_z (GeV/c)')
    ax3.set_ylabel('Count')
    ax3.set_title('z-Momentum Distribution')
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax3.grid(True, alpha=0.3)

    # Plot 4: Momentum magnitude distribution
    ax4 = fig.add_subplot(gs[0, 3])
    for pid in unique_ids:
        subset = df[df['Particle_ID'] == pid]
        label = id_labels.get(pid, f'ID:{pid}')
        ax4.hist(subset['p_mag'], bins=20, alpha=0.7, label=label,
                color=id_to_color[pid], edgecolor='black', linewidth=0.5)
    ax4.set_xlabel('|p| (GeV/c)')
    ax4.set_ylabel('Count')
    ax4.set_title('Momentum Magnitude Distribution')
    ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax4.grid(True, alpha=0.3)

    # Plot 5: 3D momentum scatter plot
    ax5 = fig.add_subplot(gs[1, :2], projection='3d')
    for pid in unique_ids:
        subset = df[df['Particle_ID'] == pid]
        label = id_labels.get(pid, f'ID:{pid}')
        ax5.scatter(subset['px'], subset['py'], subset['pz'],
                   c=[id_to_color[pid]], label=label, alpha=0.7, s=30)
    ax5.set_xlabel('p_x (GeV/c)')
    ax5.set_ylabel('p_y (GeV/c)')
    ax5.set_zlabel('p_z (GeV/c)')
    ax5.set_title('3D Momentum Distribution')
    ax5.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    # Plot 6: px vs py (transverse momentum plane)
    ax6 = fig.add_subplot(gs[1, 2])
    for pid in unique_ids:
        subset = df[df['Particle_ID'] == pid]
        label = id_labels.get(pid, f'ID:{pid}')
        ax6.scatter(subset['px'], subset['py'], c=[id_to_color[pid]],
                   label=label, alpha=0.7, s=30, edgecolors='black', linewidth=0.5)
    ax6.set_xlabel('p_x (GeV/c)')
    ax6.set_ylabel('p_y (GeV/c)')
    ax6.set_title('Transverse Momentum (p_x vs p_y)')
    ax6.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax6.grid(True, alpha=0.3)
    ax6.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax6.axvline(x=0, color='k', linestyle='--', alpha=0.3)

    # Plot 7: pz vs |p_T| (longitudinal vs transverse)
    ax7 = fig.add_subplot(gs[1, 3])
    df['p_T'] = np.sqrt(df['px']**2 + df['py']**2)  # Transverse momentum
    for pid in unique_ids:
        subset = df[df['Particle_ID'] == pid]
        label = id_labels.get(pid, f'ID:{pid}')
        ax7.scatter(subset['p_T'], subset['pz'], c=[id_to_color[pid]],
                   label=label, alpha=0.7, s=30, edgecolors='black', linewidth=0.5)
    ax7.set_xlabel('p_T (GeV/c)')
    ax7.set_ylabel('p_z (GeV/c)')
    ax7.set_title('Longitudinal vs Transverse Momentum')
    ax7.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax7.grid(True, alpha=0.3)
    ax7.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax7.axvline(x=0, color='k', linestyle='--', alpha=0.3)

    # Plot 8: Energy vs momentum magnitude
    ax8 = fig.add_subplot(gs[2, :2])
    for pid in unique_ids:
        subset = df[df['Particle_ID'] == pid]
        label = id_labels.get(pid, f'ID:{pid}')
        ax8.scatter(subset['p_mag'], subset['E'], c=[id_to_color[pid]],
                   label=label, alpha=0.7, s=30, edgecolors='black', linewidth=0.5)
    ax8.set_xlabel('|p| (GeV/c)')
    ax8.set_ylabel('E (GeV)')
    ax8.set_title('Energy vs Momentum Magnitude')
    ax8.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax8.grid(True, alpha=0.3)
    # Add E = |p| line for massless particles
    p_range = np.linspace(0, max(df['p_mag']), 100)
    ax8.plot(p_range, p_range, 'k--', alpha=0.5, label='E = |p| (massless)')

    # Plot 9: Mass distribution
    ax9 = fig.add_subplot(gs[2, 2])
    for pid in unique_ids:
        subset = df[df['Particle_ID'] == pid]
        label = id_labels.get(pid, f'ID:{pid}')
        ax9.hist(subset['mass'], bins=15, alpha=0.7, label=label,
                color=id_to_color[pid], edgecolor='black', linewidth=0.5)
    ax9.set_xlabel('Mass (GeV/c²)')
    ax9.set_ylabel('Count')
    ax9.set_title('Particle Mass Distribution')
    ax9.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax9.grid(True, alpha=0.3)

    # Plot 10: Event-by-event statistics
    ax10 = fig.add_subplot(gs[2, 3])
    event_stats = df.groupby('Event').agg({
        'px': lambda x: np.sqrt(np.sum(x**2)),  # Total p_x per event
        'py': lambda x: np.sqrt(np.sum(x**2)),  # Total p_y per event
        'pz': lambda x: np.sum(x),              # Total p_z per event (should be ~0)
        'E': 'sum'                              # Total energy per event
    })

    ax10.scatter(range(len(event_stats)), event_stats['pz'],
                alpha=0.7, s=50, edgecolors='black', linewidth=0.5)
    ax10.set_xlabel('Event Number')
    ax10.set_ylabel('Total p_z (GeV/c)')
    ax10.set_title('Total Longitudinal Momentum per Event')
    ax10.grid(True, alpha=0.3)
    ax10.axhline(y=0, color='r', linestyle='--', alpha=0.7, label='Expected (0)')
    ax10.legend()

    plt.tight_layout()
    plt.savefig('momentum_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def print_momentum_statistics(df):
    """
    Print detailed momentum statistics.
    """
    print("\n=== Momentum Analysis Statistics ===")
    print(f"Total particles analyzed: {len(df)}")
    print(f"Number of events: {df['Event'].nunique()}")

    print("\nMomentum component statistics (GeV/c):")
    for component in ['px', 'py', 'pz', 'p_mag']:
        values = df[component]
        print(f"  {component}: mean={values.mean():.3f}, std={values.std():.3f}, "
              f"min={values.min():.3f}, max={values.max():.3f}")

    print("\nPer-particle type statistics:")
    id_labels = {
        211: 'π⁺', -211: 'π⁻', 321: 'K⁺', -321: 'K⁻',
        130: 'K_L⁰', 2212: 'p⁺', -2212: 'p̄⁻',
        2112: 'n⁰', -2112: 'n̄⁰'
    }

    for pid in df['Particle_ID'].unique():
        subset = df[df['Particle_ID'] == pid]
        label = id_labels.get(pid, f'ID:{pid}')
        print(f"  {label}: {len(subset)} particles, "
              f"<|p|>={subset['p_mag'].mean():.3f} GeV/c")

    # Check momentum conservation
    total_momentum = df[['px', 'py', 'pz']].sum()
    print("\nTotal momentum conservation check:")
    print(f"  Σ p_x = {total_momentum['px']:.6f} GeV/c")
    print(f"  Σ p_y = {total_momentum['py']:.6f} GeV/c")
    print(f"  Σ p_z = {total_momentum['pz']:.6f} GeV/c")

def main():
    """Main function to run the momentum analysis."""
    filename = 'momentum_data.csv'

    try:
        # Load the momentum data
        print("Loading momentum data...")
        df = load_momentum_data(filename)
        print(f"Loaded data for {len(df)} particles from {df['Event'].nunique()} events")

        # Print statistics
        print_momentum_statistics(df)

        # Create plots
        print("Creating momentum plots...")
        create_momentum_plots(df)

        print("\nAnalysis complete! Plots saved as 'momentum_analysis.png'")

    except FileNotFoundError:
        print(f"Error: Could not find file '{filename}'")
        print("Make sure the momentum_data.csv file is in the current directory.")
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main()