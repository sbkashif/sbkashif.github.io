---
layout: post
title: 'Understanding atomic and sub-atomic interactions to predict material properties: Which model captures what?'
permalink: /blog/:year/:month/:day/:title/
tags: [molecular dynamics, dft, machine learning, quantum mechanics, force fields]
usemathjax: true
ai_assistants:
  - tool: chatgpt
    url: https://chatgpt.com/share/680195d7-86f0-8006-95a2-5c36358798ca
---

Predicting material behavior starts with understanding the fundamental interactions between atoms and molecules. For instance, the mechanical strength of polymeric materials arises from the collective response of polymer chains to applied stress: from stretching and sliding past one another to scission. Similarly, the electrical conductivity of metals depends on how electrons traverse the atomic lattice.

<!--more-->

Capturing these atomic‑scale phenomena that govern macroscopic properties requires mathematical models capable of representing both interatomic and sub‑atomic interactions. At the sub‑atomic level, quantum mechanics governs electron–nuclear forces, whereas at the interatomic level, bonded and nonbonded interactions dominate. The choice of model therefore depends on which physical effects one needs to describe. In this post, we will explore various models for atomic and sub‑atomic interactions, discuss their strengths and limitations, and examine how they interrelate.



### 1. The Simplest Model: Charged Particles and Coulomb's Law

Imagine electrons and nuclei as simple charged particles. In this simplified view, classical physics, specifically Coulomb's law, could describe their interactions. Coulomb's law quantifies the force between two point charges:

$$V_{\text{Coulomb}}(r) = \frac{1}{4\pi \varepsilon_0} \frac{q_1 q_2}{r}$$

This equation describes the attraction between negatively charged electrons and positively charged nuclei, as well as the repulsion between like-charged electrons. Conceptually, if we treated a hydrogen atom (one proton, one electron) using only Coulomb's law, we could begin to understand the electrostatic forces holding the atom together. However, this purely classical approach neglects the quantum mechanical nature of electrons.

### 2. Enter Quantum Mechanics: Wavefunctions and Electron Clouds

How does quantum mechanics refine our understanding of electron behavior? Instead of treating electrons as point charges, we recognize their wave-like nature i.e. electrons are not localized particles but rather exist as **clouds** which are distributed in space. 

The probability of finding an electron in a specific region is described by a wavefunction, $\psi$. The square of this wavefunction, $\psi^2$, defines the electron cloud, representing the spatial distribution of electron density.

### 3. Pauli Exclusion and Short-Range Repulsion

A fundamental principle governing electron behavior is the **Pauli Exclusion Principle**: no two electrons can occupy the same quantum state. This principle has significant consequences when electron clouds overlap. As electrons are forced into closer proximity, the Pauli Exclusion Principle gives rise to **Pauli repulsion**, a short-range repulsive force that becomes significant at small interatomic distances. 

This leads to development of a **repulsive potential** that prevents atoms from collapsing into one another. This repulsion is often approximated by a term proportional to $r^{-12}$, where $r$ is the distance between atoms. This term effectively captures the steep increase in repulsion as atoms get very close, preventing atoms from collapsing into one another.

### 4. Modeling Dispersion: Induced Dipoles

While Pauli repulsion prevents atoms from getting too close, atoms are not always repelling each other. When two neutral atoms are separated by a distance $r$, the electrons in one atom can experience attractive forces from the protons(nucleus) of the other atom. These attractive forces leads to disruptions in the electron clouds, creating **induced dipoles** i.e. temporary dipoles that arise from the instantaneous (re)distribution of electron density.

These induced dipoles are modeled by a dispersion term where the forcs, also known as **London dispersion forces** or **van der Waals forces**, are proportional to $r^{-6}$.

### 5. Lennard-Jones Potential: Combining Repulsion and Attraction

The combined $r^{-12}$ repulsive term and the $r^{-6}$ attractive term is known as the **Lennard-Jones potential**. The Lennard-Jones potential is a widely used model in molecular dynamics simulations to describe the interaction between neutral atoms or molecules. It combines both the repulsive and attractive forces into a single equation:

$$V_{\text{LJ}}(r) = 4\varepsilon \left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6\right]$$

Here, $\varepsilon$ determines the depth of the potential well, and $\sigma$ determines the distance at which the potential is zero. The Lennard-Jones potential provides a simple yet effective way to model the balance between repulsive and attractive forces between atoms.

### 6. Beyond Induced Dipoles: Permanent Dipoles and Electrostatics

While the Lennard-Jones potential have a term to capture induced dipoles, it does not account for **permanent dipoles**. Permanent dipoles arise from the uneven distribution of electron density in molecules, leading to partial charges on atoms. For example, in water (H₂O), the oxygen atom has a partial negative charge, while the hydrogen atoms have partial positive charges. This creates a permanent dipole moment in the molecule.

The interaction between these partial charges is then naturally modeled using **Coulomb's law**:

$$V_{\text{Coulomb}} = \frac{1}{4\pi\varepsilon_0} \sum_{i,j} \frac{q_i q_j}{r_{ij}}$$

where $q_i$ and $q_j$ are the partial charges on atoms $i$ and $j$, and $r_{ij}$ is the distance between them. This term captures **electrostatics**: attraction/repulsion between charged atoms, even across different molecules. A prime example is hydrogen bonding, where the partial positive charge on a hydrogen atom is attracted to the partial negative charge on an oxygen or nitrogen atom. 

### 7. Geometry Terms: Bonds, Angles, and Dihedrals

In addition to non-bonded interactions like Coulomb and Lennard-Jones, classical molecular models often include bonded terms to describe internal molecular geometry:

- **Bond stretching**: Modeled as harmonic springs to capture vibrations between bonded atoms.
- **Angle bending**: Keeps three bonded atoms near equilibrium angles, reflecting hybridization preferences.
- **Dihedral torsion**: Controls rotation around bonds, especially in chains and rings, capturing steric and conjugative effects.

These bonded terms are not derived from fundamental laws but are empirical approximations. Why are these terms useful? They reduce computational cost. Instead of calculating all pairwise interactions in a molecule, bonded terms constrain atoms to move around their equilibrium positions. This avoids recalculating expensive electron-level interactions each time a bond stretches or an angle bends. By encoding typical molecular shapes directly, bonded terms allow large systems to be simulated over longer timescales with reasonable accuracy.

### 8. What's Still Missing in Classical Models?

Even with Lennard-Jones, Coulomb, and geometric terms, classical force fields still miss important effects:

- **Charge redistribution** (polarization) under external fields or nearby charges
- **Chemical reactivity** — breaking and forming of bonds
- **Electronic delocalization** and **many-body effects**

To model these phenomena, we need to turn to quantum mechanical approaches.

### 9. DFT and AIMD: Quantum Treatments of Electrons

**Density Functional Theory (DFT)** models electrons using electron density rather than wavefunctions. It solves the Schrödinger equation approximately by minimizing energy as a functional of the electron density $\rho(\mathbf{r})$. DFT captures both particle-like electrostatics and wave-like quantum effects (including Pauli repulsion and dispersion corrections, when included).

However, DFT is fundamentally **static**: it typically assumes that atomic nuclei are fixed in space and calculates the electronic structure for that specific configuration. It does not inherently simulate how atoms move over time.

But material properties, such as melting points, elasticity, and protein folding, depend on atomic motion. For that, we need **dynamics**. Enter **Ab Initio Molecular Dynamics (AIMD)**, which combines DFT with molecular dynamics. AIMD treats nuclei classically while using DFT to calculate forces on the nuclei at each timestep. This allows for:

- Accurate electron-nuclear forces
- Bond making and breaking
- Real-time evolution of atomic motion at finite temperature

However, AIMD is computationally expensive and often limited to small systems and short timescales.

### 10. Machine-Learned Potentials: A New Frontier

**MLIPs** (Machine-Learned Interatomic Potentials) are emerging as a great alternative to capture the best of both worlds. With neural network being a universal approximator, MLIPs can learn complex potential energy surfaces from DFT or AIMD data. Once trained, they can generate atomic-level forces and energies with quantum accuracy but at a fraction of the computational cost (albeit still higher than classical force fields).

It would be interesting to see how inclusion of essential interactions like polarization, charge transfer, and many-body effects which are missing in classical models could lead to newer materail discoveries that have be limited by accuracy-speed trade-offs.

---

### Summary of Models
In summary, here is a table that summarizes the different models and their strengths and weaknesses:

| Model               | Captures                                  | Misses                                           |
|---------------------|------------------------------------------|--------------------------------------------------|
| Coulomb (point charges) | Electrostatics (e⁻–p⁺, dipoles)      | Quantum effects, overlap, bond directionality    |
| Lennard-Jones       | Pauli repulsion + induced dipole attraction | Charge transfer, explicit electrons          |
|Coulomb (partial charges) | Permanent dipoles, hydrogen bonding         | Charge redistribution, polarization              |
| Bonds/Angles/Dihedrals | Molecular geometry and conformations   | Electronic structure, reactivity                 |
| DFT                 | Quantum electron density, Pauli, dispersion | Dynamics (static nuclei), high computational cost |
| AIMD                | Full quantum dynamics                     | Scalability (computational cost)                 |
| MLIP                | Accuracy + speed (trained on DFT/AIMD)    | Generalizability outside training data           |

---

Overall, every model is still an approximation. The key is to choose the right one for the phenomenon you are trying to capture. Most most modern research questions in material science, we often need a hydrid approach that combines classical and quantum models, leveraging the strengths of each to provide a comprehensive understanding of material behavior.

