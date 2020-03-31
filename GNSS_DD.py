import math
import numpy as np

"""
The data contains 3 epochs of phase and pseudorage observations measured on a calibration baseline in valencia, spain.
The sensors used are geodetic quality recievers using choke ring antennas.
The reciever on pillar 1A is treated as the reference reciever.
"""

# X, Y, Z ECEF coordinates for the phase center of the recievers
pillar_1A_base = np.array([[4929635.400], [-29041.877], [4033567.846]])  # Refernence reciever
pillar_3A_rover = np.array([[4929605.400], [-29123.700], [4033603.800]])

"""
ECEF coordinates (m) of the satelite phase centers when they transmitted the signals measured at each epoch.
"""
# ECEF SATELLITE POSITIONS X, Y, Z (m) (already corrected for earth rotation during signal travel time)
# 2016 11 15 22 19  5

G10 = [4634093.207, -19899701.050, 16933747.321]
G12 = [22559170.178, -8979632.676, 10377257.530]
G13 = [23277536.897, 12575815.276, -2029027.200]
G15 = [25950462.808, 2443858.353, 5881092.070]
G17 = [5785091.956, 16827408.400, 20125597.869]
G18 = [13564948.214, -21357948.777, 8232124.013]
G19 = [12262838.101, 17165601.305, 15682863.092]
G24 = [15569244.807, -1039249.482, 21443791.252]

"""
Use double differenced phase measurements, from the first epoch of data only 2016_11_15_22_19_5
TO compute the precise coordinates of the pillar 3A sensor phase center. 
These are pseudo range measurements 
"""

# BASE OBSERVATIONS (Pillar 1A) C1C (metres), L1C (L1 cycles)
# 2016_11_15_22_19_5

G10_base_obs = [23726969.123, 124686036.295]
G12_base_obs = [20647534.024, 108503516.027]
G13_base_obs = [23087780.798, 121327099.499]
G15_base_obs = [21346539.664, 112176830.803]
G17_base_obs = [23379753.757, 122861442.012]
G18_base_obs = [23217805.737, 122010370.583]
G19_base_obs = [22181729.713, 116565751.296]
G24_base_obs = [20436699.926, 107395596.426]

# ROVER OBSERVATIONS (Pillar 3A) C1C (metres), L1C (L1 cycles)
# 2016 11 15 22 19  5

G10_rover_obs = [23726881.094, 124685588.685]  # meters, cycles
G12_rover_obs = [20647514.655, 108503447.644]
G13_rover_obs = [23087860.345, 121327512.345]
G15_rover_obs = [21346576.786, 112177022.660]
G17_rover_obs = [23379790.820, 122861635.973]
G18_rover_obs = [23217736.821, 122010019.631]
G19_rover_obs = [22181785.598, 116566080.299]
G24_rover_obs = [20436682.002, 107395502.123]

# At the first epoch we have 16 raw phase observations in cycles.
l = np.transpose([G10_base_obs[1], G10_rover_obs[1],
                  G12_base_obs[1], G12_rover_obs[1],
                  G13_base_obs[1], G13_rover_obs[1],
                  G15_base_obs[1], G15_rover_obs[1],
                  G17_base_obs[1], G17_rover_obs[1],
                  G18_base_obs[1], G18_rover_obs[1],
                  G19_base_obs[1], G19_rover_obs[1],
                  G24_base_obs[1], G24_rover_obs[1]])

"""
Standard Deviations
L1C variance for satellite at elevation angle E: s*s/sin(E)
NOTE: Satellite G24 has the highest elevation: 71 degrees.

"""
elevation_angle_e = 71
l1c_standard_deviation_s = 0.003


def variance(s, e):
    a = s * s / math.cos(e)
    return a


l1c_variance = variance(l1c_standard_deviation_s, elevation_angle_e)

"""
Phase Ambiguity terms (N) for each measurement, before and after ambiguity resolution 
Use integer terms in computations
2016 11 15 22 19  5
G24 is a reference satelite - and has the highest 
"""

# Phase ambiguities for each epoch and each phase measurement:

before_ambiguity_resolution = np.array([[4929605.364], [-29123.817], [4033603.867]])
(G24toG10_before) = 12.564
(G24toG12_before) = 34.873
(G24toG13_before) = -3.838
(G24toG15_before) = -4.170
(G24toG17_before) = 1.538
(G24toG18_before) = 11.324
(G24toG19_before) = 34.352

after_ambiguity_resolution = np.array([[4929605.542], [-29123.828], [4033603.932]])
(G24toG10_after) = int(12.000)
(G24toG12_after) = int(35.000)
(G24toG13_after) = int(-4.000)
(G24toG15_after) = int(-4.000)
(G24toG17_after) = int(1.000)
(G24toG18_after) = int(11.000)
(G24toG19_after) = int(34.000)

"""
Try to get your answer close to the figures for 3A. The nominal coordinates given mean you do not need to iterate the 
least squares solution, you should converge on the answer with on round of matrix inversion
"""

# 16 x 8:  Differencing matrix
s = np.array([[1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -1]])

D = np.array([[1, -1, 0, 0, 0, 0, 0, 0],
              [1, 0, -1, 0, 0, 0, 0, 0],
              [1, 0, 0, -1, 0, 0, 0, 0],
              [1, 0, 0, 0, -1, 0, 0, 0],
              [1, 0, 0, 0, 0, -1, 0, 0],
              [1, 0, 0, 0, 0, 0, -1, 0],
              [1, 0, 0, 0, 0, 0, 0, -1]])


def x_differential(reference_station, satelite_corresponding, satelite_reference, wavelenth):
    # Extract Coordinates
    X_3A = reference_station[0]
    Y_3A = reference_station[1]
    Z_3A = reference_station[2]

    X_s = satelite_corresponding[0]
    Y_s = satelite_corresponding[1]
    Z_s = satelite_corresponding[2]

    X_s_ref = satelite_reference[0]
    Y_s_ref = satelite_reference[1]
    Z_s_ref = satelite_reference[2]

    result = 1 / wavelenth * \
             (
                     (X_3A - X_s) /
                     (math.sqrt((X_s - X_3A) ** 2 + (Y_s - Y_3A) ** 2 + (X_s - X_3A) ** 2 + (Z_s - Z_3A) ** 2))
                     -
                     (X_3A - X_s_ref) /
                     (math.sqrt(X_s_ref - X_3A) ** 2 + (Y_s_ref - Y_3A) ** 2 + (X_s_ref - X_3A) ** 2 +
                      (Z_s_ref - Z_3A) ** 2)
             )
    return float(result)


def y_differential(reference_station, satelite_corresponding, satelite_reference, wavelenth):
    # Extract Coordinates
    X_3A = reference_station[0]
    Y_3A = reference_station[1]
    Z_3A = reference_station[2]

    X_s = satelite_corresponding[0]
    Y_s = satelite_corresponding[1]
    Z_s = satelite_corresponding[2]

    X_s_ref = satelite_reference[0]
    Y_s_ref = satelite_reference[1]
    Z_s_ref = satelite_reference[2]

    result = 1 / wavelenth * \
             (
                     (Y_3A - Y_s) /
                     (math.sqrt((X_s - X_3A) ** 2 + (Y_s - Y_3A) ** 2 + (X_s - X_3A) ** 2 + (Z_s - Z_3A) ** 2))
                     -
                     (Y_3A - Y_s_ref) /
                     (math.sqrt(X_s_ref - X_3A) ** 2 + (Y_s_ref - Y_3A) ** 2 + (X_s_ref - X_3A) ** 2 +
                      (Z_s_ref - Z_3A) ** 2)
             )
    return float(result)


def z_differential(reference_station, satelite_corresponding, satelite_reference, wavelenth):
    # Extract Coordinates
    X_3A = reference_station[0]
    Y_3A = reference_station[1]
    Z_3A = reference_station[2]

    X_s = satelite_corresponding[0]
    Y_s = satelite_corresponding[1]
    Z_s = satelite_corresponding[2]

    X_s_ref = satelite_reference[0]
    Y_s_ref = satelite_reference[1]
    Z_s_ref = satelite_reference[2]

    result = 1 / wavelenth * \
             (
                     (Z_3A - Z_s) /
                     (math.sqrt((X_s - X_3A) ** 2 + (Y_s - Y_3A) ** 2 + (X_s - X_3A) ** 2 + (Z_s - Z_3A) ** 2))
                     -
                     (Z_3A - Z_s_ref) /
                     (math.sqrt(X_s_ref - X_3A) ** 2 + (Y_s_ref - Y_3A) ** 2 + (X_s_ref - X_3A) ** 2 +
                      (Z_s_ref - Z_3A) ** 2)
             )
    return float(result)


if __name__ == "__main__":
    print("Script start")

    """
    Typical observation rates might be every second / 5s / 10s / 30s
    2 stations 
    8 satellites 
    60 seconds per minute 
    If the A to B was tracked for 10 minutes: 
    2 x 8 x 60 x 10 = 9600
    9600 measurements
    We are assuming tha
    """

    print(l)

    # Calculate the vector of single differences
    sl = s.dot(l)

    # Calculate the vector of double differences
    Dsl = D.dot(sl)
    print(Dsl)

    wavelength = G10[1] / G10[0]

    # Constructing the Design Matrix
    design = np.array([

    [x_differential(pillar_1A_base, G10, G24, wavelength),
     y_differential(pillar_1A_base, G10, G24, wavelength),
     z_differential(pillar_1A_base, G10, G24, wavelength), 1, 0, 0, 0, 0, 0, 0],

    [x_differential(pillar_1A_base, G12, G24, wavelength),
     y_differential(pillar_1A_base, G12, G24, wavelength),
     z_differential(pillar_1A_base, G12, G24, wavelength), 0, 1, 0, 0, 0, 0, 0],

    [x_differential(pillar_1A_base, G13, G24, wavelength),
     y_differential(pillar_1A_base, G13, G24, wavelength),
     z_differential(pillar_1A_base, G13, G24, wavelength), 0, 0, 1, 0, 0, 0, 0],

    [x_differential(pillar_1A_base, G15, G24, wavelength),
     y_differential(pillar_1A_base, G15, G24, wavelength),
     z_differential(pillar_1A_base, G15, G24, wavelength), 0, 0, 0, 1, 0, 0, 0],

    [x_differential(pillar_1A_base, G17, G24, wavelength),
     y_differential(pillar_1A_base, G17, G24, wavelength),
     z_differential(pillar_1A_base, G17, G24, wavelength), 0, 0, 0, 0, 1, 0, 0],

    [x_differential(pillar_1A_base, G18, G24, wavelength),
     y_differential(pillar_1A_base, G18, G24, wavelength),
     z_differential(pillar_1A_base, G18, G24, wavelength), 0, 0, 0, 0, 0, 1, 0],

    [x_differential(pillar_1A_base, G19, G24, wavelength),
     y_differential(pillar_1A_base, G19, G24, wavelength),
     z_differential(pillar_1A_base, G19, G24, wavelength), 0, 0, 0, 0, 0, 0, 1],

    ])


    # Weight matrices
    









