import cv2 
from matplotlib import pyplot as plt

from difflib import SequenceMatcher


def simtext(txt1, txt2):
    # compare text using difflib
    # Return a measure of the sequences’ similarity as a float in the range [0, 1].
    similar = SequenceMatcher(None, txt1, txt2).ratio()
    return similar

def simage(img1, img2):
    # find frequency of pixels in range 0-255
    histr1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    histr2 = cv2.calcHist([img2], [0], None, [256], [0, 256])

    similar = cv2.compareHist(histr1, histr2, cv2.HISTCMP_CORREL)
    return similar


def getVidDuration(vid):
    # get video duration
    fps = vid.get(cv2.CAP_PROP_FPS)
    frameCount = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frameCount / fps
    return duration

def simvid(vid1, vid2):
    totalsim = 0

    # set frequency and interval for both videos
    freq1 = 10
    freq2 = 10
    interval1 = getVidDuration(vid1) / freq1
    interval2 = getVidDuration(vid2) / freq2

    for count1 in range(freq1):
        vid1.set(cv2.CAP_PROP_POS_MSEC, count1 * interval1)
        success, image2 = vid2.read()

        maxsim = 0
        for count2 in range(freq2):
            vid2.set(cv2.CAP_PROP_POS_MSEC, count2 * interval2)
            success, image1 = vid1.read()

            similar = simage(image1, image2)
            # get frame with highest similarity
            if maxsim < similar:
                maxsim = similar
        # add max similarity for each interval frame
        totalsim += maxsim
        
    # get average similarity
    return totalsim / freq1


if __name__ == '__main__':
    # compare videos
    vid1 = cv2.VideoCapture('test.m4v')
    vid2 = cv2.VideoCapture('test1.mp4')
    print(simvid(vid1, vid2))

    # compare images
    img1 = cv2.imread('test1.jpg', 0)
    img2 = cv2.imread('test1b.jpg', 0)
    print(simage(img1, img2))

    # compare texts
    txt1 = "Dump Administration Dismisses Surgeon General Vivek Murthy (http)PUGheO7BuT5LUEtHDcgm"
    txt2 = "asd Dump werv Administration wer  Dismisses wer Surgeon sdf General Vivek Murthy (http)avGqdhRVOO"
    print(simtext(txt1, txt2))
