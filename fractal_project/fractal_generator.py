#!/usr/bin/env python3
"""
Advanced Fractal Generator

Generates Mandelbrot and Julia set fractals using vectorized NumPy escape-time
iteration, with optional smooth (continuous) colouring.
"""

import argparse
import os
import time

import numpy as np
import matplotlib.pyplot as plt


class FractalGenerator:
    """Generate and visualize Mandelbrot and Julia set fractals."""

    # Points further than this from the origin are guaranteed to diverge.
    ESCAPE_RADIUS = 2.0
    # A larger bailout radius gives smoother continuous colouring.
    SMOOTH_ESCAPE_RADIUS = 256.0

    def __init__(self, width=800, height=600, max_iter=100, smooth=True):
        if width < 1 or height < 1:
            raise ValueError("width and height must be positive")
        if max_iter < 1:
            raise ValueError("max_iter must be positive")
        self.width = width
        self.height = height
        self.max_iter = max_iter
        self.smooth = smooth

    def bounds(self, center, span):
        """Return (x_min, x_max, y_min, y_max) for a view of the complex plane.

        ``span`` is the width of the view along the real axis; the imaginary
        extent is derived from the image aspect ratio so pixels stay square.
        """
        center = complex(center)
        half_x = span / 2
        half_y = half_x * self.height / self.width
        return (center.real - half_x, center.real + half_x,
                center.imag - half_y, center.imag + half_y)

    def _grid(self, bounds):
        """Build the complex grid for the given bounds (row 0 = y_min)."""
        x_min, x_max, y_min, y_max = bounds
        x = np.linspace(x_min, x_max, self.width)
        y = np.linspace(y_min, y_max, self.height)
        return x[np.newaxis, :] + 1j * y[:, np.newaxis]

    def mandelbrot(self, c, max_iter=None):
        """Scalar escape-time count for a single complex number ``c``."""
        max_iter = self.max_iter if max_iter is None else max_iter
        z = 0j
        for n in range(max_iter):
            if abs(z) > self.ESCAPE_RADIUS:
                return n
            z = z * z + c
        return max_iter

    def _escape_time(self, z, c):
        """Vectorized escape-time iteration of z -> z**2 + c.

        Points that never escape get ``max_iter``. With smooth colouring,
        escaped points get a fractional count in [n, n + 1).
        """
        shape = z.shape
        z = z.ravel().copy()
        c = np.broadcast_to(c, shape).ravel().copy()
        counts = np.full(z.size, float(self.max_iter))
        # Only iterate the points that have not escaped yet.
        idx = np.arange(z.size)
        radius = self.SMOOTH_ESCAPE_RADIUS if self.smooth else self.ESCAPE_RADIUS

        for n in range(self.max_iter):
            escaped = np.abs(z) > radius
            if escaped.any():
                if self.smooth:
                    log_ratio = np.log(np.abs(z[escaped])) / np.log(radius)
                    counts[idx[escaped]] = n + 1 - np.log2(log_ratio)
                else:
                    counts[idx[escaped]] = n
                keep = ~escaped
                idx, z, c = idx[keep], z[keep], c[keep]
                if idx.size == 0:
                    break
            z = z * z + c

        return counts.reshape(shape)

    def generate_mandelbrot(self, center=-0.75 + 0j, span=3.5):
        """Generate Mandelbrot set iteration counts for the given view."""
        c = self._grid(self.bounds(center, span))
        return self._escape_time(np.zeros_like(c), c)

    def generate_julia(self, c=-0.7 + 0.27015j, center=0j, span=3.2):
        """Generate Julia set iteration counts for constant ``c``."""
        z = self._grid(self.bounds(center, span))
        return self._escape_time(z, complex(c))

    def visualize_fractal(self, fractal_data, bounds, title="Fractal Visualization",
                          colormap="hot", output=None, dpi=150):
        """Plot fractal data; save to ``output`` if given. Returns the figure."""
        fig_width = 10
        fig, ax = plt.subplots(figsize=(fig_width, fig_width * self.height / self.width))
        image = ax.imshow(fractal_data, extent=bounds, cmap=colormap,
                          origin="lower", interpolation="bilinear")
        fig.colorbar(image, ax=ax, label="Iteration count")
        ax.set_title(title)
        ax.set_xlabel("Real")
        ax.set_ylabel("Imaginary")
        fig.tight_layout()
        if output:
            fig.savefig(output, dpi=dpi, bbox_inches="tight")
        return fig

    def animate_fractal(self, frames=20, center=-0.743643887 + 0.131825904j,
                        start_span=3.5, zoom_per_frame=1.5, output_dir="."):
        """Save a sequence of Mandelbrot frames zooming in on ``center``.

        Returns the list of written file paths.
        """
        os.makedirs(output_dir, exist_ok=True)
        paths = []
        print("Creating animated fractal sequence...")
        for i in range(frames):
            span = start_span / zoom_per_frame ** i
            data = self.generate_mandelbrot(center=center, span=span)
            path = os.path.join(output_dir, f"fractal_zoom_{i:03d}.png")
            fig = self.visualize_fractal(data, self.bounds(center, span),
                                         title=f"Mandelbrot Set - Zoom Level {i + 1}",
                                         output=path)
            plt.close(fig)
            paths.append(path)
            print(f"Saved frame {i + 1}/{frames}")
        return paths


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Generate Mandelbrot and Julia set fractals.")
    parser.add_argument("--width", type=int, default=800, help="image width in pixels")
    parser.add_argument("--height", type=int, default=600, help="image height in pixels")
    parser.add_argument("--max-iter", type=int, default=100, help="maximum iterations per point")
    parser.add_argument("--julia-c", type=complex, default=complex(-0.7, 0.27015),
                        help="Julia set constant, e.g. -0.8+0.156j")
    parser.add_argument("--colormap", default="hot", help="matplotlib colormap name")
    parser.add_argument("--no-smooth", action="store_true",
                        help="use integer iteration counts instead of smooth colouring")
    parser.add_argument("--output-dir", default=".", help="directory to write images to")
    parser.add_argument("--animate", type=int, default=0, metavar="FRAMES",
                        help="also render a zoom sequence with this many frames")
    parser.add_argument("--show", action="store_true", help="display the plots interactively")
    return parser.parse_args(argv)


def main(argv=None):
    """Generate the Mandelbrot and Julia fractals from the command line."""
    args = parse_args(argv)
    print("Advanced Fractal Generator")
    print("=" * 30)

    generator = FractalGenerator(width=args.width, height=args.height,
                                 max_iter=args.max_iter, smooth=not args.no_smooth)
    os.makedirs(args.output_dir, exist_ok=True)

    jobs = [
        ("Mandelbrot", "Mandelbrot Set Fractal", "mandelbrot_fractal.png",
         generator.bounds(-0.75, 3.5),
         lambda: generator.generate_mandelbrot(center=-0.75, span=3.5)),
        ("Julia", f"Julia Set Fractal (c = {args.julia_c})", "julia_fractal.png",
         generator.bounds(0, 3.2),
         lambda: generator.generate_julia(c=args.julia_c, center=0, span=3.2)),
    ]

    for name, title, filename, bounds, generate in jobs:
        print(f"Generating {name} set...")
        start_time = time.perf_counter()
        data = generate()
        print(f"{name} set generated in {time.perf_counter() - start_time:.2f} seconds")

        path = os.path.join(args.output_dir, filename)
        fig = generator.visualize_fractal(data, bounds, title=title,
                                          colormap=args.colormap, output=path)
        print(f"Saved {path}")
        if not args.show:
            plt.close(fig)

    if args.animate:
        generator.animate_fractal(frames=args.animate, output_dir=args.output_dir)

    if args.show:
        plt.show()

    print("Fractal generation complete!")


if __name__ == "__main__":
    main()
