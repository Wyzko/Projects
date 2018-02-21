# Imports
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
from sklearn.metrics import confusion_matrix

# Abstract distance for the classification of unrecognize signs
MAX_DISTANCE = 999999999

# Main method
def main():
    # Initialisation of the test and reference folders
    folder_ref = 'img/ref'
    folder_test = 'img/test'
    current_result = []
    final_result = []

    # Results we want to retrieve
    true_classes = ["3","3","3","2","2","1","1","2","2","1","4","4","4","5","5","5","5","6","6","6",
    "6","6","6","7","7","7","7","7","5","1","1","1","4","4","4","7","2","2","2","2","2","3","3","3","3",
    "3","3","3","1","4","4","4","4","1","5","5","5","5","5","6","6","6","1","7","7","6","2","1","7","7"]

    print('Calcul des couples d\'images reconnues........')

    # Loop on the test images
    for tf in range(1,71):
        test_file = folder_test + '/' + str(tf) + '.jpg'
        img1 = cv2.imread(test_file)
        # Loop on the different classes
        for c in range(1,8):
            ref_prefix = folder_ref + '/' + str(c) + '/'
            # Loop on the refrence images
            for rf in range(1,8):
                ref_file = ref_prefix + str(rf) + '.jpg'
                img2 = cv2.imread(ref_file)
                current_result.append(sift(img1,img2,test_file,ref_file))

        current_result= [i for i in current_result if i != None]
        tf_classification = minimise_distance(current_result)
        final_result.append(tf_classification)
        current_result = []

    format_result(final_result)
    predetermined_classes = getClassesArray(final_result)

    # Creation of a confusion matrix
    createConfusionMatrix(predetermined_classes,true_classes)


# Method that create a confusion matrix, based on the results of the SIFT algorithm
def createConfusionMatrix(expectedData,estimatedData):
    conf_matrix = confusion_matrix(expectedData, estimatedData)
    print(conf_matrix)
    norm_conf = []
    for i in conf_matrix:
        a = 0
        tmp_arr = []
        a = sum(i, 0)
        for j in i:
            tmp_arr.append(float(j)/float(a))
        norm_conf.append(tmp_arr)

    fig = plt.figure()
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    res = ax.imshow(np.array(norm_conf), cmap=plt.cm.jet,
                    interpolation='nearest')

    width, height = conf_matrix.shape

    for x in xrange(width):
        for y in xrange(height):
            ax.annotate(str(conf_matrix[x][y]), xy=(y, x),
                        horizontalalignment='center',
                        verticalalignment='center')

    cb = fig.colorbar(res)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    plt.xticks(range(width), alphabet[:width])
    plt.yticks(range(height), alphabet[:height])
    plt.savefig('confusion_matrix.png', format='png')


# Method to get the class of an image
def getClassesArray(association_array):
    class_array = []
    for tupl in association_array:
        class_array.append(getClass(tupl[1]))
    return class_array


# Method that minimize the distance of the test images
def minimise_distance(tuples):
    if (len(tuples)>0):

        # trie par ordre croissant par rapport au 3eme element de la liste de tuple
        tuples.sort(key=itemgetter(2))
        print tuples[0]
        print tuples[1]
        print tuples[2]
        if tuples[1][2]==MAX_DISTANCE:
            return "unknown"
        if (getClass(tuples[1][1]) == getClass(tuples[2][1])):
            return tuples[1]
        else:
            return tuples[0]


#affichage des resultats sous forme textuelle
def format_result(result):
    for tup in result:
        if (tup != None) & (tup!="unknown"):
            line = tup[0] +'  ->  '+ getClass(tup[1]) +' ( '+tup[1]+' )'
            print(line+'\n')


# Method that retrieve the class of the reference image
def getClass(string):
    if string == "unknown":
        return string;
    else:
        string_array = string.split('/')
        if (len(string_array) > 3):
            return string_array[2]
        else:
            return "Error while getting the associated class"


# Method that use the SIFT algorithm to classify the images
def sift(im1, im2, name1, name2):
    img1 = im1
    img2 = im2
    good = []
    distance = 0
    distance_min = MAX_DISTANCE

    # SIFT descriptor Initialisation
    sift = cv2.xfeatures2d.SIFT_create()

    # Retrival of the descriptors and the key points of the 2 images
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    # Creation of a list with the key points that match in the 2 images
    for m, n in matches:
        # Lowe's ratio test
        if m.distance < 0.7*n.distance:
            good.append(m)

    # If there is more that 10 points that match, the 2 images can be the same
    if len(good)>5:
        # print(m.trainIdx)
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        # Computation of the hommography with the RANSAC method
        H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,8.0)
        if H is not None:
            estimatedPoints = cv2.perspectiveTransform(src_pts,H)

            distance = computeDistance(estimatedPoints, dst_pts)

            if(distance < distance_min):
                distance_min = distance
        else:
            distance_min = MAX_DISTANCE
    else:
        distance_min = MAX_DISTANCE

    return(name1, name2, distance_min)


# Method to compute the distance between points
def computeDistance(realKeyPoints, estimatedKeyPoints):
    error_pt = 0
    for i in range(0,len(realKeyPoints)):
        realKeyPoint = realKeyPoints[i,0]
        estimatedKeyPoint = estimatedKeyPoints[i,0]
        error_pt = error_pt + math.sqrt(pow(estimatedKeyPoint[0] - realKeyPoint[0],2) + pow(estimatedKeyPoint[1] - realKeyPoint[1], 2))
    return error_pt


if __name__ == "__main__":
    main()
