import cv2

# set screen visual appearance
COLOR = (0, 0, 255)
THICKNESS = 2


def applyMasks(frame, greenUpperBound, greenLowerBound):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # creates a mask for the color, do dilatations and erosions
    # to remove small blobs in the mask
    mask = cv2.inRange(hsv, greenLowerBound, greenUpperBound)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    return mask


def findCircleContour(contours):
    # find the largest contour in the mask, then use it to compute
    # the minimunm enclosing circle and centroid
    largestContour = max(contours, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(largestContour)
    return (x, y), radius, largestContour


def calculateCentroid(largestContour):
    M = cv2.moments(largestContour)
    if M["m00"] > 0:
        centroid = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        return centroid


def drawCircle(frame, center, radius):
    cv2.circle(frame, (int(center[0]), int(center[1])), int(radius), COLOR, THICKNESS)


def findScreenPosition(centroid, frame):
    position = ""

    if centroid[0] < (frame.shape[1] / 3):
        position = "Esquerda"
    elif centroid[0] < ((frame.shape[1] / 3) * 2):
        position = "Centro"
    else:
        position = "Direita"

    if centroid[1] < (frame.shape[0]/3):
        position += "-Cima"
    elif centroid[1] < ((frame.shape[0] / 3) * 2):
        position += "-Centro"
    else:
        position += "-Baixo"

    return position


def printDistance(frame, distance):
    cv2.putText(frame, "%.2f cm" % distance, (frame.shape[1] - 200, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, COLOR, THICKNESS)


def printPosition(frame, position):
    cv2.putText(frame, position, (50, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, COLOR, THICKNESS)
