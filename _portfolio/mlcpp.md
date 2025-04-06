---
layout: page
title: "ML-CPP: Machine Learning Library with C++ Backend"
permalink: /portfolio/mlcpp/
keywords: machine learning, C++, Python, pybind11, scikit-learn, neural networks, linear regression
thumbnail: https://raw.githubusercontent.com/isocpp/logos/master/cpp_logo.png
thumbnail_alt: "C++ Programming Language Logo"
---

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sbkashif/mlcpp)

## Project Overview

ML-CPP is a high-performance machine learning library that combines the computational efficiency of C++ with the user-friendly interface of Python. The project demonstrates how to bridge these two worlds effectively, creating a machine learning framework that's both powerful and easy to use.

<!--more-->

## Key Achievements

- Designed and implemented a modular C++ machine learning library with Python bindings
- Successfully engineered two core algorithms:
  - Linear regression with gradient descent optimization
  - Neural network with customizable architecture and multiple activation functions
- Achieved 95.67% accuracy on binary classification tasks, comparable to scikit-learn's 96.33%
- Demonstrated the viability of C++ backend for machine learning applications

## Technical Features

### Linear Regression Implementation

- Gradient descent optimization with configurable learning rate and convergence criteria
- Full vector/matrix support for multivariate regression
- Comprehensive evaluation metrics including MSE and R-squared

### Neural Network Implementation

- Fully customizable architecture with support for any number of hidden layers
- Multiple activation functions (Sigmoid, ReLU, and Tanh)
- Mini-batch stochastic gradient descent optimization
- Xavier/Glorot weight initialization for improved training stability

### Performance Analysis

![Performance Comparison](/assets/images/sklearn_mlp_boundary.png)

- **Neural Network Accuracy**: 95.67% accuracy (compared to scikit-learn's 96.33%)
- **Activation Functions**: Tanh achieved 100% accuracy on XOR problem, while Sigmoid and ReLU reached 75%
- **Training Speed**: While ~40x slower than scikit-learn's optimized implementation on large datasets, the implementation is efficient for small to medium datasets
- **Memory Usage**: Lower memory footprint than equivalent scikit-learn models

## Implementation Highlights

The project demonstrates several advanced techniques:

- **C++/Python Interoperability**: Seamless integration between C++ and Python using pybind11
- **Vector Mathematics**: Custom implementation of linear algebra operations for machine learning
- **Gradient Descent Optimization**: Implementation of both full-batch and mini-batch versions
- **Backpropagation Algorithm**: From-scratch implementation for neural network training

## Code Example

```cpp
// Create a neural network with 2 inputs, 8 hidden neurons, and 1 output
mlcpp::models::NeuralNetwork model(
    {2, 8, 1}, 
    mlcpp::models::ActivationFunction::TANH, 
    0.01,  // learning rate
    1000   // max iterations
);

// Train the model
model.fit(X_train, y_train);

// Make predictions
std::vector<double> predictions = model.predictBinary(X_test);
```

## Technologies Used

- **C++14**: Core implementation language
- **Python 3.x**: Interface language and comparison testing
- **pybind11**: For C++/Python bindings
- **CMake**: Build system
- **scikit-learn**: For benchmarking and comparison

## Learnings and Future Directions

The project demonstrated both the advantages and challenges of implementing machine learning algorithms in C++:

- C++ provides fine-grained control over memory and computation
- The implementation gap between scikit-learn and our library highlights the extensive optimization in mature ML libraries
- Future work could include SIMD optimizations, GPU acceleration, and additional algorithms

## GitHub Repository

[View the complete project on GitHub](https://github.com/sbkashif/mlcpp)
