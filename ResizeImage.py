import numpy as np
import math


class ResizeImage:
    # init method or constructor
    def __init__(self, height_factor, width_factor, img):
        self.height_factor = height_factor
        self.width_factor = width_factor
        self.img = img

    def pixelReplication(self):
        height, width = self.img.shape  # get image size

        # new size
        new_width = int(width * self.width_factor)
        new_height = int(height * self.height_factor)

        # new blank image
        new_image = np.zeros((new_height, new_width))

        for ROW in range(new_height):
            for COL in range(new_width):
                #  every output pixel is replaced by its nearest pixel in the input
                pixel = self.img[math.floor(ROW / self.height_factor), math.floor(COL / self.width_factor)]
                new_image[ROW, COL] = pixel

        return new_image

    def bicubicInterpolation(self):
        # Interpolation kernel
        def u(s, a):
            if (abs(s) >= 0) & (abs(s) <= 1):
                return (a + 2) * (abs(s) ** 3) - (a + 3) * (abs(s) ** 2) + 1
            elif (abs(s) > 1) & (abs(s) <= 2):
                return a * (abs(s) ** 3) - (5 * a) * (abs(s) ** 2) + (8 * a) * abs(s) - 4 * a
            return 0

        # Adding padding to the input image
        # Padding
        def padding(img, H, W):
            zimg = np.zeros((H + 4, W + 4))
            zimg[2:H + 2, 2:W + 2] = img

            # Pad the first/last two col and row
            zimg[2:H + 2, 0:2] = img[:, 0:1]
            zimg[H + 2:H + 4, 2:W + 2] = img[H - 1:H, :]
            zimg[2:H + 2, W + 2:W + 4] = img[:, W - 1:W]
            zimg[0:2, 2:W + 2] = img[0:1, :]

            # Pad the missing corner points
            zimg[0:2, 0:2] = img[0, 0]
            zimg[H + 2:H + 4, 0:2] = img[H - 1, 0]
            zimg[H + 2:H + 4, W + 2:W + 4] = img[H - 1, W - 1]
            zimg[0:2, W + 2:W + 4] = img[0, W - 1]

            return zimg

        # Writing the bicubic interpolation function
        # Get image size
        H, W = self.img.shape

        # Coefficient
        a = -1 / 2

        img = padding(self.img, H, W)

        # Create new image
        dH = math.floor(H * self.height_factor)
        dW = math.floor(W * self.width_factor)

        # Converting into matrix
        dst = np.zeros((dH, dW))
        # np.zeroes generates a matrix
        # consisting only of zeroes
        # Here we initialize our answer
        # (dst) as zero

        for j in range(dH):
            for i in range(dW):
                # Getting the coordinates of the
                # nearby values
                x, y = i * 1 / self.width_factor + 2, j * 1 / self.height_factor + 2

                x1 = 1 + x - math.floor(x)
                x2 = x - math.floor(x)
                x3 = math.floor(x) + 1 - x
                x4 = math.floor(x) + 2 - x

                y1 = 1 + y - math.floor(y)
                y2 = y - math.floor(y)
                y3 = math.floor(y) + 1 - y
                y4 = math.floor(y) + 2 - y

                # Considering all nearby 16 values
                mat_l = np.matrix([[u(x1, a), u(x2, a), u(x3, a), u(x4, a)]])
                mat_m = np.matrix([[img[int(y - y1), int(x - x1)],
                                    img[int(y - y2), int(x - x1)],
                                    img[int(y + y3), int(x - x1)],
                                    img[int(y + y4), int(x - x1)]],
                                   [img[int(y - y1), int(x - x2)],
                                    img[int(y - y2), int(x - x2)],
                                    img[int(y + y3), int(x - x2)],
                                    img[int(y + y4), int(x - x2)]],
                                   [img[int(y - y1), int(x + x3)],
                                    img[int(y - y2), int(x + x3)],
                                    img[int(y + y3), int(x + x3)],
                                    img[int(y + y4), int(x + x3)]],
                                   [img[int(y - y1), int(x + x4)],
                                    img[int(y - y2), int(x + x4)],
                                    img[int(y + y3), int(x + x4)],
                                    img[int(y + y4), int(x + x4)]]])
                mat_r = np.matrix(
                    [[u(y1, a)], [u(y2, a)], [u(y3, a)], [u(y4, a)]])

                # Here the dot function is used to get
                # the dot product of 2 matrices
                dst[j, i] = np.dot(np.dot(mat_l, mat_m), mat_r)

        return dst
