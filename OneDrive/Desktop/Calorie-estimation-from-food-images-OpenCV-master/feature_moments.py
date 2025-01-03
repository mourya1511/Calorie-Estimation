import numpy as np
import cv2
import sys

def getShapeFeatures(img):
    '''
    The shape features of an image are calculated
    based on the contour of the food item using Hu moments.
    '''
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    moments = cv2.moments(contours[0])
    hu = cv2.HuMoments(moments)
    feature = []
    for i in hu:
        feature.append(i[0])
    
    M = max(feature)
    m = min(feature)
    feature = list(map(lambda x: x * 2, feature))
    feature = [(x - M - m) / (M - m) for x in feature]
    mean = np.mean(feature)
    dev = np.std(feature)
    feature = [(x - mean) / dev for x in feature]
    
    return np.array(feature)

if __name__ == '__main__':
    img = cv2.imread(sys.argv[1])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(img, 80, 255)
    img1 = cv2.bitwise_and(img, img, mask=mask)
    h = getShapeFeatures(img1)
    print(h)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
