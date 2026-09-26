import matplotlib

matplotlib.use("Agg")

import numpy as np
import pytest

from fractal_generator import FractalGenerator, main


def test_vectorized_matches_scalar_reference():
    gen = FractalGenerator(width=40, height=30, max_iter=50, smooth=False)
    data = gen.generate_mandelbrot()
    grid = gen._grid(gen.bounds(-0.75, 3.5))
    expected = np.vectorize(gen.mandelbrot)(grid)
    np.testing.assert_array_equal(data, expected)


def test_known_points():
    gen = FractalGenerator(max_iter=50, smooth=False)
    assert gen.mandelbrot(0) == 50      # in the set
    assert gen.mandelbrot(-1) == 50     # period-2 cycle, in the set
    assert gen.mandelbrot(2 + 2j) == 1  # escapes after one step


def test_output_shape_and_range():
    gen = FractalGenerator(width=64, height=48, max_iter=40)
    for data in (gen.generate_mandelbrot(), gen.generate_julia()):
        assert data.shape == (48, 64)
        assert data.min() >= 0
        assert data.max() <= 40


def test_smooth_colouring_is_fractional():
    gen = FractalGenerator(width=64, height=48, max_iter=40, smooth=True)
    data = gen.generate_mandelbrot()
    escaped = data[data < 40]
    assert np.any(escaped != np.round(escaped))


def test_julia_is_point_symmetric():
    # Julia sets satisfy J(-z) = J(z); a grid centred on 0 is point-symmetric.
    gen = FractalGenerator(width=51, height=41, max_iter=60, smooth=False)
    data = gen.generate_julia(c=-0.8 + 0.156j)
    np.testing.assert_array_equal(data, data[::-1, ::-1])


def test_bounds_keep_square_pixels():
    gen = FractalGenerator(width=800, height=600)
    x_min, x_max, y_min, y_max = gen.bounds(-0.5 + 0.25j, 4.0)
    assert (x_min, x_max) == (-2.5, 1.5)
    assert (y_min, y_max) == pytest.approx((-1.25, 1.75))


def test_invalid_arguments():
    with pytest.raises(ValueError):
        FractalGenerator(width=0)
    with pytest.raises(ValueError):
        FractalGenerator(max_iter=0)


def test_animate_writes_frames(tmp_path):
    gen = FractalGenerator(width=20, height=15, max_iter=20)
    paths = gen.animate_fractal(frames=3, output_dir=str(tmp_path))
    assert len(paths) == 3
    assert all((tmp_path / f"fractal_zoom_{i:03d}.png").exists() for i in range(3))


def test_main_writes_images(tmp_path):
    main(["--width", "40", "--height", "30", "--max-iter", "20",
          "--output-dir", str(tmp_path)])
    assert (tmp_path / "mandelbrot_fractal.png").exists()
    assert (tmp_path / "julia_fractal.png").exists()
