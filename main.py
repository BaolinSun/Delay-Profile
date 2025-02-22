import numpy as np
import matplotlib.pyplot as plt
from utils import Probe

def cal_focus_transmit_delay(probe, focus_point, sound_speed):
    """
    Calculate delay matrix for focusing.

    Args:
        probe (object): Object containing `geometry` as an Nx7 array, where first three columns are [x, y, z].
        focus_point (array): 1x3 array representing the focus point [x_focus, 0, z_focus_transmit].
        sound_speed (float): Speed of sound (m/s).

    Returns:
        np.ndarray: Delay matrix for each element.
    """
    # Extract aperture positions (Nx3 matrix)
    focus_point = np.asarray(focus_point)

    aperture_positions = probe.geometry_vectors

    # Calculate distances from each element to the focus point
    distances = np.sqrt(np.sum((aperture_positions - focus_point) ** 2, axis=1))

    # Calculate maximum, minimum, and mid distances
    max_distance = np.max(distances)
    min_distance = np.min(distances)
    mid_distance = np.linalg.norm(focus_point)

    # Calculate delay matrix
    delay_matrix = (max_distance - distances) / sound_speed
    # Uncomment one of the below if using alternative delay methods
    # delay_matrix = -(distances - min_distance) / sound_speed
    # delay_matrix = -(distances - mid_distance) / sound_speed

    return delay_matrix


def numpy_to_c_array(matrix):
    # 转为Python列表
    matrix_list = matrix.tolist()
    
    # 构造C语言数组字符串
    c_array = "{\n"
    for row in matrix_list:
        row_str = ", ".join(map(str, row))
        c_array += f"    {{ {row_str} }},\n"
    c_array = c_array.rstrip(",\n") + "\n};"
    
    return c_array


if __name__ == '__main__':

    probe = Probe(0.3e-3, 0.18e-03, 0.12e-3, 5e-3, 8, "linear array")
    # probe = Probe(0.4e-3, 0.23e-03, 0.17e-3, 5e-3, 64, "linear array")

    # print(probe.geometry_vectors)

    delay = cal_focus_transmit_delay(probe, [0, 0, 30e-3], 1540)
    delay = delay / 0.01e-6
    print(delay)
        

