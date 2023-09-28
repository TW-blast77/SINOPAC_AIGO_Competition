import cv2
import numpy as np
import matplotlib.pyplot as plt

def whole_img_dct(img_f32):
    img_dct = cv2.dct(img_f32)            
    img_dct_log = np.log(abs(img_dct))    
    img_idct = cv2.idct(img_dct)          
    return img_dct_log, img_idct


def block_img_dct(img_f32):
    height,width = img_f32.shape[:2]
    block_y = height // 8
    block_x = width // 8
    height_ = block_y * 8
    width_ = block_x * 8
    img_f32_cut = img_f32[:height_, :width_]
    img_dct = np.zeros((height_, width_), dtype=np.float32)
    new_img = img_dct.copy()
    for h in range(block_y):
        for w in range(block_x):
            
            img_block = img_f32_cut[8*h: 8*(h+1), 8*w: 8*(w+1)]
            img_dct[8*h: 8*(h+1), 8*w: 8*(w+1)] = cv2.dct(img_block)

            
            dct_block = img_dct[8*h: 8*(h+1), 8*w: 8*(w+1)]
            img_block = cv2.idct(dct_block)
            new_img[8*h: 8*(h+1), 8*w: 8*(w+1)] = img_block
    img_dct_log2 = np.log(abs(img_dct))
    return img_dct_log2, new_img


if __name__ == '__main__':
    img_u8 = cv2.imread("lena5_2.raw", 0)
    img_f32 = img_u8.astype(float)  # Use built-in float type
    img_dct_log, img_idct = whole_img_dct(img_f32)
    img_dct_log2, new_img = block_img_dct(img_f32.copy())

    plt.figure(6, figsize=(12, 8))
    plt.subplot(231)
    plt.imshow(img_u8, 'gray')
    plt.title('original image'), plt.xticks([]), plt.yticks([])
    plt.subplot(232)
    plt.imshow(img_dct_log)
    plt.title('DCT'), plt.xticks([]), plt.yticks([])
    plt.subplot(233)
    plt.imshow(img_idct, 'gray')
    plt.title('IDCT'), plt.xticks([]), plt.yticks([])
    plt.subplot(234)
    plt.imshow(img_dct_log2)
    plt.title('block_DCT'), plt.xticks([]), plt.yticks([])
    plt.subplot(235)
    plt.imshow(new_img, 'gray')
    plt.title('block_IDCT'), plt.xticks([]), plt.yticks([])
    plt.show()
