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

    F = 120e-3
    nxmits = 64

    angles = np.linspace(-45, 45, nxmits).tolist()
    theta = np.radians(angles)

    xx = F * np.sin(theta)
    zz = F * np.cos(theta)
    yy = 0 * xx
    focus_point = [xx, yy, zz]

    delay = []
    for i in range(nxmits):
        delay.append(cal_phased_array_transmit_delay(probe, [xx[i], yy[i], zz[i]], F, 1540))

    delay = np.array(delay)
    delay = delay / 0.01e-6
    delay = delay.astype(int)

    plt.plot(delay[0, :])
    plt.plot(delay[7, :])
    plt.plot(delay[8, :])
    plt.plot(delay[15, :])
    plt.plot(delay[31, :])
    plt.plot(delay[32, :])
    plt.show()    

    delay = numpy_to_c_array(delay)
    with open("delay_profile.txt", "w", encoding="utf-8") as file:
        file.write(delay)



