from manim import *

class PythagoreanTheoremProof(Scene):
    def construct(self):
        # 1. Define triangle properties and base vertices
        a_len = 3  # length of side 'a' (vertical)
        b_len = 4  # length of side 'b' (horizontal)
        c_len = np.sqrt(a_len**2 + b_len**2)

        # Vertices of the right triangle (initially at origin for calculation ease)
        p_origin = ORIGIN # The right angle vertex
        p_b = b_len * RIGHT # Vertex along x-axis
        p_a = a_len * UP # Vertex along y-axis

        # Triangle lines
        side_b_line = Line(p_origin, p_b, color=WHITE)
        side_a_line = Line(p_origin, p_a, color=WHITE)
        side_c_line = Line(p_b, p_a, color=WHITE) # Hypotenuse

        triangle_lines = VGroup(side_a_line, side_b_line, side_c_line)

        # 2. Labels for the sides
        label_a = Text("a").next_to(side_a_line, LEFT, buff=0.1)
        label_b = Text("b").next_to(side_b_line, DOWN, buff=0.1)
        
        # Position label_c in the middle of side_c_line, slightly outside
        mid_c = (p_b + p_a) / 2
        vec_c_direction = p_a - p_b
        # Rotate vec_c by -90 degrees (clockwise) to point outwards from the triangle
        perp_vec_c = rotate_vector(vec_c_direction, -PI / 2)
        label_c = Text("c").move_to(mid_c + normalize(perp_vec_c) * 0.4)

        side_labels = VGroup(label_a, label_b, label_c)

        # 3. Construct squares on each side
        # Square on side 'a' (vertical)
        square_a_obj = Square(side_length=a_len, fill_opacity=0.6, color=BLUE_B, stroke_width=3)
        # Position square_a so its right side aligns with side_a_line
        square_a_obj.move_to(p_origin + a_len/2 * UP + a_len/2 * LEFT)

        # Square on side 'b' (horizontal)
        square_b_obj = Square(side_length=b_len, fill_opacity=0.6, color=GREEN_B, stroke_width=3)
        # Position square_b so its top side aligns with side_b_line
        square_b_obj.move_to(p_origin + b_len/2 * RIGHT + b_len/2 * DOWN)

        # Square on side 'c' (hypotenuse)
        # Vector from p_b to p_a defines the hypotenuse
        vec_c_hypotenuse = p_a - p_b
        # Normal vector pointing outwards from hypotenuse (rotated 90 degrees counter-clockwise from hypotenuse direction)
        normal_vec_c = rotate_vector(normalize(vec_c_hypotenuse), PI/2) 
        
        square_c_verts = [
            p_b,
            p_a,
            p_a + normal_vec_c * c_len, # Third vertex
            p_b + normal_vec_c * c_len  # Fourth vertex
        ]
        square_c_obj = Polygon(*square_c_verts, fill_opacity=0.6, color=RED_B, stroke_width=3)

        squares = VGroup(square_a_obj, square_b_obj, square_c_obj)

        # Group all geometric elements and center them on the screen
        all_geometry = VGroup(triangle_lines, side_labels, squares)
        all_geometry.move_to(ORIGIN)

        # 4. Animation Sequence
        self.play(Create(triangle_lines))
        self.wait(0.5)

        self.play(Write(side_labels))
        self.wait(0.5)

        self.play(Create(square_a_obj), Create(square_b_obj), Create(square_c_obj))
        self.wait(1)

        # 5. Display the algebraic identity
        # CRITICAL FONT RULE: Use Text() for all text, no MathTex or Tex.
        equation = Text("a^2 + b^2 = c^2").to_edge(UP).scale(0.8)
        self.play(Write(equation))
        self.wait(2)