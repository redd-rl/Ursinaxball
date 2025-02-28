"""
The physics object.
"""

from abc import ABC, abstractmethod

from numpy import cos, sin
from ursina.color import Color, rgb

from ursinaxball.common_values import DICT_COLLISION, DICT_KEYS


class PhysicsObject(ABC):
    def __init__(self, data_object: dict, data_stadium: dict):
        pass

    @staticmethod
    def apply_trait(self, data: dict) -> None:
        """
        Applies the trait to the physics object.
        """
        if self.trait is not None:
            if data.get("traits") is not None and self.trait in data["traits"]:
                trait_value = data.get("traits").get(self.trait)
                for key in trait_value:
                    key_object = DICT_KEYS.get(key)
                    if key_object is not None and hasattr(self, key_object):
                        if getattr(self, key_object) is None:

                            if (
                                key_object == "collision_group"
                                or key_object == "collision_mask"
                            ):
                                value = self.transform_collision_dict(
                                    trait_value.get(key)
                                )
                            else:
                                value = trait_value.get(key)

                            setattr(self, key_object, value)

    @abstractmethod
    def apply_default_values(self):
        """
        Applies the default values to the physics object if they are none
        """
        pass

    @staticmethod
    def transform_collision_dict(collision_dict: dict) -> int:
        """
        Transforms the collision into a float.
        For example, ["ball", "red", "blue", "wall"] should return 1 + 2 + 4 + 32 = 39
        """
        if collision_dict is None:
            return None
        else:
            return sum(DICT_COLLISION[key] for key in collision_dict)

    @staticmethod
    def parse_color_entity(color: str) -> Color:
        (r, g, b) = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
        return rgb(r, g, b)

    @staticmethod
    def arc(
        x: float,
        y: float,
        radius: float,
        start_angle: float,
        end_angle: float,
        clockwise: bool = True,
        segments: int = 16,
    ) -> list:
        """
        Returns a list of points for an arc.
        """
        points = []
        for i in range(segments + 1):
            angle = start_angle + (end_angle - start_angle) * i / segments
            x_pos = x + radius * cos(angle)
            y_pos = y + radius * sin(angle)
            points.append((x_pos, y_pos))
        if clockwise:
            return points[::-1]
        else:
            return points
