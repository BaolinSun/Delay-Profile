import numpy as np
from utils import Probe

def cal_plane_wave_transmit_delay(probe, theta, sound_speed):
    """
    Calculate time delays for each probe element to generate a planar wavefront.

    Theory:
    --------
    This function calculates the time delays required for each probe element to transmit signals
    such that the emitted waves form a planar wavefront propagating at a specified angle 'theta'.
    The calculation is based on the projection of each element's position onto the wavefront direction.

    1. Wavefront Direction:
       The wavefront direction is defined by angle 'theta' relative to the x-axis, and is computed as:
           v_x = sin(theta)    (x-component of the wavefront vector)
           v_y = 0             (assuming no movement along the y-axis)
           v_z = cos(theta)    (z-component of the wavefront vector)

       This gives the normalized wavefront direction vector:
           v = [v_x, v_y, v_z] / ||v||

    2. Projection Distance:
       Each probe element has a 3D position vector r_i = [x_i, y_i, z_i]. The projection of this position
       vector onto the wavefront direction determines its effective distance along the propagation path:
           d_i = r_i · v

    3. Time Delay Calculation:
       The time delay required for each element to synchronize with the wavefront is:
           t_i = d_i / sound_speed

    Assumptions:
    ------------
    - The probe elements are treated as a rigid linear array.
    - The wavefront is planar, and its propagation direction is controlled by 'theta'.
    - The medium is homogeneous with a constant speed of sound.

    Args:
    -----
    probe (Probe): Object containing the geometry of the probe elements with (x, y, z) coordinates.
    theta (float): Angle of the wavefront relative to the x-axis, specified in radians.
    sound_speed (float): Speed of sound in the medium, specified in meters per second.

    Returns:
    --------
    np.ndarray: A 1D NumPy array containing the computed time delays for each probe element.

    Example Usage:
    --------------
    >>> delays = calculate_element_delays_for_wavefront(probe, np.pi/6, 1540)
    >>> print(delays)

    """
    # Number of elements in the probe
    N = probe.element_num

    # Compute the wavefront direction vector
    v_x = np.sin(theta)  # x-component of wavefront direction
    v_y = 0              # Assume wavefront direction parallel to the y-axis
    v_z = np.cos(theta)  # z-component of wavefront direction

    # Normalize the direction vector
    wave_vector = np.array([v_x, v_y, v_z]) / np.linalg.norm([v_x, v_y, v_z])

    # Initialize delay array
    delays = np.zeros(N)

    # Compute delays for each probe element
    for i in range(N):
        # Extract element coordinates
        x_i = probe.geometry[i].x
        y_i = probe.geometry[i].y
        z_i = probe.geometry[i].z

        # Compute element position vector
        position_vector = np.array([x_i, y_i, z_i])

        # Compute projection of the position vector onto the wavefront direction
        projection_distance = np.dot(position_vector, wave_vector)

        # Compute time delay for the current element
        delays[i] = projection_distance / sound_speed

    # Return calculated delays
    return delays


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
    probe = Probe(0.3e-3, 0.18e-03, 0.12e-3, 5e-3, 64, "linear array")

    angles = np.linspace(-16, 16, 3).tolist()
    theta = np.radians(angles)
    print(theta)


    sound_speed = 1540

    print(theta.shape[0])

    delay = []
    for i in range(theta.shape[0]):
        delay.append(cal_plane_wave_transmit_delay(probe, theta[i], sound_speed))

    # print(delay)

    print(np.max(delay), np.min(delay))
    
    delay = np.array(delay)
    delay = delay - np.min(delay)
    delay = delay / 0.01e-6
    delay = delay.astype(int)
    # delay = convert_delay_profile(delay)
    delay = delay + 100
    print(delay)
    # delay = prepare_for_register(delay)

    delay = numpy_to_c_array(delay)

    with open("delay_profile.txt", "w", encoding="utf-8") as file:
        file.write(delay)