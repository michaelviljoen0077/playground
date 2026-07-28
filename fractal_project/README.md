# Advanced Fractal Generator

This project demonstrates the generation and visualization of beautiful fractal patterns, specifically the Mandelbrot and Julia sets. The implementation showcases advanced Python programming techniques including mathematical computation, visualization, and performance optimization.

## Features

- **Mandelbrot Set Generation**: Creates the iconic Mandelbrot fractal with smooth coloring
- **Julia Set Generation**: Generates customizable Julia fractals
- **High-Resolution Visualization**: Produces publication-quality fractal images
- **Performance Optimized**: Efficient algorithms for fast computation
- **Interactive Visualization**: Matplotlib-based plotting with color mapping

## Mathematical Background

### Mandelbrot Set
The Mandelbrot set is defined as the set of complex numbers c for which the function f(z) = z² + c does not diverge when iterated from z = 0.

### Julia Set
Julia sets are similar fractals defined by a fixed complex number c, where each point in the complex plane is tested for divergence under the same iteration.

## Requirements

- Python 3.6+
- NumPy
- Matplotlib

## Installation

```bash
pip install numpy matplotlib
```

## Usage

```bash
python fractal_generator.py
```

This will generate two fractal images:
- `mandelbrot_fractal.png`
- `julia_fractal.png`

## Code Structure

The project consists of:
1. `fractal_generator.py` - Main implementation with FractalGenerator class
2. `README.md` - This documentation

## Performance

The implementation uses vectorized NumPy operations for efficient computation, making it possible to generate high-resolution fractals in reasonable time.

## Examples

The program generates:
- High-resolution Mandelbrot fractal
- Customizable Julia fractal
- Publication-quality visualizations with color mapping

## Mathematical Beauty

Fractals demonstrate self-similarity at all scales and reveal infinite complexity within simple mathematical rules. This implementation showcases the beauty of mathematical art through computational visualization.