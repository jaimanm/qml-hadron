#!/usr/bin/env python3
"""
First Hadron Analysis Script

This script analyzes the first hadron emitted in each Pythia8 hadronization event,
creating comprehensive plots and statistics.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.gridspec as gridspec
import seaborn as sns
import os

def load_first_hadron_data(filename):
    """
    Load first hadron data from CSV file with derived quantities.

    Returns:
        pandas.DataFrame: DataFrame containing first hadron data
    """
    df = pd.read_csv(filename)

    # Calculate derived quantities
    df['p_mag'] = np.sqrt(df['px']**2 + df['py']**2 + df['pz']**2)  # momentum magnitude
    df['p_trans'] = np.sqrt(df['px']**2 + df['py']**2)  # transverse momentum
    df['eta'] = 0.5 * np.log((df['p_mag'] + df['pz']) / (df['p_mag'] - df['pz'] + 1e-10))  # pseudorapidity
    df['pt'] = df['p_trans']  # alias for clarity

    return df

def create_particle_type_analysis(df, plots_dir):
    """
    Create particle type specific analysis plots for first hadrons.
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))

    # Particle type labels (using ASCII for consistency)
    particle_labels = {
        111: 'pi0', -211: 'pi-', 211: 'pi+', 311: 'K0', -311: 'Kbar0',
        313: 'K*0', -313: 'K*bar0', 2112: 'neutron', -2112: 'antineutron',
        -213: 'rho-', 223: 'omega', 113: 'rho0', 213: 'rho+',
        3322: 'Xi0', -3122: 'Lambdabar0', -2214: 'Deltabar-', 2212: 'proton'
    }

    # Plot 1: First hadron type distribution (pie chart)
    particle_counts = df['ID'].value_counts()
    labels = [particle_labels.get(pid, f'ID:{pid}') for pid in particle_counts.index]
    ax1.pie(particle_counts.values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.set_title('First Hadron Type Distribution')

    # Plot 2: Energy by first hadron type (box plot)
    df_plot = df.copy()
    df_plot['Particle'] = df_plot['ID'].map(particle_labels).fillna(df_plot['ID'].astype(str))
    sns.boxplot(data=df_plot, x='Particle', y='E', ax=ax2)
    ax2.set_xlabel('First Hadron Type')
    ax2.set_ylabel('Energy (GeV)')
    ax2.set_title('Energy Distribution by First Hadron Type')
    ax2.tick_params(axis='x', rotation=45)

    # Plot 3: Mass by first hadron type
    sns.boxplot(data=df_plot, x='Particle', y='m', ax=ax3)
    ax3.set_xlabel('First Hadron Type')
    ax3.set_ylabel('Mass (GeV/c²)')
    ax3.set_title('Mass Distribution by First Hadron Type')
    ax3.tick_params(axis='x', rotation=45)

    # Plot 4: Momentum magnitude by first hadron type
    sns.boxplot(data=df_plot, x='Particle', y='p_mag', ax=ax4)
    ax4.set_xlabel('First Hadron Type')
    ax4.set_ylabel('|p| (GeV/c)')
    ax4.set_title('Momentum Distribution by First Hadron Type')
    ax4.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    fig.savefig(f'{plots_dir}/first_hadron_types.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Saved first hadron type analysis to {plots_dir}/first_hadron_types.png")

def create_momentum_analysis(df, plots_dir):
    """
    Create momentum-related plots for first hadrons.
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

    # Set style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")

    # Plot 1: px distribution
    ax1.hist(df['px'], bins=20, alpha=0.7, color='blue', edgecolor='black')
    ax1.set_xlabel('p_x (GeV/c)')
    ax1.set_ylabel('Count')
    ax1.set_title('First Hadron p_x Distribution')
    ax1.grid(True, alpha=0.3)

    # Plot 2: py distribution
    ax2.hist(df['py'], bins=20, alpha=0.7, color='red', edgecolor='black')
    ax2.set_xlabel('p_y (GeV/c)')
    ax2.set_ylabel('Count')
    ax2.set_title('First Hadron p_y Distribution')
    ax2.grid(True, alpha=0.3)

    # Plot 3: pz distribution
    ax3.hist(df['pz'], bins=20, alpha=0.7, color='green', edgecolor='black')
    ax3.set_xlabel('p_z (GeV/c)')
    ax3.set_ylabel('Count')
    ax3.set_title('First Hadron p_z Distribution')
    ax3.grid(True, alpha=0.3)

    # Plot 4: |p| distribution
    ax4.hist(df['p_mag'], bins=20, alpha=0.7, color='purple', edgecolor='black')
    ax4.set_xlabel('|p| (GeV/c)')
    ax4.set_ylabel('Count')
    ax4.set_title('First Hadron Momentum Magnitude Distribution')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    fig.savefig(f'{plots_dir}/first_hadron_momentum.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Saved first hadron momentum analysis to {plots_dir}/first_hadron_momentum.png")

def create_energy_mass_analysis(df, plots_dir):
    """
    Create energy and mass analysis plots for first hadrons.
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

    # Energy distribution
    ax1.hist(df['E'], bins=20, alpha=0.7, color='blue', edgecolor='black')
    ax1.set_xlabel('Energy (GeV)')
    ax1.set_ylabel('Count')
    ax1.set_title('First Hadron Energy Distribution')
    ax1.grid(True, alpha=0.3)

    # Mass distribution
    ax2.hist(df['m'], bins=20, alpha=0.7, color='red', edgecolor='black')
    ax2.set_xlabel('Mass (GeV/c²)')
    ax2.set_ylabel('Count')
    ax2.set_title('First Hadron Mass Distribution')
    ax2.grid(True, alpha=0.3)

    # Transverse momentum
    ax3.hist(df['pt'], bins=20, alpha=0.7, color='green', edgecolor='black')
    ax3.set_xlabel('p_T (GeV/c)')
    ax3.set_ylabel('Count')
    ax3.set_title('First Hadron Transverse Momentum Distribution')
    ax3.grid(True, alpha=0.3)

    # Pseudorapidity
    ax4.hist(df['eta'], bins=20, alpha=0.7, color='purple', edgecolor='black')
    ax4.set_xlabel('Pseudorapidity η')
    ax4.set_ylabel('Count')
    ax4.set_title('First Hadron Pseudorapidity Distribution')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    fig.savefig(f'{plots_dir}/first_hadron_energy_mass.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Saved first hadron energy/mass analysis to {plots_dir}/first_hadron_energy_mass.png")

def create_3d_momentum_visualization(df, plots_dir):
    """
    Create 3D momentum space visualization for first hadrons.
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Color by particle type
    particle_ids = df['ID'].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(particle_ids)))
    id_to_color = dict(zip(particle_ids, colors))

    # Particle name mapping
    particle_labels = {
        111: 'pi0', -211: 'pi-', 211: 'pi+', 311: 'K0', -311: 'Kbar0',
        313: 'K*0', -313: 'K*bar0', 2112: 'neutron', -2112: 'antineutron',
        -213: 'rho-', 223: 'omega', 113: 'rho0', 213: 'rho+',
        3322: 'Xi0', -3122: 'Lambdabar0', -2214: 'Deltabar-', 2212: 'proton'
    }

    # Plot each particle type with different color
    for pid in particle_ids:
        mask = df['ID'] == pid
        particle_data = df[mask]
        color = id_to_color[pid]
        particle_name = particle_labels.get(pid, f'ID:{pid}')
        ax.scatter(particle_data['px'], particle_data['py'], particle_data['pz'],
                  c=[color], label=particle_name, alpha=0.7, s=50)

    ax.set_xlabel('p_x (GeV/c)')
    ax.set_ylabel('p_y (GeV/c)')
    ax.set_zlabel('p_z (GeV/c)')
    ax.set_title('3D Momentum Space: First Hadrons from Fragmentation')

    # Add legend
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    fig.savefig(f'{plots_dir}/first_hadron_3d_momentum.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Saved first hadron 3D momentum visualization to {plots_dir}/first_hadron_3d_momentum.png")

    # Return the figure for interactive display
    return fig

def create_correlation_analysis(df, plots_dir):
    """
    Create correlation plots between first hadron properties.
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))

    # Energy vs Mass
    scatter1 = ax1.scatter(df['m'], df['E'], alpha=0.6, c=df['p_mag'], cmap='viridis', s=50)
    ax1.set_xlabel('Mass (GeV/c²)')
    ax1.set_ylabel('Energy (GeV)')
    ax1.set_title('First Hadron: Energy vs Mass')
    ax1.grid(True, alpha=0.3)
    plt.colorbar(scatter1, ax=ax1, label='|p| (GeV/c)')

    # Energy vs Momentum Magnitude
    scatter2 = ax2.scatter(df['p_mag'], df['E'], alpha=0.6, c=df['m'], cmap='plasma', s=50)
    ax2.set_xlabel('Momentum Magnitude (GeV/c)')
    ax2.set_ylabel('Energy (GeV)')
    ax2.set_title('First Hadron: Energy vs |p|')
    ax2.grid(True, alpha=0.3)
    plt.colorbar(scatter2, ax=ax2, label='Mass (GeV/c²)')

    # Mass vs Transverse Momentum
    scatter3 = ax3.scatter(df['pt'], df['m'], alpha=0.6, c=df['E'], cmap='coolwarm', s=50)
    ax3.set_xlabel('Transverse Momentum (GeV/c)')
    ax3.set_ylabel('Mass (GeV/c²)')
    ax3.set_title('First Hadron: Mass vs p_T')
    ax3.grid(True, alpha=0.3)
    plt.colorbar(scatter3, ax=ax3, label='Energy (GeV)')

    # 3D plot: Energy, Mass, Momentum
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    scatter4 = ax4.scatter(df['m'], df['p_mag'], df['E'],
                          c=df['pt'], cmap='rainbow', alpha=0.7, s=50)
    ax4.set_xlabel('Mass (GeV/c²)')
    ax4.set_ylabel('|p| (GeV/c)')
    ax4.set_zlabel('Energy (GeV)')
    ax4.set_title('First Hadron: 3D Property Space')
    plt.colorbar(scatter4, ax=ax4, label='p_T (GeV/c)', shrink=0.8)

    plt.tight_layout()
    fig.savefig(f'{plots_dir}/first_hadron_correlations.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✓ Saved first hadron correlation analysis to {plots_dir}/first_hadron_correlations.png")

def print_first_hadron_statistics(df):
    """
    Print comprehensive statistics for first hadrons.
    """
    print("=" * 70)
    print("FIRST HADRON STATISTICS (Primary Hadrons from Fragmentation)")
    print("=" * 70)

    print(f"\nTotal events analyzed: {len(df)}")
    print(f"Unique first hadron types: {df['ID'].nunique()}")

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
    print(f"  Mean: {df['m'].mean():.3f} GeV/c²")
    print(f"  Std:  {df['m'].std():.3f} GeV/c²")
    print(f"  Min:  {df['m'].min():.3f} GeV/c²")
    print(f"  Max:  {df['m'].max():.3f} GeV/c²")

    # Particle type breakdown
    print(f"\nFIRST HADRON TYPE BREAKDOWN:")
    particle_counts = df['ID'].value_counts()
    particle_labels = {
        111: 'pi0', -211: 'pi-', 211: 'pi+', 311: 'K0', -311: 'Kbar0',
        313: 'K*0', -313: 'K*bar0', 2112: 'neutron', -2112: 'antineutron',
        -213: 'rho-', 223: 'omega', 113: 'rho0', 213: 'rho+',
        3322: 'Xi0', -3122: 'Lambdabar0', -2214: 'Deltabar-', 2212: 'proton'
    }

    for pid, count in particle_counts.items():
        label = particle_labels.get(pid, f'ID:{pid}')
        percentage = (count / len(df)) * 100
        print(f"  {label}: {count} ({percentage:.1f}%)")

    # Final state vs decayed
    final_count = df['IsFinal'].sum()
    decayed_count = len(df) - final_count
    print(f"\nFINAL STATE VS DECAYED:")
    print(f"  Final state: {final_count} ({final_count/len(df)*100:.1f}%)")
    print(f"  Decayed: {decayed_count} ({decayed_count/len(df)*100:.1f}%)")

    # Correlation analysis
    print(f"\nKEY CORRELATIONS:")
    corr_em = df['E'].corr(df['m'])
    corr_ep = df['E'].corr(df['p_mag'])
    corr_mp = df['m'].corr(df['p_mag'])
    corr_et = df['E'].corr(df['pt'])

    print(f"  Energy-Mass: {corr_em:.3f}")
    print(f"  Energy-Momentum: {corr_ep:.3f}")
    print(f"  Mass-Momentum: {corr_mp:.3f}")
    print(f"  Energy-p_T: {corr_et:.3f}")

def main():
    """
    Main function to run first hadron analysis.
    """
    import argparse
    parser = argparse.ArgumentParser(description='First Hadron Analysis')
    parser.add_argument('--no-interactive', action='store_true',
                       help='Skip interactive 3D plot display')
    args = parser.parse_args()

    filename = 'first_hadron_data.csv'
    plots_dir = 'plots'

    # Ensure plots directory exists
    os.makedirs(plots_dir, exist_ok=True)

    try:
        # Load data
        print("Loading first hadron data...")
        df = load_first_hadron_data(filename)
        print(f"Loaded {len(df)} first hadrons from {len(df)} events")

        # Print statistics
        print_first_hadron_statistics(df)

        # Create all analysis plots
        print("\n" + "="*50)
        print("GENERATING FIRST HADRON ANALYSIS PLOTS")
        print("="*50)

        create_particle_type_analysis(df, plots_dir)
        create_momentum_analysis(df, plots_dir)
        create_energy_mass_analysis(df, plots_dir)
        corr_fig = create_correlation_analysis(df, plots_dir)
        momentum_3d_fig = create_3d_momentum_visualization(df, plots_dir)

        print("\n" + "="*50)
        print("FIRST HADRON ANALYSIS COMPLETE!")
        print("="*50)
        print(f"All plots saved to: {plots_dir}/")
        print("\nGenerated plot files:")
        plot_files = [
            "first_hadron_types.png - First hadron type distributions and properties",
            "first_hadron_momentum.png - Momentum component distributions",
            "first_hadron_energy_mass.png - Energy, mass, p_T, and η distributions",
            "first_hadron_correlations.png - Property correlation scatter plots",
            "first_hadron_3d_momentum.png - 3D momentum space visualization"
        ]
        for plot_file in plot_files:
            print(f"  • {plot_file}")

        # Display 3D interactive plots (if not skipped)
        if not args.no_interactive:
            print("\n" + "="*50)
            print("DISPLAYING 3D PLOTS")
            print("="*50)
            print("Note: For full interactivity (rotation, zoom), run in Jupyter notebook or IPython")
            print("Use --no-interactive to skip this display")
            print("Close the plot windows to continue...")

            # Close all other figures to avoid blank windows
            plt.close('all')

            # Display 3D correlation plot
            print("Displaying 3D property correlations...")
            plt.figure(corr_fig)
            plt.show()

            # Display 3D momentum visualization
            print("Displaying 3D momentum space visualization...")
            plt.figure(momentum_3d_fig)
            plt.show()

            print("3D plot display complete!")
        else:
            print("\nSkipping interactive 3D plot display (--no-interactive flag used)")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        print("Please run the first_emitted program first to generate the data.")
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main()