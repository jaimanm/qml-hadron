# QCBM for Hadron Collision Data

This implementation follows the [PennyLane QCBM Tutorial](https://pennylane.ai/qml/demos/tutorial_qcbm) to create a Quantum Circuit Born Machine for learning hadron collision momentum distributions.

## Overview

**Quantum Circuit Born Machines (QCBMs)** are quantum generative models that learn classical probability distributions through pure quantum states. Unlike classical Boltzmann machines, QCBMs leverage the Born rule to generate samples directly through projective measurements.

## Implementation Details

### Data
- **Source**: Hadron collision data from 50 GeV events
- **Features**: 
  - `pT`: Transverse momentum
  - `pz'`: Rescaled longitudinal momentum (E_ref × pz/E, where E_ref = 50 GeV)
- **Preprocessing**: Data discretized into 64 bins (2^6) for quantum processing

### QCBM Architecture

```
Quantum Circuit:
- Qubits: 6 (encoding 64 discrete states)
- Layers: 6 StronglyEntanglingLayers
- Total Parameters: 144
- Initial State: |000000⟩ (Born machine characteristic)
- Gate Set: Rotation gates (RY, RZ) + CNOT entangling gates
```

### Training

**Loss Function**: Maximum Mean Discrepancy (MMD) with RBF kernel
- Compares model distribution p_θ(x) with target distribution π(x)
- Multi-scale RBF kernel with bandwidths [0.25, 1.0, 4.0]

**Optimizer**: Adam
- Learning rate: 0.1
- Iterations: 150
- Framework: JAX + Optax (JIT compiled for efficiency)

**Metrics**:
- MMD Loss (training objective)
- KL Divergence (monitoring convergence)
- Fidelity (final distribution similarity)

### Key Components

1. **MMD Class**: Implements Maximum Mean Discrepancy loss with RBF kernel
2. **QCBM Class**: Wraps quantum circuit and loss function
3. **Quantum Circuit**: StronglyEntanglingLayers from PennyLane
4. **Update Step**: JIT-compiled gradient descent with JAX

## Results

The notebook trains two separate QCBMs:
1. **pT QCBM**: Learns transverse momentum distribution
2. **pz' QCBM**: Learns rescaled longitudinal momentum distribution

### Performance Metrics
- Both models achieve high fidelity (>0.9) with target distributions
- MMD loss converges to near-zero values
- KL divergence decreases throughout training

### Visualizations
- Training curves (MMD loss and KL divergence)
- Target vs learned distributions
- Sample generation from trained QCBMs

## Usage

```bash
# Open the notebook
jupyter notebook qcbm.ipynb

# Or run in VS Code with Jupyter extension
```

The notebook is fully self-contained and includes:
1. Data loading and visualization
2. Distribution discretization
3. QCBM training for both pT and pz'
4. Results visualization and analysis
5. Sample generation from trained models

## Dependencies

```python
jax>=0.4.0
jax.numpy
pennylane>=0.30.0
optax
numpy
pandas
matplotlib
```

## Key Differences from Original Tutorial

1. **Data**: Uses real hadron collision data instead of toy datasets (Bars & Stripes, Gaussian mixture)
2. **Continuous → Discrete**: Implements histogram-based discretization for continuous physics data
3. **Two Models**: Trains separate QCBMs for pT and pz' (could be extended to joint distribution)
4. **Physics Context**: Adapts quantum generative modeling to high-energy physics application

## Physics Motivation

### Why QCBM for Hadron Data?

1. **Fast Simulation**: QCBMs could provide faster alternatives to Monte Carlo event generators
2. **Data Augmentation**: Generate synthetic collision events for training ML models
3. **Anomaly Detection**: Learned distributions can identify unusual physics events
4. **Quantum Advantage**: Exponential state space scaling (2^n) for n qubits

### Applications in HEP

- Event generation for detector simulations
- Background modeling for rare process searches
- Parton shower simulation
- Jet substructure modeling

## Next Steps

### Short Term
1. **Joint Distribution**: Train QCBM to learn p(pT, pz') simultaneously
2. **More Qubits**: Increase to 8-10 qubits for finer discretization
3. **Validation**: Compare generated events with Monte Carlo

### Medium Term
1. **Conditional QCBM**: Condition on collision energy or particle type
2. **Hardware Testing**: Run on IBM Quantum or other NISQ devices
3. **Benchmarking**: Compare with classical generative models (GANs, VAEs)

### Long Term
1. **Full Event Generation**: Include all particle momenta and types
2. **Detector Effects**: Model detector response and resolution
3. **Production Use**: Integration with physics analysis pipelines

## References

1. **PennyLane Tutorial**: https://pennylane.ai/qml/demos/tutorial_qcbm
2. **Liu & Wang (2018)**: "Differentiable learning of quantum circuit born machines", Phys. Rev. A 98, 062324
3. **Benedetti et al. (2019)**: "A generative modeling approach for benchmarking and training shallow quantum circuits", npj Quantum Information 5, 45

## Citation

If you use this implementation, please cite:
- The PennyLane QCBM tutorial
- Liu & Wang (2018) original QCBM paper
- PennyLane library

## License

This implementation is provided for educational and research purposes.
