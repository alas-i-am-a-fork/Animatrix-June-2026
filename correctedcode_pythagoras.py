import numpy as np
from manim import *

class PythagoreanTheoremProof(Scene):
    def construct(self):
        # Triangle side lengths
        a_len = 3
        b_len = 4
        c_len = np.sqrt(a_len**2 + b_len**2)


        # Triangle vertices
        p_origin = ORIGIN
        p_b = b_len * RIGHT
        p_a = a_len * UP

        # Triangle sides
        side_b_line = Line(p_origin, p_b, color=WHITE)
        side_a_line = Line(p_origin, p_a, color=WHITE)
        side_c_line = Line(p_b, p_a, color=WHITE)

        triangle_lines = VGroup(
            side_a_line,
            side_b_line,
            side_c_line
        )

        # Side labels
        label_a = Text("a").scale(0.6).next_to(side_a_line, LEFT, buff=0.1)
        label_b = Text("b").scale(0.6).next_to(side_b_line, DOWN, buff=0.1)

        mid_c = (p_b + p_a) / 2

        vec_c_direction = p_a - p_b
        perp_vec_c = rotate_vector(vec_c_direction, -PI / 2)
        perp_vec_c = perp_vec_c / np.linalg.norm(perp_vec_c)

        label_c = Text("c").scale(0.6).move_to(
            mid_c + perp_vec_c * 0.4
        )

        side_labels = VGroup(label_a, label_b, label_c)

        # Square on side a
        square_a_obj = Square(
            side_length=a_len,
            fill_opacity=0.6,
            color=BLUE_B,
            stroke_width=3,
        )

        square_a_obj.move_to(
            p_origin + a_len / 2 * UP + a_len / 2 * LEFT
        )

        # Square on side b
        square_b_obj = Square(
            side_length=b_len,
            fill_opacity=0.6,
            color=GREEN_B,
            stroke_width=3,
        )

        square_b_obj.move_to(
            p_origin + b_len / 2 * RIGHT + b_len / 2 * DOWN
        )

        # Square on side c
        vec_c_hypotenuse = p_a - p_b
        unit_hypotenuse = vec_c_hypotenuse / np.linalg.norm(
            vec_c_hypotenuse
        )

        normal_vec_c = rotate_vector(
            unit_hypotenuse,
            -PI / 2
        )

        square_c_verts = [
            p_b,
            p_a,
            p_a + normal_vec_c * c_len,
            p_b + normal_vec_c * c_len,
        ]

        square_c_obj = Polygon(
            *square_c_verts,
            fill_opacity=0.6,
            color=RED_B,
            stroke_width=3,
        )

        squares = VGroup(
            square_a_obj,
            square_b_obj,
            square_c_obj,
        )

        # Group geometry
        diagram = VGroup(
            triangle_lines,
            side_labels,
            square_a_obj,
            square_b_obj,
            square_c_obj,
        )

        # Scale everything to fit comfortably
        diagram.scale(0.75)

        # Move slightly left and down so the red square has room
        diagram.shift(LEFT * 1.5 + DOWN * 0.5)

        self.play(Create(triangle_lines))
        self.wait(0.5)

        self.play(Write(side_labels))
        self.wait(0.5)

        self.play(
            Create(square_a_obj),
            Create(square_b_obj),
            Create(square_c_obj),
        )

        self.wait(1)

        equation = Text(
            "a² + b² = c²"
        ).scale(0.8).to_edge(UP, buff=0.4)

        self.play(Write(equation))
        self.wait(2)

