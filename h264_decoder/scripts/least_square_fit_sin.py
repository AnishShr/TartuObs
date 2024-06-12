import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Generate data points for the first sine function
x1 = np.linspace(0, 2*np.pi, 100)
y1 = np.sin(x1)

# Generate data points for the second sine function
x2 = np.linspace(0.2, 2*np.pi + 0.2, 100)
y2 = 3 * np.sin(x2 + np.pi/4) + 0.3

# # Interpolate the first sine function at the x-coordinate of the first point of the second sine function
# interp_cubic = interp1d(x1, y1, kind='cubic')
# y_interp_x2_0 = interp_cubic(x2[0])

# Define the error function (residuals)
def error_func(params, x1, y1, x2, y2):
    A, y0, delta_t = params
    interp_func = interp1d(x1 + delta_t, y1, kind='cubic', fill_value="extrapolate")
    y1_shifted_scaled = A * (interp_func(x2) + y0)
    return y1_shifted_scaled - y2

# Initial guess for the parameters A, y0 and delta_t
initial_guess = [1, 0, 0]

# Fit the second sine function to the first using least squares
result = least_squares(error_func, initial_guess, args=(x1, y1, x2, y2))

# Extract the parameters A and y0
A_fit, y0_fit, delta_t_fit = result.x

# Create the fitted curve
interp_func = interp1d(x1 + delta_t_fit, y1, kind='cubic', fill_value="extrapolate")
y_fitted = A_fit * (interp_func(x2) + y0_fit)

# Plot the original data and the fitted line
plt.plot(x1, y1, label='First Sine Function')
plt.plot(x2, y2, label='Second Sine Function')
plt.plot(x2, y_fitted, 'x', label='Fitted Second Sine Function to First', linestyle='dashed')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Least Squares Fitting of Second Sine Function to First')
plt.grid(True)
plt.show()

print(f"Estimated scale factor (A): {A_fit}")
print(f"Estimated y-offset (y0): {y0_fit}")
print(f"Estimated delta_t: {delta_t_fit}")
