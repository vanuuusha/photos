import cv2

def find_end_y(img, ymin, xmin):
    for y in range(ymin, img.shape[1]):
        if img[xmin, y] > 250:
            return y
    return img.shape[1]


def find_end_x(img, ymin, xmin):
    for x in range(xmin, img.shape[0]):
        if img[x, ymin] > 250:
            return x
    return img.shape[0]


def start_find(img, ymin, xmin, name):
    ymax = find_end_y(img, ymin, xmin)
    xmax = find_end_x(img, ymin, xmin)
    if (xmax - xmin) < 10 or (ymax - ymin) < 10:
        pass
    else:
        new_image = img[xmin:xmax, ymin:ymax]
        cv2.imwrite('test/'+str(name) + '_corrected.png', new_image)
        img[xmin:xmax, ymin:ymax] = 255


def find_mini_images(img):
    index = 0
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if img[x, y] < 250:
                start_find(img, y, x, index)
                index += 1


def open_image(url):
    img = cv2.imread(url, cv2.IMREAD_GRAYSCALE)
    find_mini_images(img)


print('Введите номер картинки: ')
a = int(input())
print('Спасибо')
open_image(str(a) + '.png')