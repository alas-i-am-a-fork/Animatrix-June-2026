import numpy as np
from manim import *

class SquareWaveFourierSeries(Scene):
    def construct(self):
        # Configuration for the graph
        x_range = [-2 * PI, 2 * PI, PI / 2]
        y_range = [-1.5, 1.5, 0.5]
        n_harmonics_to_show = 5 # This means the first 5 odd harmonics (n=1, 3, 5, 7, 9)

        # Colors for individual harmonics and the sum
        harmonic_colors = [
            YELLOW,
            BLUE_C,
            GREEN_C,
            RED_C,
            PURPLE_C,
            ORANGE,
            TEAL,
        ]
        sum_color = WHITE
        target_wave_color = GRAY_B

        # 1. Setup Axes
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=12,
            y_length=6,
            axis_config={"include_numbers": True},
        ).add_coordinates()
        self.add(axes)

        # 2. Define the target square wave function
        # A square wave from -1 to 1 with period 2*PI
        def square_wave_func(x):
            # Normalize x to be within one period [0, 2*PI]
            x_mod = (x + 2*PI) % (2 * PI)
            if 0 < x_mod < PI:
                return 1.0
            elif PI < x_mod < 2 * PI:
                return -1.0
            else: # At exact boundaries or points where it jumps
                return 0.0

        # Plot the target square wave (for reference)
        square_wave_graph = axes.plot(square_wave_func, color=target_wave_color, stroke_opacity=0.5)
        square_wave_label = Text("Target Square Wave", font_size=24, color=target_wave_color).to_corner(UP + LEFT)
        
        self.play(Create(axes), FadeIn(square_wave_label, square_wave_graph))
        self.wait(1)

        # 3. Initialize cumulative sum
        # Start with a function that returns 0 for all x
        current_sum_func = lambda x: 0.0
        current_sum_graph = axes.plot(current_sum_func, color=sum_color, stroke_width=3)
        self.add(current_sum_graph) # Add initial zero sum graph

        sum_label = Text("Cumulative Sum", font_size=24, color=sum_color).to_corner(UP + RIGHT)
        self.play(FadeIn(sum_label))
        self.wait(1)

        # 4. Loop through harmonics and animate their summation
        # Fourier series for a square wave uses only odd harmonics: n=1, 3, 5, 7, 9...
        harmonic_numbers = [2 * k + 1 for k in range(n_harmonics_to_show)]

        for i, n in enumerate(harmonic_numbers):
            # Define the current harmonic function
            # Formula: (4/PI) * (1/n) * sin(n*x)
            harmonic_func_n = lambda x, n_val=n: (4 / PI) * (1 / n_val) * np.sin(n_val * x)
            new_harmonic_graph = axes.plot(harmonic_func_n, color=harmonic_colors[i], stroke_width=2)
            
            # Create a label for the current harmonic
            harmonic_text = Text(f"Harmonic n={n}", font_size=24, color=harmonic_colors[i]).to_corner(DOWN + LEFT)
            
            # Animate the creation of the current harmonic graph and its label
            self.play(
                Create(new_harmonic_graph),
                FadeIn(harmonic_text),
                run_time=1
            )
            self.wait(0.5)

            # Define the new cumulative sum function by adding the current harmonic
            # This lambda captures the *current* state of current_sum_func and harmonic_func_n
            new_sum_func = lambda x, old_func=current_sum_func, new_h_func=harmonic_func_n: old_func(x) + new_h_func(x)
            
            # Create a temporary graph for the new sum
            temp_new_sum_graph = axes.plot(new_sum_func, color=sum_color, stroke_width=3)

            # Animate the transformation of the cumulative sum graph
            # The individual harmonic graph and its label fade out as it's added to the sum
            self.play(
                Transform(current_sum_graph, temp_new_sum_graph),
                FadeOut(new_harmonic_graph),
                FadeOut(harmonic_text),
                run_time=1.5
            )
            
            # Update the current sum function for the next iteration
            current_sum_func = new_sum_func
            # current_sum_graph is already updated in-place by Manim's Transform

            self.wait(0.5)

        self.wait(3)