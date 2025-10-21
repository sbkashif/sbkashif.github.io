---
layout: post
title: 'Parameterizing force fields: A walkthrough of the TIP3P water model'
permalink: _posts/:year/:month/:day/:title/
tags: [molecular dynamics, non-equilibrium, steady-state, ergodic hypothesis]
usemathjax: true
ai_assistants:
  - tool: chatgpt
    url: https://chatgpt.com/share/680ba763-d7d4-8000-93e4-cbd339eca56b
---

---

A compact, fixed-charge water model like **TIP3P** is built by separately tuning (1) **van der Waals** interactions via Lennard-Jones parameters, (2) **Coulombic** partial charges, and (3) **bond/angle** terms to quantum and experimental data. It trades full flexibility for computational speed via rigid constraints. Each term is fit iteratively: you guess initial parameters, simulate or compute observables, evaluate an error function, update parameters, and repeat until convergence. This section walks through each step using TIP3P's **LJ**, **electrostatic**, and **geometry** terms as examples.  

---

## Lennard-Jones (van der Waals) Fit

**Functional form:**  

$$V_{\text{LJ}}(r) = 4\varepsilon \left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6\right]$$

captures Pauli repulsion ($r^{-12}$) and dispersion ($r^{-6}$) between neutral sites.  

**TIP3P choice:** Only the **oxygen** site carries LJ parameters; hydrogens have ε=0, σ arbitrary—for efficiency and because O–H and H–H vdW are negligible in bulk water simulations.  

### 1.1 Targets and Error Metric  
- **Density** at 298 K, 1 atm: $rho_{target}=1.00$ g/cm³  
- **Heat of vaporization**: $\Delta H_{vap,target}=10.5$ kcal/mol  
Define  
$
E_{\rm LJ}
=100\,(\rho_{\rm sim}-1.00)^2 + (\Delta H_{\rm sim}-10.5)^2
$  
$w_\rho=100$, $w_H=1$ to balance units.

### 1.2 Iterative Fitting Example  
```python
# Placeholder: run MD with initial σ=3.2Å, ε=0.10 kcal/mol and measure
rho_sim = …   # e.g. 0.95
dH_sim  = …   # e.g. 9.0
E_LJ = 100*(rho_sim-1.00)**2 + (dH_sim-10.5)**2
print("E_LJ:", E_LJ)  # Placeholder output: 2.50
```
Estimate ∂E/∂σ and ∂E/∂ε numerically (e.g. +20 per Å, –3 per kcal/mol), then update  
$sigma\leftarrow\sigma-\alpha\,\partial E/\partial\sigma$,  
$varepsilon\leftarrow\varepsilon-\alpha\,\partial E/\partial\varepsilon$  
(e.g. $alpha=0.01$). After ~5–10 iterations converge to  
$
\sigma\approx3.1507\;\text{Å},\quad
\varepsilon\approx0.1521\;\text{kcal/mol}
$  
reproducing bulk water properties within target tolerance.

---

## Electrostatic (Partial-Charge) Fit

**Coulomb’s law:**  

$V_{Coulomb}
=\sum_{i<j}\frac{k_C,q_iq_j}{r_{ij}}$,

models permanent dipoles and ionic interactions via fixed point charges on O/H sites.

### 2.1 Targets and Error Function  
- **Quantum ESP** on a grid around H₂O  
- **Dipole moment** $\mu_{target}=1.85$ D  
$
E_{\rm elec}
=\tfrac1N\sum_j\bigl[\Phi_{\rm model}(r_j)-\Phi_{\rm QM}(r_j)\bigr]^2
+(\mu_{\rm model}-1.85)^2
$

### 2.2 Iterative Fitting Example  
```python
# Placeholder: load QM ESP from h2o_esp.npz
# Fit q_O,q_H via least_squares:
# -> Fitted charges: [-0.8340, 0.4170]
```
One sets initial \((q_O,q_H)=(-0.80,0.40)$, computes $Phi_{\rm model}$ at grid points and $mu_{\rm model}$, evaluates \(E_{\rm elec}$, then updates  
\(q_a\leftarrow q_a-\alpha_e\,\partial E/\partial q_a$  
(e.g. $alpha_e=0.05$). Converges to **q_O≈–0.834 e**, **q_H≈+0.417 e** (each H) matching the original TIP3P values.

---

## Geometry: From Harmonic Fit to Rigid Constraints

### 3.1 Flexible Harmonic Terms  
**Bond stretching:**  
\[
V_{\rm bond}=\sum_{\rm bonds}\tfrac12\,k_{b}(r-r_{0})^2,
\quad r_{0}=0.9572\;\text{Å}.
\]  
**Angle bending:**  
\[
V_{\rm angle}=\sum_{\rm angles}\tfrac12\,k_{\theta}(\theta-\theta_{0})^2,
\quad \theta_{0}=104.52^\circ.
\]  
Typical **force constants** are fit to vibrational frequencies (OH stretch ≃3650 cm⁻¹, bend ≃1590 cm⁻¹):  
\[
k_{b}\approx450\;\tfrac{\mathrm{kcal}}{\mathrm{mol·Å}^2},\quad
k_{\theta}\approx55\;\tfrac{\mathrm{kcal}}{\mathrm{mol·rad}^2}.
\]

### 3.2 Parameterization via Normal-Mode Analysis  
1. **Quantum target**: frequencies from QM Hessian.  
2. **Classical normal modes**: solve \(H\,x=\omega^2x$ for the harmonic model.  
3. **Error:** \((\omega_{\rm class}-\omega_{\rm QM})^2$.  
4. **Update** \(k_b,k_\theta$ via least-squares until match within ~1–2 cm⁻¹.

### 3.3 Why Rigid Geometry?  

- **OH stretch period:**  
  \[
    T \approx \frac{1}{3650\;\mathrm{cm}^{-1}\times3\times10^{10}\;\mathrm{cm/s}}
    \approx9\;\mathrm{fs},
  \]  
  requiring $Delta t\lesssim0.9$ fs (practical ~0.5 fs) for stability.  
- **With bonds/angle fixed** via SHAKE/SETTLE at \(r_{0}$ and $theta_{0}$, the fastest modes vanish. Remaining modes have periods ≳100 fs, allowing a **2 fs** timestep safely.  

| Model    | Δt (fs) | Energy Drift (kcal/mol/ns) |
|----------|---------|-----------------------------|
| Flexible | 0.5     | 0.02                        |
| Rigid    | 2.0     | 0.03                        |

The ~4× larger timestep yields ~4× speedup with negligible impact on accuracy of structural and dynamical observables.

---

## Final TIP3P Parameter Summary

| Term           | Parameter              | Value                    |
|----------------|------------------------|--------------------------|
| **LJ (O–O)**   | $sigma$             | 3.1507 Å |
|                | $varepsilon$        | 0.1521 kcal/mol |
| **Charges**    | \(q_O$                | –0.834 e |
|                | \(q_H$                | +0.417 e (each H)        |
| **Geometry**   | \(r_{OH}$             | 0.9572 Å (rigid)         |
|                | $theta_{HOH}$       | 104.52° (rigid)          |
| **Force Const.** | \(k_b$              | 450 kcal/mol·Å²          |
|                | \(k_\theta$           | 55 kcal/mol·rad²         |

---

By iteratively fitting LJ and Coulombic parameters to **bulk** and **quantum** targets, then tuning bond/angle force constants to **vibrational** data—and finally rigidifying those degrees of freedom—TIP3P water achieves a balance of **accuracy** and **speed**. In our next section, we’ll explore **ab initio MD**, where electrons roam dynamically, enabling polarization, bond breaking/forming, and many-body quantum effects that classical force fields cannot capture.