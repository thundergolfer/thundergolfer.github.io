import manim

from typing import List


class GeneralPositionScene(manim.ThreeDScene):
    def construct(self):
        plane = manim.NumberPlane()
        axis_config = {
            "x_range": (-10, 10, 1),
            "y_range": (-10, 10, 1),
            "z_range": (-10, 10, 1),
        }

        axes = manim.ThreeDAxes(**axis_config)
        self.set_camera_orientation(
            phi=-130*manim.DEGREES,
            theta=10*manim.DEGREES,
            distance=10,
        )
        # circle = manim.Circle()
        # square = manim.Square()
        # square.flip(manim.RIGHT)
        # square.rotate(-3 * manim.TAU / 8)
        # circle.set_fill(manim.PINK, opacity=0.5)

        vec_coordinates: List[List[int]] = [
            [2, 2], [0, 5], [1, 3],
        ]
        vec_colors = [
            manim.ORANGE,
            manim.GREEN_C,
            manim.YELLOW_C,
        ]
        self.add(plane)
        self.add(axes)

        for vec_coords, vec_color in zip(vec_coordinates, vec_colors):
            v = manim.Vector(vec_coords)
            v.set_color(vec_color)
            # v.coordinate_label(color=manim.ORANGE)
            self.add(v)

        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(12)
        # self.play(manim.Create(square))
        # self.play(manim.Transform(square, circle))
        # self.play(manim.FadeOut(square))


class NotGeneralPositionScene(manim.ThreeDScene):
    def construct(self):
        pass
