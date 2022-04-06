import cv2
import os


def find_end_y(img, ymin, xmin):
    for y in range(ymin, img.shape[1]):
        if [i for i in range(3) if img[xmin, y][i] > 250]:
            return y
    return img.shape[1]


def find_end_x(img, ymin, xmin):
    for x in range(xmin, img.shape[0]):
        if [i for i in range(3) if img[x, ymin][i] > 250]:
            return x
    return img.shape[0]


def start_find(img, ymin, xmin, name, name_folder):
    ymax = find_end_y(img, ymin, xmin)
    xmax = find_end_x(img, ymin, xmin)
    if (xmax - xmin) < 40 or (ymax - ymin) < 40:
        pass
    else:
        new_image = img[xmin+1:xmax-3, ymin:ymax]
        cv2.imwrite('test/'+str(name) + '_corrected' + '_from_image_' + str(name_folder) + '.png', new_image)
        img[xmin:xmax, ymin:ymax] = [255, 255, 255]


def find_mini_images(img, name_folder):
    index = 0
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if [i for i in range(3) if img[x, y][i] < 250]:
                start_find(img, y, x, index, name_folder)
                index += 1


def open_image(url):
    img = cv2.imread(url, cv2.IMREAD_COLOR)
    print('new_image', url[url.index(os.path.sep)+1:url.index('.')])
    find_mini_images(img, url[url.index(os.path.sep)+1:url.index('.')])


def start_program(folder_name):
    for photo in os.listdir(folder_name):
        open_image(os.path.join(folder_name, photo))


def renamer(folder_name):
    index = 1000
    for photo in os.listdir(folder_name):
        if photo.endswith(".png"):
            index += 1
            os.rename(os.path.join(folder_name, photo), os.path.join(folder_name, str(index) + '.png'))

    start_program(folder_name)


def start():
    print('Введите название папка (в данной директории)')
    folder_name = input()
    renamer(folder_name)


if __name__ == '__main__':
    start()