import numpy as np
import matplotlib.pyplot as plt

# Generate ABCD matrices
def ABCDspace(d: float, n: float) -> np.ndarray:
    return np.array([[1, d/n], [0, 1]])


def ABCDlens(f: float) -> np.ndarray:
    return np.array([[1, 0], [-1/f, 1]])


# Get beam parameters from ABCD matrix
def beamWaist(ABCD: np.ndarray, w0: float, wave: float) -> float:
    zr = np.pi * w0**2 / wave
    return np.sqrt(w0**2 * ((ABCD[0, 1]**2 + ABCD[0, 0]**2 * zr**2) / zr**2))

def beamRadius(ABCD: np.ndarray, w0: float, wave: float) -> float:
    zr = np.pi * w0**2 / wave
    return (ABCD[0, 1]**2 + ABCD[0, 0]**2 * zr**2) / (ABCD[0, 1] * ABCD[1, 1] + ABCD[0, 0] * ABCD[1, 0] * zr**2)


# Generate beam intensities
def intensityGauss(rr: np.ndarray, w0:float, w: float):
    return (w0/w)**2 * np.exp(-2 * (rr/w)**2)

def intensitySum(rr: np.ndarray, w0: float, w1: float, w2: float, R1: float, R2: float, C1: float, C2: float, opd: float, k: float) -> np.ndarray:
    # Phase difference
    delta = k * (opd + rr**2 / (2*R2) - rr**2 / (2*R1))

    # Intensities of each beam
    I1 = intensityGauss(rr, w0, w1) * np.abs(C1)
    I2 = intensityGauss(rr, w0, w2) * np.abs(C2)
    
    # Total intensity
    return I1 + I2 + 2 * np.sqrt(I1 * I2) * np.cos(delta)

def plotGauss(ABCD: np.ndarray, w0: float, wave: float, rr: np.ndarray, Imax = 1.0, label = "ABCD Calculation", scale = 0.001) -> None:
    """
        Given the beam parameters return the beam intensity at the points stored in `rr`.
    """

    # Calculate new beam waist
    w = beamWaist(ABCD, w0, wave)

    # Generate the beam intensities
    ii = intensityGauss(rr, w0, w)
    ii = ii * Imax / np.max(ii)

    # Plot the beam intensities
    plt.plot(rr / scale, ii, label=label)

    return
