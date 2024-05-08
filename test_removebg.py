# import cv2
# import numpy as np

# # Read image
# img = cv2.imread('Project Push Git/Image/sample No.7.JPG')
# hh, ww = img.shape[:2]

# # threshold on white
# # Define lower and uppper limits
# lower = np.array([200, 200, 200])
# upper = np.array([255, 255, 255])

# # Create mask to only select black
# thresh = cv2.inRange(img, lower, upper)

# # apply morphology
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
# morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# # invert morp image
# mask = 255 - morph

# # apply mask to image
# result = cv2.bitwise_and(img, img, mask=mask)


# # save results
# cv2.imwrite('pills_thresh.jpg', thresh)
# cv2.imwrite('pills_morph.jpg', morph)
# cv2.imwrite('pills_mask.jpg', mask)
# cv2.imwrite('pills_result.jpg', result)

# cv2.imshow('thresh', thresh)
# cv2.imshow('morph', morph)
# cv2.imshow('mask', mask)
# cv2.imshow('result', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


import cv2
# from skimage import io  # Only needed for web grabbing images, use cv2.imread for local images

# Read images from web
img_bg = cv2.cvtColor(io.imread('https://i.stack.imgur.com/rMoqy.jpg'), cv2.COLOR_RGB2BGR)
img = cv2.cvtColor(io.imread('https://i.stack.imgur.com/oyrKo.jpg'), cv2.COLOR_RGB2BGR)

# Set up and feed background subtractor (cf. tutorial linked in question)
backSub = cv2.createBackgroundSubtractorMOG2()
_ = backSub.apply(img_bg)
mask = backSub.apply(img)

# Morphological opening and closing to improve mask
mask_morph = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
mask_morph = cv2.morphologyEx(mask_morph, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))

# Generate output
output = cv2.bitwise_and(img, img, None, mask_morph)

# Visualization
cv2.imshow('img', img)
cv2.imshow('mask', mask)
cv2.imshow('mask_morph', mask_morph)
cv2.imshow('output', output)
cv2.waitKey(0)
cv2.destroyAllWindows()