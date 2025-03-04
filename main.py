import numpy as np
import matplotlib.pyplot as plt
from utils import Probe, numpy_to_c_array

def cal_phased_array_transmit_delay(probe, focus_point, F, c):

    # Extract aperture positions (Nx3 matrix)
    focus_point = np.asarray(focus_point)

    aperture_positions = probe.geometry_vectors

    # Calculate distances from each element to the focus point
    L = np.sqrt(np.sum((aperture_positions - focus_point) ** 2, axis=1))

    delay_matrix = 5e-6 - (L - F) / c

    # print(delay_matrix)

    return delay_matrix



if __name__ == '__main__':

    probe = Probe(0.3e-3, 0.18e-03, 0.12e-3, 5e-3, 64, "phase array")

    F = 80e-3
    nxmits = 128

    angles = np.linspace(-30, 30, nxmits).tolist()
    theta = np.radians(angles)

    xx = F * np.sin(theta)
    zz = F * np.cos(theta)
    yy = 0 * xx
    focus_point = [xx, yy, zz]

    rx_dir = np.stack((theta, theta*0), axis=-1)

    print(rx_dir)



