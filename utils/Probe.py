import numpy as np


class Geometry:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

class Probe:
    def __init__(self, pitch, kerf, element_width, element_height, element_num, probe_type):
        self.kerf = kerf
        self.pitch = pitch
        self.element_height = element_height
        self.element_width = self.pitch - self.kerf if element_width < 0 else element_width
        self.element_num = element_num
        self.probe_type = probe_type
        self.geometry = [Geometry() for _ in range(element_num)]
        self.geometry_vectors = np.zeros((element_num,3))

        if probe_type == "linear array":
            self.create_linear_array()
            self.create_linear_array_vectors()
        else:
            raise ValueError("unsupported probe type")

    def create_linear_array(self):
        mean = 0.0
        sum_x = 0.0

        for i in range(self.element_num):
            self.geometry[i].x = (i + 1) * self.pitch
            sum_x += self.geometry[i].x
            self.geometry[i].y = 0.0
            self.geometry[i].z = 0.0

        mean = sum_x / self.element_num

        for i in range(self.element_num):
            self.geometry[i].x -= mean

        return 0

    def create_linear_array_vectors(self):
        mean = 0.0
        sum_x = 0.0

        for i in range(self.element_num):
            self.geometry_vectors[i][0] = (i + 1) * self.pitch
            sum_x += self.geometry_vectors[i][0]
            self.geometry_vectors[i][1] = 0.0
            self.geometry_vectors[i][2] = 0.0

        mean = sum_x / self.element_num

        for i in range(self.element_num):
            self.geometry_vectors[i][0] -= mean

        return 0

