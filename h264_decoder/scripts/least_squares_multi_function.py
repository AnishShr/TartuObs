import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import lstsq

# Sample data for the four functions (replace with your actual data)
timestamps1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # Timestamps for function 1
timestamps2 = np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5])  # Timestamps for function 2
timestamps3 = np.array([1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2, 8.2, 9.2, 10.2])  # Timestamps for function 3
timestamps4 = np.array([1.7, 2.7, 3.7, 4.7, 5.7, 6.7, 7.7, 8.7, 9.7, 10.7])  # Timestamps for function 4

yaw_values1 = np.array([0.1, 0.9, 1.4, 2.0, 2.3, 2.1, 1.8, 1.5, 1.0, 0.5])  # Yaw values for function 1
yaw_values2 = np.array([0.2, 1.0, 1.6, 2.1, 2.5, 2.2, 1.9, 1.4, 0.8, 0.3])  # Yaw values for function 2
yaw_values3 = np.array([0.3, 1.2, 1.8, 2.3, 2.7, 2.4, 2.0, 1.6, 1.1, 0.7])  # Yaw values for function 3
yaw_values4 = np.array([0.4, 1.5, 2.0, 2.5, 2.9, 2.6, 2.2, 1.7, 1.2, 0.8])  # Yaw values for function 4

# Combine yaw values from all four functions
combined_yaw_values = np.concatenate((yaw_values1, yaw_values2, yaw_values3, yaw_values4))

# Combine timestamps for all four functions
combined_timestamps = np.concatenate((timestamps1, timestamps2, timestamps3, timestamps4))

# Degree of the polynomial to fit
degree = 9

# Construct the design matrix using polynomial terms up to the specified degree
X = np.vstack([combined_timestamps**i for i in range(degree + 1)]).T

# Solve the least squares problem
coefficients, residuals, rank, s = lstsq(X, combined_yaw_values, rcond=None)

# Predicted yaw values at original timestamps using the fitted model
fitted_yaw_values = X @ coefficients

# Calculate the average of timestamps and fitted values
average_timestamps = np.mean([timestamps1, timestamps2, timestamps3, timestamps4], axis=0)
average_fitted_values = np.mean([fitted_yaw_values[:len(timestamps1)], 
                                 fitted_yaw_values[len(timestamps1):len(timestamps1)+len(timestamps2)], 
                                 fitted_yaw_values[len(timestamps1)+len(timestamps2):len(timestamps1)+len(timestamps2)+len(timestamps3)], 
                                 fitted_yaw_values[len(timestamps1)+len(timestamps2)+len(timestamps3):]], axis=0)

# Plotting the data and the average fitted values
plt.plot(average_timestamps, average_fitted_values, color='black', label='Average Fitted Function', linewidth=4)
plt.plot(timestamps1, yaw_values1, color='blue', label='Original Data Function 1', linewidth=2)
plt.plot(timestamps2, yaw_values2, color='orange', label='Original Data Function 2', linewidth=2)
plt.plot(timestamps3, yaw_values3, color='purple', label='Original Data Function 3', linewidth=2)
plt.plot(timestamps4, yaw_values4, color='green', label='Original Data Function 4', linewidth=2)

plt.scatter(average_timestamps, average_fitted_values, color='black', linewidth=5)
plt.scatter(timestamps1, yaw_values1, color='blue')
plt.scatter(timestamps2, yaw_values2, color='orange')
plt.scatter(timestamps3, yaw_values3, color='purple')
plt.scatter(timestamps4, yaw_values4, color='green')


plt.xlabel('Timestamp')
plt.ylabel('Yaw')
plt.legend()
plt.title(f'Average Least Squares Fit with Polynomial Degree {degree}')
plt.grid()
plt.show()

# Print coefficients
print(f"Coefficients of the fitted model (degree {degree}):", coefficients)

print(f"combined timesteps:\n{combined_timestamps}")
print(f"fitted value:\n{fitted_yaw_values}")
