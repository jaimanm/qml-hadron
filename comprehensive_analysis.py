#!/usr/bin/env python3
"""
Comprehensive Pythia8 Particle Analysis Script

This script performs complete analysis of Pythia8 hadronization data,
creating organized plots in separate files for better visualization.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
import seaborn as sns
import os

def load_particle_data(filename):
    """
    Load particle data from CSV file with derived quantities.

    Returns:
        pandas.DataFrame: DataFrame containing particle data
    """
    # Read the CSV file with proper column names
    column_names = ['Event', 'Particle_ID', 'px', 'py', 'pz', 'E', 'mass']
    df = pd.read_csv(filename, comment='#', names=column_names, header=None)

    # Calculate derived quantities
    df['p_mag'] = np.sqrt(df['px']**2 + df['py']**2 + df['pz']**2)  # momentum magnitude
    df['p_trans'] = np.sqrt(df['px']**2 + df['py']**2)  # transverse momentum
    df['eta'] = 0.5 * np.log((df['p_mag'] + df['pz']) / (df['p_mag'] - df['pz'] + 1e-10))  # pseudorapidity
    df['pt'] = df['p_trans']  # alias for clarity

    return df

def create_momentum_distributions(df, plots_dir):
    """
    Create momentum distribution plots.
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

    # Set style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")

    # Plot 1: px distribution
    ax1.hist(df['px'], bins=50, alpha=0.7, color='blue', edgecolor='black')
    ax1.set_xlabel('p_x (GeV/c)')
    ax1.set_ylabel('Count')
    ax1.set_title('p_x Distribution')
    ax1.grid(True, alpha=0.3)

    # Plot 2: py distribution
    ax2.hist(df['py'], bins=50, alpha=0.7, color='red', edgecolor='black')
    ax2.set_xlabel('p_y (GeV/c)')
    ax2.set_ylabel('Count')
    ax2.set_title('p_y Distribution')
    ax2.grid(True, alpha=0.3)

    # Plot 3: pz distribution
    ax3.hist(df['pz'], bins=50, alpha=0.7, color='green', edgecolor='black')
    ax3.set_xlabel('p_z (GeV/c)')
    ax3.set_ylabel('Count')
    ax3.set_title('p_z Distribution')
    ax3.grid(True, alpha=0.3)

    # Plot 4: |p| distribution
    ax4.hist(df['p_mag'], bins=50, alpha=0.7, color='purple', edgecolor='black')
    ax4.set_xlabel('|p| (GeV/c)')
    ax4.set_ylabel('Count')
    ax4.set_title('Momentum Magnitude Distribution')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    fig.savefig(f'{plots_dir}/momentum_components.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Saved momentum distributions to {plots_dir}/momentum_components.png")

def create_energy_mass_distributions(df, plots_dir):
    """
    Create energy and mass distribution plots.
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

    # Energy distribution
    ax1.hist(df['E'], bins=50, alpha=0.7, color='blue', edgecolor='black')
    ax1.set_xlabel('Energy (GeV)')
    ax1.set_ylabel('Count')
    ax1.set_title('Energy Distribution')
    ax1.grid(True, alpha=0.3)

    # Mass distribution
    ax2.hist(df['mass'], bins=30, alpha=0.7, color='red', edgecolor='black')
    ax2.set_xlabel('Mass (GeV/c²)')
    ax2.set_ylabel('Count')
    ax2.set_title('Mass Distribution')
    ax2.grid(True, alpha=0.3)

    # Transverse momentum
    ax3.hist(df['pt'], bins=50, alpha=0.7, color='green', edgecolor='black')
    ax3.set_xlabel('p_T (GeV/c)')
    ax3.set_ylabel('Count')
    ax3.set_title('Transverse Momentum Distribution')
    ax3.grid(True, alpha=0.3)

    # Pseudorapidity
    ax4.hist(df['eta'], bins=50, alpha=0.7, color='purple', edgecolor='black')
    ax4.set_xlabel('Pseudorapidity η')
    ax4.set_ylabel('Count')
    ax4.set_title('Pseudorapidity Distribution')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    fig.savefig(f'{plots_dir}/energy_mass_distributions.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Saved energy/mass distributions to {plots_dir}/energy_mass_distributions.png")

def create_correlation_plots(df, plots_dir):
    """
    Create correlation plots between different properties.
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))

    # Energy vs Mass
    scatter1 = ax1.scatter(df['mass'], df['E'], alpha=0.6, c=df['p_mag'], cmap='viridis', s=30)
    ax1.set_xlabel('Mass (GeV/c²)')
    ax1.set_ylabel('Energy (GeV)')
    ax1.set_title('Energy vs Mass')
    ax1.grid(True, alpha=0.3)
    plt.colorbar(scatter1, ax=ax1, label='|p| (GeV/c)')

    # Energy vs Momentum Magnitude
    scatter2 = ax2.scatter(df['p_mag'], df['E'], alpha=0.6, c=df['mass'], cmap='plasma', s=30)
    ax2.set_xlabel('Momentum Magnitude (GeV/c)')
    ax2.set_ylabel('Energy (GeV)')
    ax2.set_title('Energy vs |p|')
    ax2.grid(True, alpha=0.3)
    plt.colorbar(scatter2, ax=ax2, label='Mass (GeV/c²)')

    # Mass vs Transverse Momentum
    scatter3 = ax3.scatter(df['pt'], df['mass'], alpha=0.6, c=df['E'], cmap='coolwarm', s=30)
    ax3.set_xlabel('Transverse Momentum (GeV/c)')
    ax3.set_ylabel('Mass (GeV/c²)')
    ax3.set_title('Mass vs p_T')
    ax3.grid(True, alpha=0.3)
    plt.colorbar(scatter3, ax=ax3, label='Energy (GeV)')

    # 3D plot: Energy, Mass, Momentum
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    scatter4 = ax4.scatter(df['mass'], df['p_mag'], df['E'],
                          c=df['pt'], cmap='rainbow', alpha=0.7, s=40)
    ax4.set_xlabel('Mass (GeV/c²)')
    ax4.set_ylabel('|p| (GeV/c)')
    ax4.set_zlabel('Energy (GeV)')
    ax4.set_title('3D: Mass, |p|, Energy')
    plt.colorbar(scatter4, ax=ax4, label='p_T (GeV/c)', shrink=0.8)

    plt.tight_layout()
    fig.savefig(f'{plots_dir}/property_correlations.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Saved correlation plots to {plots_dir}/property_correlations.png")

def create_particle_type_analysis(df, plots_dir):
    """
    Create particle type specific analysis plots.
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))

    # Particle type labels
    particle_labels = {
        211: 'pi+', -211: 'pi-', 321: 'K+', -321: 'K-',
        130: 'K0', 2212: 'proton', -2212: 'antiproton',
        2112: 'neutron', -2112: 'antineutron'
    }

    # Plot 1: Particle type distribution (pie chart)
    particle_counts = df['Particle_ID'].value_counts()
    labels = [particle_labels.get(pid, f'ID:{pid}') for pid in particle_counts.index]
    ax1.pie(particle_counts.values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Particle Type Distribution')

    # Plot 2: Energy by particle type (box plot)
    df_plot = df.copy()
    df_plot['Particle'] = df_plot['Particle_ID'].map(particle_labels).fillna(df_plot['Particle_ID'].astype(str))
    sns.boxplot(data=df_plot, x='Particle', y='E', ax=ax2)
    ax2.set_xlabel('Particle Type')
    ax2.set_ylabel('Energy (GeV)')
    ax2.set_title('Energy Distribution by Particle Type')
    ax2.tick_params(axis='x', rotation=45)

    # Plot 3: Mass by particle type
    sns.boxplot(data=df_plot, x='Particle', y='mass', ax=ax3)
    ax3.set_xlabel('Particle Type')
    ax3.set_ylabel('Mass (GeV/c²)')
    ax3.set_title('Mass Distribution by Particle Type')
    ax3.tick_params(axis='x', rotation=45)

    # Plot 4: Momentum magnitude by particle type
    sns.boxplot(data=df_plot, x='Particle', y='p_mag', ax=ax4)
    ax4.set_xlabel('Particle Type')
    ax4.set_ylabel('|p| (GeV/c)')
    ax4.set_title('Momentum Distribution by Particle Type')
    ax4.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    fig.savefig(f'{plots_dir}/particle_type_analysis.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Saved particle type analysis to {plots_dir}/particle_type_analysis.png")

def create_3d_momentum_visualization(df, plots_dir):
    """
    Create 3D momentum space visualization with particle names.
    """
    fig = plt.figure(figsize=(12, 10))

    # Create 3D subplot
    ax = fig.add_subplot(111, projection='3d')

    # Particle name mapping
    particle_labels = {
        211: 'pi+', -211: 'pi-', 321: 'K+', -321: 'K-',
        130: 'K0', 2212: 'proton', -2212: 'antiproton',
        2112: 'neutron', -2112: 'antineutron'
    }

    # Color by particle type
    particle_ids = df['Particle_ID'].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(particle_ids)))
    id_to_color = dict(zip(particle_ids, colors))

    # Plot each particle type with different color
    for pid in particle_ids:
        mask = df['Particle_ID'] == pid
        particle_data = df[mask]
        color = id_to_color[pid]
        particle_name = particle_labels.get(pid, f'ID:{pid}')
        ax.scatter(particle_data['px'], particle_data['py'], particle_data['pz'],
                  c=[color], label=particle_name, alpha=0.7, s=50)

    ax.set_xlabel('p_x (GeV/c)')
    ax.set_ylabel('p_y (GeV/c)')
    ax.set_zlabel('p_z (GeV/c)')
    ax.set_title('3D Momentum Space Distribution')

    # Add legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    fig.savefig(f'{plots_dir}/momentum_3d_visualization.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Saved 3D momentum visualization to {plots_dir}/momentum_3d_visualization.png")

    # Return the figure for interactive display
    return fig

def create_correlation_matrix(df, plots_dir):
    """
    Create correlation matrix heatmap.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Select numerical columns for correlation
    numeric_cols = ['px', 'py', 'pz', 'E', 'mass', 'p_mag', 'pt', 'eta']
    corr_matrix = df[numeric_cols].corr()

    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, ax=ax, cbar_kws={'shrink': 0.8})
    ax.set_title('Property Correlation Matrix')

    plt.tight_layout()
    fig.savefig(f'{plots_dir}/correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Saved correlation matrix to {plots_dir}/correlation_matrix.png")

def print_statistics(df):
    """
    Print comprehensive statistical summary.
    """
    print("=" * 70)
    print("COMPREHENSIVE PARTICLE PROPERTIES STATISTICS")
    print("=" * 70)

    print(f"\nTotal particles: {len(df)}")
    print(f"Total events: {df['Event'].nunique()}")

    print(f"\nMOMENTUM STATISTICS:")
    print(f"  p_x Mean: {df['px'].mean():.3f} GeV/c")
    print(f"  p_y Mean: {df['py'].mean():.3f} GeV/c")
    print(f"  p_z Mean: {df['pz'].mean():.3f} GeV/c")
    print(f"  |p| Mean: {df['p_mag'].mean():.3f} GeV/c")
    print(f"  p_T Mean: {df['pt'].mean():.3f} GeV/c")

    print(f"\nENERGY STATISTICS:")
    print(f"  Mean: {df['E'].mean():.3f} GeV")
    print(f"  Std:  {df['E'].std():.3f} GeV")
    print(f"  Min:  {df['E'].min():.3f} GeV")
    print(f"  Max:  {df['E'].max():.3f} GeV")

    print(f"\nMASS STATISTICS:")
    print(f"  Mean: {df['mass'].mean():.3f} GeV/c²")
    print(f"  Std:  {df['mass'].std():.3f} GeV/c²")
    print(f"  Min:  {df['mass'].min():.3f} GeV/c²")
    print(f"  Max:  {df['mass'].max():.3f} GeV/c²")

    # Particle type breakdown
    print(f"\nPARTICLE TYPE BREAKDOWN:")
    particle_counts = df['Particle_ID'].value_counts()
    particle_labels = {
        211: 'pi+', -211: 'pi-', 321: 'K+', -321: 'K-',
        130: 'K0', 2212: 'proton', -2212: 'antiproton',
        2112: 'neutron', -2112: 'antineutron'
    }

    for pid, count in particle_counts.items():
        label = particle_labels.get(pid, f'ID:{pid}')
        percentage = (count / len(df)) * 100
        print(f"  {label}: {count} ({percentage:.1f}%)")

    # Correlation analysis
    print(f"\nKEY CORRELATIONS:")
    corr_em = df['E'].corr(df['mass'])
    corr_ep = df['E'].corr(df['p_mag'])
    corr_mp = df['mass'].corr(df['p_mag'])
    corr_et = df['E'].corr(df['pt'])

    print(f"  Energy-Mass: {corr_em:.3f}")
    print(f"  Energy-Momentum: {corr_ep:.3f}")
    print(f"  Mass-Momentum: {corr_mp:.3f}")
    print(f"  Energy-p_T: {corr_et:.3f}")

def main():
    """
    Main function to run comprehensive analysis.
    """
    filename = 'momentum_data.csv'
    plots_dir = 'plots'

    # Ensure plots directory exists
    os.makedirs(plots_dir, exist_ok=True)

    try:
        # Load data
        print("Loading particle data...")
        df = load_particle_data(filename)
        print(f"Loaded {len(df)} particles from {df['Event'].nunique()} events")

        # Print statistics
        print_statistics(df)

        # Create all analysis plots
        print("\n" + "="*50)
        print("GENERATING ANALYSIS PLOTS")
        print("="*50)

        create_momentum_distributions(df, plots_dir)
        create_energy_mass_distributions(df, plots_dir)
        create_correlation_plots(df, plots_dir)
        create_particle_type_analysis(df, plots_dir)
        create_3d_momentum_visualization(df, plots_dir)
        create_correlation_matrix(df, plots_dir)

        print("\n" + "="*50)
        print("ANALYSIS COMPLETE!")
        print("="*50)
        print(f"All plots saved to: {plots_dir}/")
        print("\nGenerated plot files:")
        plot_files = [
            "momentum_components.png - Individual momentum component distributions",
            "energy_mass_distributions.png - Energy, mass, p_T, and η distributions",
            "property_correlations.png - Scatter plots showing relationships between properties",
            "particle_type_analysis.png - Particle composition and property distributions by type",
            "momentum_3d_visualization.png - 3D momentum space visualization",
            "correlation_matrix.png - Correlation heatmap of all numerical properties"
        ]
        for plot_file in plot_files:
            print(f"  • {plot_file}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        print("Please run the simulation first to generate the data.")
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main()