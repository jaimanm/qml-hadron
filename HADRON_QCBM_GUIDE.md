# QCBM Tutorial Adaptation for Hadron Data - Complete Guide (AI-Generated)

## Overview

This guide explains how to adapt the PennyLane QCBM tutorial (https://pennylane.ai/qml/demos/tutorial_qcbm) for hadron collision momentum data instead of the Bars and Stripes dataset.

## Key Concept: Data Embedding

### Tutorial (Bars & Stripes)
- **Data**: 3×3 binary images → 9-bit bitstrings
- **Representation**: 14 valid patterns out of 2^9 = 512 possible
- **Encoding**: Direct mapping of pixels to qubits
- **Distribution**: Discrete, sparse (uniform over 14 states)

### Hadron Data
- **Data**: Continuous momentum values (pT, pz, E)
- **Representation**: ~10,000 continuous measurements
- **Encoding**: Histogram discretization + probability distribution
- **Distribution**: Continuous → discretized, dense

## Step-by-Step Adaptation

### 1. Data Loading (NEW)

```python
import pandas as pd
import numpy as np

# Load CSV
df = pd.read_csv('first_emission_50gev.csv')

# Extract features
pT_data = df['Particle_pT'].values
pz_data = df['Particle_pz'].values
E_data = df['Particle_E'].values

# Calculate rescaled momentum
E_ref = 50.0  # Reference energy
pz_prime = E_ref * (pz_data / E_data)
```

**Why pz'?** Normalizes momentum by energy for fair comparison across events.

### 2. Discretization (NEW - CRITICAL)

```python
def discretize_to_target_distribution(continuous_data, n_qubits):
    n_bins = 2 ** n_qubits
    counts, bin_edges = np.histogram(continuous_data, bins=n_bins)
    probs = counts / counts.sum()
    return probs, bin_edges

# Create target distribution
n_qubits = 6  # 64 bins
pT_target_probs, pT_bins = discretize_to_target_distribution(pT_data, n_qubits)
```

**Why this works:**
- QCBM generates bitstrings |x⟩ where x ∈ {0,1,...,2^n-1}
- Each bitstring maps to a histogram bin
- QCBM learns p_θ(x) to match π(x) = normalized histogram

### 3. Variable Mapping (MODIFY)

Replace tutorial variables:

```python
# Tutorial:
n = 3
size = n**2  # 9
data = get_bars_and_stripes(n)  # (14, 9) array
probs = np.zeros(2**size)
probs[nums] = 1/len(data)

# Hadron:
n_qubits = 6
size = n_qubits  # 6
data = pT_target_probs  # Already a probability vector
probs = data  # Target π(x)
```

### 4. Circuit Definition (SAME)

```python
import pennylane as qml

n_qubits = size
dev = qml.device("default.qubit", wires=n_qubits)
n_layers = 6

@qml.qnode(dev)
def circuit(weights):
    qml.StronglyEntanglingLayers(weights=weights, ranges=[1]*n_layers, wires=range(n_qubits))
    return qml.probs()

jit_circuit = jax.jit(circuit)
```

**No changes needed!** Circuit adapts automatically based on `n_qubits`.

### 5. Training (SAME)

The MMD loss, QCBM class, and training loop work identically:

```python
# Initialize (same as tutorial)
bandwidth = jnp.array([0.25, 0.5, 1])
space = jnp.arange(2**n_qubits)
mmd = MMD(bandwidth, space)
qcbm = QCBM(jit_circuit, mmd, probs)

# Train (same as tutorial)
opt = optax.adam(learning_rate=0.1)
for i in range(n_iterations):
    weights, opt_state, loss_val, kl_div = update_step(weights, opt_state)
```

### 6. Sampling & Interpretation (MODIFY OUTPUT)

```python
# Generate samples (same)
samples = circ(weights)  # Returns bin indices

# Map back to physical values (NEW)
def bin_index_to_momentum(bin_idx, bin_edges):
    """Convert bin index to momentum value (bin center)"""
    return (bin_edges[bin_idx] + bin_edges[bin_idx+1]) / 2

# Generate synthetic hadron events
generated_pT = [bin_index_to_momentum(idx, pT_bins) for idx in samples]
```

## Key Differences Summary

| Aspect | Tutorial (Bars & Stripes) | Hadron Data |
|--------|-------------------------|-------------|
| **Data type** | Discrete binary | Continuous real |
| **Data shape** | (14, 9) patterns | (10000,) values |
| **Qubits** | 9 | 6 (configurable) |
| **Preprocessing** | None | Histogram discretization |
| **Target π(x)** | Uniform over 14 states | Continuous → histogram |
| **Output interpretation** | Binary image | Momentum value |
| **Physics meaning** | Spatial pattern | Momentum distribution |

## What to Run

1. **Execute new cells** (data loading, discretization, visualization)
2. **Run tutorial cells as-is** (MMD, QCBM, training, testing)
3. **Interpret results** (bin indices → momentum values)

## Advanced: Joint Distribution

To learn p(pT, pz') jointly:

```python
# Option 1: Concatenate (needs more qubits)
n_qubits_pT = 4  # 16 bins
n_qubits_pz = 4  # 16 bins
total_qubits = n_qubits_pT + n_qubits_pz  # 8 qubits → 256 states

# Build 2D histogram
joint_hist, _, _ = np.histogram2d(pT_data, pz_prime, bins=(2**n_qubits_pT, 2**n_qubits_pz))
joint_probs = joint_hist.flatten() / joint_hist.sum()

# Option 2: Product encoding (more complex)
# Combine bitstrings: first 4 bits = pT bin, last 4 bits = pz' bin
```

## Troubleshooting

### "NameError: 'nums' is not defined"
- **Cause**: Tutorial code references Bars & Stripes specific variables
- **Fix**: Skip or remove cells that reference `nums`, `bitstrings`, image visualization

### "Loss not decreasing"
- **Try**: 
  - More layers (n_layers=8)
  - Different learning rate (0.01 or 0.2)
  - More bandwidth scales: `bandwidth = jnp.array([0.1, 0.5, 1.0, 2.0])`

### "Overfitting to few bins"
- **Try**: Use more qubits (7 or 8) for finer discretization

## Physical Interpretation

**What the QCBM learns:**
- Start: Random quantum state
- Training: Adjusts gate parameters to match pT histogram shape
- Result: Quantum state |ψ_θ⟩ where measurement probabilities = momentum distribution

**Applications:**
1. **Fast event generation**: Sample QCBM instead of running slow detector simulations
2. **Anomaly detection**: Compare new data to learned distribution
3. **Data augmentation**: Generate synthetic training data for ML models

## Complete Working Example

```python
# 1. Load
df = pd.read_csv('first_emission_50gev.csv')
pT_data = df['Particle_pT'].values

# 2. Discretize
n_qubits = 6
counts, bins = np.histogram(pT_data, bins=2**n_qubits)
probs = counts / counts.sum()

# 3. Setup
size = n_qubits
data = probs  # This is what tutorial expects

# 4. Run tutorial cells
# (MMD class, QCBM class, circuit, training)

# 5. Generate & interpret
@qml.qnode(dev)
def sample_circuit(weights):
    qml.StronglyEntanglingLayers(weights=weights, ranges=[1]*n_layers, wires=range(n_qubits))
    return qml.sample()

sampling_dev = qml.device("default.qubit", wires=n_qubits, shots=1000)
sample_qnode = qml.QNode(sample_circuit, sampling_dev)
bin_indices = sample_qnode(weights)

# Map to momentum
generated_pT = [(bins[i] + bins[i+1])/2 for i in bin_indices]
```

## References

- Original tutorial: https://pennylane.ai/qml/demos/tutorial_qcbm
- Paper: Liu & Wang (2018), "Differentiable learning of quantum circuit born machines"
- PennyLane docs: https://docs.pennylane.ai/

## Questions?

Common confusions:
- **"Why histogram?"** → QCBM needs discrete states
- **"Why not encode directly?"** → Would need ~13 qubits to represent all float precision
- **"Can I use more qubits?"** → Yes! 7-8 qubits gives finer resolution
- **"Does training differ?"** → No, MMD loss handles any π(x) shape
