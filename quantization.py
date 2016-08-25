import numpy as np
import cv2
import xlwt
import csv


GRID_SPACE = 7
LENGTH = 96


# def base16(n):
#     a = np.base_repr(n, 16)
#     if len(a) == 1:
#         return "0" + a
#     else:
#         return a
#
# def rgbToHex(r,g,b):
#     print "#" + base16(r) + base16(g) + base16(b)
#
# rgbToHex(50,255,0)

### The 48 * 48 project

img = cv2.imread('logo17.jpg')
img = cv2.resize(img, (LENGTH, LENGTH))
Z = img.reshape((-1,3))

# convert to np.float32
Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 7
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))
res3 = res2
# res3 = cv2.resize(res2, (96,96))

palette = []



build_palette('Lego-colors-palette-2010.gpl.csv')


def fit_palette(pic, palette):

    def nearestColor(pixel, palette):
        MAX_DIFF = pow(pow(255, 2) * 3, .5)
        nearest_color, smallest_val = 0, MAX_DIFF
        r,g,b = pixel
        for p in palette:
            r2, g2, b2 = p
            val = pow(pow(r - r2, 2) + pow(g - g2, 2) + pow(b - b2, 2), .5)
            if (smallest_val > val):
                # print smallest_val
                smallest_val = val
                nearest_color = p
        return nearest_color

    h,w = len(pic[0]), len(pic)
    print h, w
    print len(pic[0])
    output = np.zeros((w,h,3), np.uint8)
    for y, row in enumerate(pic):
        for x, color in enumerate(row):
            # print len(output[y][x])
            # print x
            a = nearestColor(pic[y][x], palette)
            output[y][x] = a
    return output


# res4 = fit_palette(res3, palette)
# cv2.imshow('output', res4)
# cv2.waitKey(0)


def gen_xls(colors, pic, grid_size):
    # Create a black image
    h,w = len(pic[0]) * grid_size, len(pic) * grid_size
    output = np.zeros((w,h,3), np.uint8)
    for y, row in enumerate(pic):
         for x, color in enumerate(row):
             r,g,b = color
             r = int(r)
             g = int(g)
             b = int(b)
             cv2.rectangle(output,
                (x * grid_size, y * grid_size),
                ((x + 1) * grid_size,(y + 1) * grid_size)
                ,(r,g,b),-2)
    return output

# gen_xls(center, res3, 10)
res4 = fit_palette(res3, palette)

def draw_grid(pic, grid_size, grid_color):
    h,w = len(pic[0]), len(pic)
    for y in xrange(0, h, grid_size):
        cv2.line(pic, (0, y), (w, y), grid_color)
    for x in xrange(0, w, grid_size):
        cv2.line(pic, (x, 0), (x, h), grid_color)



res5 = gen_xls(center, res4, GRID_SPACE)

draw_grid(res5, GRID_SPACE, (200,200,200))
draw_grid(res5, GRID_SPACE * 10, (0,0,200))

cv2.imshow('output', res5)
cv2.imwrite('plan.png',res5)
cv2.waitKey(0)

# cv2.imwrite('output.png',res3)
# cv2.imshow('res3',res3)
# cv2.waitKey(0)
cv2.destroyAllWindows()
