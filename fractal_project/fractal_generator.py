#!/usr/bin/env python3
"""
Advanced Fractal Generator
This program generates beautiful fractal patterns using the Mandelbrot set
with interactive visualization capabilities.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time
import sys

class FractalGenerator:
    """A class to generate and visualize fractals, particularly the Mandelbrot set."""
    
    def __init__(self, width=800, height=600, max_iter=100):
        self.width = width
        self.height = height
        self.max_iter = max_iter
        self.x_min, self.x_max = -2.0, 1.0
        self.y_min, self.y_max = -1.5, 1.5
        
    def mandelbrot(self, c, max_iter):
        """Calculate the Mandelbrot iteration count for a complex number."""
        z = 0
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter
    
    def generate_mandelbrot(self):
        """Generate the Mandelbrot set fractal."""
        # Create coordinate arrays
        x = np.linspace(self.x_min, self.x_max, self.width)
        y = np.linspace(self.y_min, self.y_max, self.height)
        X, Y = np.meshgrid(x, y)
        
        # Create complex plane
        C = X + 1j*Y
        
        # Initialize result array
        mandelbrot_set = np.zeros((self.height, self.width))
        
        # Calculate Mandelbrot set
        for i in range(self.height):
            for j in range(self.width):
                mandelbrot_set[i, j] = self.mandelbrot(C[i, j], self.max_iter)
        
        return mandelbrot_set
    
    def generate_julia(self, c=-0.7 + 0.27015j):
        """Generate a Julia set fractal."""
        # Create coordinate arrays
        x = np.linspace(self.x_min, self.x_max, self.width)
        y = np.linspace(self.y_min, self.y_max, self.height)
        X, Y = np.meshgrid(x, y)
        
        # Create complex plane
        Z = X + 1j*Y
        
        # Initialize result array
        julia_set = np.zeros((self.height, self.width))
        
        # Calculate Julia set
        for i in range(self.height):
            for j in range(self.width):
                z = Z[i, j]
                for n in range(self.max_iter):
                    if abs(z) > 2:
                        julia_set[i, j] = n
                        break
                    z = z*z + c
                else:
                    julia_set[i, j] = self.max_iter
        
        return julia_set
    
    def visualize_fractal(self, fractal_data, title="Fractal Visualization", colormap='hot'):
        """Visualize the fractal data."""
        plt.figure(figsize=(12, 10))
        plt.imshow(fractal_data, extent=[self.x_min, self.x_max, self.y_min, self.y_max],
                   cmap=colormap, origin='lower', interpolation='bilinear')
        plt.colorbar(label='Iteration count')
        plt.title(title)
        plt.xlabel('Real')
        plt.ylabel('Imaginary')
        plt.tight_layout()
        return plt
    
    def animate_fractal(self, iterations=20):
        """Create an animated sequence of fractal zooms."""
        print("Creating animated fractal sequence...")
        for i in range(iterations):
            # Create zoom factor
            zoom = 1 + i * 0.1
            
            # Update bounds for zoom
            x_center = -0.5
            y_center = 0
            x_range = (self.x_max - self.x_min) / zoom
            y_range = (self.y_max - self.y_min) / zoom
            
            self.x_min = x_center - x_range/2
            self.x_max = x_center + x_range/2
            self.y_min = y_center - y_range/2
            self.y_max = y_center + y_range/2
            
            # Generate fractal
            fractal = self.generate_mandelbrot()
            
            # Visualize
            plt.figure(figsize=(10, 8))
            plt.imshow(fractal, extent=[self.x_min, self.x_max, self.y_min, self.y_max],
                       cmap='hot', origin='lower', interpolation='bilinear')
            plt.colorbar(label='Iteration count')
            plt.title(f'Mandelbrot Set - Zoom Level {i+1}')
            plt.xlabel('Real')
            plt.ylabel('Imaginary')
            plt.tight_layout()
            
            # Save frame
            filename = f'fractal_zoom_{i:03d}.png'
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"Saved frame {i+1}/{iterations}")

def main():
    """Main function to demonstrate fractal generation."""
    print("Advanced Fractal Generator")
    print("=" * 30)
    
    # Create fractal generator
    generator = FractalGenerator(width=800, height=600, max_iter=100)
    
    print("Generating Mandelbrot set...")
    start_time = time.time()
    
    # Generate Mandelbrot set
    mandelbrot_data = generator.generate_mandelbrot()
    
    end_time = time.time()
    print(f"Mandelbrot set generated in {end_time - start_time:.2f} seconds")
    
    # Visualize Mandelbrot set
    plt.figure(figsize=(12, 10))
    plt.imshow(mandelbrot_data, extent=[generator.x_min, generator.x_max, generator.y_min, generator.y_max],
               cmap='hot', origin='lower', interpolation='bilinear')
    plt.colorbar(label='Iteration count')
    plt.title('Mandelbrot Set Fractal')
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.tight_layout()
    plt.savefig('mandelbrot_fractal.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Generating Julia set...")
    start_time = time.time()
    
    # Generate Julia set
    julia_data = generator.generate_julia()
    
    end_time = time.time()
    print(f"Julia set generated in {end_time - start_time:.2f} seconds")
    
    # Visualize Julia set
    plt.figure(figsize=(12, 10))
    plt.imshow(julia_data, extent=[generator.x_min, generator.x_max, generator.y_min, generator.y_max],
               cmap='hot', origin='lower', interpolation='bilinear')
    plt.colorbar(label='Iteration count')
    plt.title('Julia Set Fractal')
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.tight_layout()
    plt.savefig('julia_fractal.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Fractal generation complete!")

if __name__ == "__main__":
    main()