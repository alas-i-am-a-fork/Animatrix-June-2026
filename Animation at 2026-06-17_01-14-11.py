from manim import *
import numpy as np

class BouncingBalls(Scene):
    def construct(self):
        # Configuration
        ball_radius = 0.5
        collision_e = 0.7  # Coefficient of restitution for inelastic collisions between balls
        wall_e = 0.8     # Coefficient of restitution for wall collisions
        simulation_time = 5  # seconds

        # Create two balls
        ball1 = Circle(radius=ball_radius, color=RED, fill_opacity=1)
        ball2 = Circle(radius=ball_radius, color=BLUE, fill_opacity=1)

        # Set initial positions (non-overlapping)
        ball1.set_x(-FRAME_WIDTH / 4)
        ball2.set_x(FRAME_WIDTH / 4)

        # Set initial velocities randomly
        # Use np.array for 3D vector operations for position and velocity
        ball1.velocity = np.array([np.random.uniform(-2, 2), np.random.uniform(-2, 2), 0])
        ball2.velocity = np.array([np.random.uniform(-2, 2), np.random.uniform(-2, 2), 0])

        # Add balls to the scene initially
        self.add(ball1, ball2)

        def update_balls(mobj, dt):
            # Update positions based on velocity
            ball1.shift(ball1.velocity * dt)
            ball2.shift(ball2.velocity * dt)

            # --- Wall collisions for ball1 ---
            if ball1.get_x() - ball_radius < -FRAME_WIDTH / 2:
                ball1.set_x(-FRAME_WIDTH / 2 + ball_radius)
                ball1.velocity[0] *= -wall_e
            if ball1.get_x() + ball_radius > FRAME_WIDTH / 2:
                ball1.set_x(FRAME_WIDTH / 2 - ball_radius)
                ball1.velocity[0] *= -wall_e
            if ball1.get_y() - ball_radius < -FRAME_HEIGHT / 2:
                ball1.set_y(-FRAME_HEIGHT / 2 + ball_radius)
                ball1.velocity[1] *= -wall_e
            if ball1.get_y() + ball_radius > FRAME_HEIGHT / 2:
                ball1.set_y(FRAME_HEIGHT / 2 - ball_radius)
                ball1.velocity[1] *= -wall_e

            # --- Wall collisions for ball2 ---
            if ball2.get_x() - ball_radius < -FRAME_WIDTH / 2:
                ball2.set_x(-FRAME_WIDTH / 2 + ball_radius)
                ball2.velocity[0] *= -wall_e
            if ball2.get_x() + ball_radius > FRAME_WIDTH / 2:
                ball2.set_x(FRAME_WIDTH / 2 - ball_radius)
                ball2.velocity[0] *= -wall_e
            if ball2.get_y() - ball_radius < -FRAME_HEIGHT / 2:
                ball2.set_y(-FRAME_HEIGHT / 2 + ball_radius)
                ball2.velocity[1] *= -wall_e
            if ball2.get_y() + ball_radius > FRAME_HEIGHT / 2:
                ball2.set_y(FRAME_HEIGHT / 2 - ball_radius)
                ball2.velocity[1] *= -wall_e

            # --- Ball-Ball collision detection and response ---
            distance_vec = ball2.get_center() - ball1.get_center()
            distance = np.linalg.norm(distance_vec)

            # Check for overlap (using < 2*radius for collision detection)
            if distance < 2 * ball_radius:
                # Handle edge case where centers might perfectly overlap (prevents division by zero)
                if distance == 0:
                    ball1.shift(np.array([-0.01, -0.01, 0])) # Push apart slightly
                    ball2.shift(np.array([0.01, 0.01, 0]))
                    distance_vec = ball2.get_center() - ball1.get_center()
                    distance = np.linalg.norm(distance_vec)
                    if distance == 0: return # If still 0, skip collision resolution this frame

                # Normalize collision normal vector (points from ball1 to ball2)
                normal = distance_vec / distance

                # Calculate relative velocity along the normal
                # v_rel_n > 0 means ball1 is moving towards ball2 along the normal
                v_rel_n = np.dot(ball1.velocity - ball2.velocity, normal)

                # Only resolve collision if balls are moving towards each other
                if v_rel_n > 0:
                    # Separate balls to prevent continuous overlap (push them just out of collision)
                    overlap = (2 * ball_radius - distance) / 2 + 0.001 # Small epsilon to ensure separation
                    ball1.shift(-normal * overlap)
                    ball2.shift(normal * overlap)

                    # Project velocities onto the normal and tangential vectors
                    # Tangential vector (perpendicular to normal)
                    tangent = np.array([-normal[1], normal[0], 0])

                    v1n = np.dot(ball1.velocity, normal)
                    v1t = np.dot(ball1.velocity, tangent)
                    v2n = np.dot(ball2.velocity, normal)
                    v2t = np.dot(ball2.velocity, tangent)

                    # Apply 1D inelastic collision equations along the normal for equal masses
                    # v1n_final = (v1n * (1 - e) + v2n * (1 + e)) / 2
                    # v2n_final = (v1n * (1 + e) + v2n * (1 - e)) / 2
                    v1n_final = (v1n * (1 - collision_e) + v2n * (1 + collision_e)) / 2
                    v2n_final = (v1n * (1 + collision_e) + v2n * (1 - collision_e)) / 2

                    # Update velocities using new normal components and unchanged tangential components
                    ball1.velocity = v1n_final * normal + v1t * tangent
                    ball2.velocity = v2n_final * normal + v2t * tangent

        # Add the updater function to the scene, which will be called on every frame
        # The 'mobj' argument will be 'self' (the Scene object) but is unused within the function
        self.add_updater(update_balls)

        # Run the animation for the specified duration
        self.wait(simulation_time)

        # Remove the updater after the simulation time (optional, but good practice)
        self.remove_updater(update_balls)