import math
# Given array representing the ellipse
ellipse_info = ((209.2367706298828, 141.32044982910156), (206.10877990722656, 271.5523681640625), 91.75446319580078)

# Unpack the array into separate variables
center = ellipse_info[0]
majorAxis = (ellipse_info[1][0])/2
minorAxis = (ellipse_info[1][1])/2
angle = ellipse_info[2]

print("Center (pixel):", center)
print("Major Axis (pixel):", majorAxis)
print("Minor Axis (pixel):", minorAxis)
print("Angle (degree):", angle)
# Convert angle to radians
angle_rad = math.radians(angle)

# Calculate area
area = math.pi * majorAxis * minorAxis

print("Area of the ellipse:", area)
print("math.pi",math.pi)