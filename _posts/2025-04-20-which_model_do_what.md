---
layout: post
title: 'Understanding the building blocks of molecular simulations'
permalink: /blog/:year/:month/:day/:title/
tags: [molecular dynamics, dft, machine learning, quantum mechanics, force fields]
usemathjax: true
ai_assistants:
  - tool: chatgpt
    url: https://chatgpt.com/share/680195d7-86f0-8006-95a2-5c36358798ca
---

Designing new materials with tailored properties increasingly relies on molecular simulations—computational tools that model how atoms and molecules interact over time. These simulations provide valuable insights into phenomena like how polymer chains stretch and break under stress, how membranes filter ions, or how molecules self-assemble into functional structures. By capturing atomic-level interactions, molecular simulations offer a unique perspective on material behavior that is often difficult to probe experimentally.

<!--more-->
The reliability of molecular simulations hinges on how well interatomic interactions are represented. These interactions are described by mathematical models known as force fields, which have proven successful in simulating a wide range of materials and behaviors. Classical force fields, often parameterized with experimental or quantum mechanical data, can accurately predict many important material properties. For more complex or quantum-sensitive phenomena, molecular simulations can be enhanced by quantum mechanical methods or machine-learned models.

In this post, we will build up from a simple model of an atom to the typical funcitonal form of a classical forcefield used in molecular simulations, and then explore how quantum and machine-learned approaches extend their reach—offering improved accuracy where traditional force fields fall short.

### A simplistic starting point to model atomic interactions
We know that an atom consists of a nucleui and electrons. Imagine electrons and nuclei as simple charged particles. In this classical view, their interactions can be described using **Coulomb’s law**, which quantifies the force between two point charges:


$$V_{\text{Coulomb}}(r) = \frac{1}{4\pi \varepsilon_0} \frac{q_1 q_2}{r}$$

**where**  
- $$V_{\text{Coulomb}}$$ is the potential energy due to the Coulomb force,  
- $$q_1$$ and $$q_2$$ are the charges,  
- $$r$$ is the distance between them, and  
- $$\varepsilon_0$$ is the vacuum permittivity.

This equation describes the attraction between negatively charged electrons and positively charged protons in nuclei, and repulsion between electrons. In this simplified classical picture, one might imagine the electron orbiting the nucleus in a circular path, bound by this electrostatic force—much like a planet orbiting the sun due to gravity.

But there's a serious flaw in this analogy.

**If this model were correct, atoms would not be stable. They would collapse.**

---

#### Detour: Why a Classical Atom Collapses  
To understand the collapse, we need to consider what classical physics says about accelerating charges.

Even if the speed of an electron in a circular orbit remains constant, its direction is constantly changing. This change in velocity means the electron is undergoing **centripetal acceleration**, directed toward the center of the orbit. And according to Maxwell’s equations, a charged particle that accelerates disturbs the electromagnetic field around it in a dynamic way.These disturbances propagate outward as **electromagnetic waves**, carrying energy away from the accelerating charge. This process—radiation due to acceleration—is a direct and unavoidable consequence of electromagetic force -- one of the four fundamental forces of nature which includes gravity. More on it [here](https://science.nasa.gov/universe/overview/forces/).

As the electron emits radiation, it loses energy. With less energy, the electron can no longer maintain its orbit at the same radius. It spirals inward, accelerating further, radiating more intensely, and continuing to lose energy in a vicious feedback loop. The end result: the electron crashes into the nucleus, and the atom self-destructs.
 
---

Clearly, this collapse doesn’t happen. Atoms exist. Matter is stable. What is the missing piece then that can help develop an accuarate model? 

### Enter Quantum Mechanics: Wavefunctions and Electron Clouds

 In quantum mechanical description, electrons are not tiny charged balls flying in deterministic orbits. Instead, they exhibit wave-particle duality: their behavior is governed by both particle-like and wave-like properties.

Rather than tracing a specific trajectory, an electron in an atom is described by a wavefunction, $$\psi$$, which encodes the probability amplitude of finding the electron at different locations. The square of the wavefunction’s magnitude,$\|\psi\|^2$ , gives the **probability density**—essentially a map of where the electron is likely to be found.

This leads to the idea of an **electron cloud**, a fuzzy spatial distribution that replaces the classical orbit. Unlike the classical model, this quantum picture predicts discrete, stable energy levels—a key reason atoms don’t collapse.

However, quantum mechanics introduces new considerations when it comes to interactions between atoms which we will explore next.

### Pauli Exclusion and Short-Range Repulsion

One of the key principles in quantum mechanics is the Pauli Exclusion Principle, which states that no two electrons can occupy the same quantum state at the same time. This principle becomes especially important when electron clouds overlap. As atoms get closer, the electron clouds start to interact, and the Pauli Exclusion Principle ensures that electrons cannot exist in the same quantum state.

This results in a Pauli repulsion, a short-range repulsive force that increases rapidly as the interatomic distance decreases. It prevents atoms from collapsing into each other by creating a repulsive force that grows stronger as atoms come closer. This repulsion is often modeled by a potential term that behaves as $$1/r^12$$, effectively preventing atoms from getting too close and defines the hard-core repulsion in many empirical potentials.

### Modeling Dispersion: Induced Dipoles

As atoms move apart and electron cloud overlap diminishes, the strong short-range repulsion caused by Pauli exclusion fades. In this regime, another kind of interaction emerges—not from exclusion, but from the subtle polarization of electron distributions.

Even in a completely neutral atom, the electron cloud is not static. Electrons are constantly fluctuating around the nucleus, and these fluctuations mean that—at any given instant—the charge distribution may be slightly imbalanced. For a fleeting moment, more electron density may reside on one side of the atom than the other, forming a temporary dipole: one side becomes slightly negative, the other slightly positive.

Now, consider what happens if a second atom is nearby. The temporary dipole on the first atom creates an electric field, which subtly distorts the electron cloud of the second atom. This distortion is not random—it shifts the electrons in such a way that an opposite dipole is induced. The two dipoles—transient as they may be—are now aligned in opposite directions, causing a net attractive interaction.

This quantum-mechanical phenomenon—known as the London dispersion force—is one of the key components of what are collectively called **van der Waals interactions**. It is modeled by an attractive potential that scales as $$1/r^6$$. Though individually weak, these forces are cumulative and omnipresent in nature—contributing significantly to the cohesion of gases, the condensation of liquids, and the stability of molecular assemblies.

### Lennard-Jones Potential: Combining Repulsion and Attraction

The combined $r^{-12}$ repulsive term and the $r^{-6}$ attractive term is known as the **Lennard-Jones potential**.

$$V_{\text{LJ}}(r) = 4\varepsilon \left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6\right]$$

Here, $\varepsilon$ determines the depth of the potential well, and $\sigma$ determines the distance at which the potential is zero. The Lennard-Jones potential provides a simple yet effective way to model the balance between repulsive and attractive forces between atoms.

The Lennard-Jones potential is a widely used model in molecular dynamics simulations to describe the interaction between neutral atoms or molecules. For many applications, modeling usig just the Lennard-Jones potential is sufficient to gain insights into the material behavior. For example, it can be used to study the phase behavior of simple fluids, the structure of liquids, and the dynamics of simple polymers. 

### Beyond Induced Dipoles: Permanent Dipoles and Electrostatics

While the Lennard-Jones potential have a term to capture induced dipoles, it does not account for **permanent dipoles**. Permanent dipoles arise from the uneven distribution of electron density in molecules, leading to partial charges on atoms. For example, in water (H₂O), the oxygen atom has a partial negative charge, while the hydrogen atoms have partial positive charges. This creates a permanent dipole moment in the molecule.

The interaction between these partial charges is then naturally modeled using **Coulomb's law**:

$$V_{\text{Coulomb}} = \frac{1}{4\pi\varepsilon_0} \sum_{i,j} \frac{q_i q_j}{r_{ij}}$$

where $q_i$ and $q_j$ are the partial charges on atoms $i$ and $j$, and $r_{ij}$ is the distance between them. This term captures **electrostatics**: attraction/repulsion between charged atoms, even across different molecules. A prime example is hydrogen bonding, where the partial positive charge on a hydrogen atom is attracted to the partial negative charge on an oxygen or nitrogen atom. 

### Geometry Terms: Bonds, Angles, and Dihedrals

In addition to non-bonded interactions like Coulomb and Lennard-Jones, classical molecular models often include bonded terms to describe internal molecular geometry:

- **Bond stretching**: Modeled as harmonic springs to capture vibrations between bonded atoms.
- **Angle bending**: Keeps three bonded atoms near equilibrium angles, reflecting hybridization preferences.
- **Dihedral torsion**: Controls rotation around bonds, especially in chains and rings, capturing steric and conjugative effects.

These bonded terms are not derived from fundamental laws but are empirical approximations that can reduce computational cost. Instead of calculating all pairwise interactions in a molecule, bonded terms constrain atoms to move around their equilibrium positions. This avoids recalculating expensive electron-level interactions each time a bond stretches or an angle bends. By encoding typical molecular shapes directly, bonded terms allow large systems to be simulated over longer timescales with reasonable accuracy.

These models are often parameterized using experimental data or high-level quantum mechanical calculations -- effectivly called **force fields**. Many common forcefields such as AMBER, CHARMM, and OPLS have proven effective for simulating useful phenomena in biological and materials systems like protein folding, polymer dynamics, and crystal growth.

### What's Still Missing in Classical Models?

These force fields are not universal. They are typically optimized for specific classes of molecules and may not perform well outside their intended domain. For example, a force field parameterized for proteins may not accurately capture the behavior of small organic molecules or inorganic materials. 

Furthemore, the force fields inherently miss several important quantum mechanical effects, including:
- **Charge redistribution** (polarization) under external fields or nearby charges
- **Chemical reactivity** — breaking and forming of bonds
- **Electronic delocalization** and **many-body effects**

To model these phenomena, we need to turn to quantum mechanical approaches, and eventually the hybrid approaches.

---
**Detour: Quntum mechanical desccriptions captured by models like Density Functional Theory (DFT)**

**Density Functional Theory (DFT)** models electrons using electron density rather than wavefunctions. It solves the Schrödinger equation approximately by minimizing energy as a functional of the electron density $\rho(\mathbf{r})$. DFT captures both particle-like electrostatics and wave-like quantum effects (including Pauli repulsion and dispersion corrections, when included).

However, DFT is fundamentally **static**: it typically assumes that atomic nuclei are fixed in space and calculates the electronic structure for that specific configuration.

---


### Ab Initio Molecular Dynamics (AIMD): The Quantum-Classical Hybrid

Determining material properties, such as melting points, elasticity, and protein folding require simulating atomic motion over time. How can we do this while still capturing the quantum effects that classical models miss? We can use **Ab Initio Molecular Dynamics (AIMD)**, which, while simulaing the motion of atoms, uses quantum mechanical calculations to determine the forces acting on them.

Effectively, this allows to capture:
- Accurate electron-nuclear forces
- Bond making and breaking
- Real-time evolution of atomic motion at finite temperature

In other words, AIMD enables generating molecular dyanmics trajectories with the accuracy of the chosen quantum mechanical method (e.g., DFT). This is particularly useful for studying chemical reactions where polarization effects and charge transfer are important.


However, AIMD is computationally expensive and scales poorly with system size. It is limited to small systems (hundreds of atoms) and short timescales (picoseconds).

###  Machine-Learned Potentials: A New Frontier

**MLIPs** (Machine-Learned Interatomic Potentials) have recently emerged as a promising avenue to reduce the speed-accuracy tradeoff of molecular simulations. Assuming a neural network to be a universal approximator, MLIPs can be trained on quantum mechanical data (e.g., DFT or AIMD) to learn the underlying energetics of a system without needing to come up with a functional form for a forcefield. 

MLIPs can be orders of magnitude faster than AIMD while maintaining comparable accuracy. They can also be trained on large datasets, allowing them to generalize to new configurations and systems. This makes them a powerful tool for simulating complex materials and chemical processes.

It would be interesting to see what new questions MLIPs can help unlock that have traditonally been limited by accuracy-speed trade-offs of classical and quantum models. However, MLIPs are not without their challenges. They require large amounts of training data, and their performance can be sensitive to the choice of architecture and hyperparameters. Additionally, they may struggle to generalize outside the training data, leading to potential inaccuracies in extrapolation.

Finally, MLIPs are still orders of magnitude slower than classical force fields, making them impractical for very large systems or long timescales. They are best suited for applications where accuracy is paramount and computational resources are available.

### Summary

| Model               | Captures                                  | Misses                                           |
|---------------------|------------------------------------------|--------------------------------------------------|
|**Intuitive starting point**|                                          |                                                  |
| Coulomb (directly modeling e⁻–p⁺ as point charges) | Electrostatics (e⁻–p⁺)      | Fundamentally incorrect and may not to suitable for any real system    |
|**Classical force fields appoximating quantum effects via paramterizaton**|                                    |                                                  |
| Lennard-Jones       | Pauli repulsion + induced dipole attraction | Charge transfer, explicit electrons          |
|Coulomb (partial charges) | Permanent dipoles, hydrogen bonding         | Charge redistribution, polarization              |
| Bonds/Angles/Dihedrals | Molecular geometry and conformations   | Electronic structure, reactivity                 |
|**Quantum approaches**|                                       |                                                  |
| DFT                 | Quantum electron density, Pauli, dispersion | Dynamics (static nuclei), high computational cost |
|**Hybrid approaches**|                                        |                                                  |
| AIMD                | Full quantum dynamics                     | Scalability (computational cost)                 |
| MLIP                | Accuracy + speed (trained on DFT/AIMD)    | Generalizability outside training data, Still orders of magnitide slower than classical FFs           |

Overall, every model is still an approximation. The key is to choose the right one for the phenomenon you are trying to capture. For most modern research questions in material science we often need a hydrid approach that combines classical and quantum models, leveraging the strengths of each to provide a comprehensive understanding of material behavior.