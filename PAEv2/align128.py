from cgi import print_arguments
import cv2
import dlib
import numpy as np
import os
from PIL import Image

class Face_Align(object):
    def __init__(self,shape_predictor_path):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(shape_predictor_path)
        self.LEFT_EYE_INDICES = [36, 37, 38, 39, 40, 41]
        self.RIGHT_EYE_INDICES = [42, 43, 44, 45, 46, 47]

    def rect_to_tuple(self, rect):
        left = rect.left()
        right = rect.right()
        top = rect.top()
        bottom = rect.bottom()
        return left, top, right, bottom

    def extract_eye(self, shape, eye_indices):
        points = map(lambda i: shape.part(i), eye_indices)
        return list(points)

    def extract_eye_center(self, shape, eye_indices):
        points = self.extract_eye(shape, eye_indices)
        xs = map(lambda p: p.x, points)
        ys = map(lambda p: p.y, points)
        return sum(xs) // 6, sum(ys) // 6

    def extract_left_eye_center(self, shape):
        return self.extract_eye_center(shape, self.LEFT_EYE_INDICES)

    def extract_right_eye_center(self, shape):
        return self.extract_eye_center(shape, self.RIGHT_EYE_INDICES)

    def angle_between_2_points(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        tan = (y2 - y1) / (x2 - x1)
        return np.degrees(np.arctan(tan))

    def get_rotation_matrix(self, p1, p2):
        angle = self.angle_between_2_points(p1, p2)
        x1, y1 = p1
        x2, y2 = p2
        xc = (x1 + x2) // 2
        yc = (y1 + y2) // 2
        M = cv2.getRotationMatrix2D((xc, yc), angle, 1)
        return M

    def crop_image(self, image, det):
        left, top, right, bottom = self.rect_to_tuple(det)
        return image[top:bottom, left:right]

    def __call__(self, image=None,image_path=None,save_path=None,only_one=True):
        '''
        Face alignment, can select input image variable or image path, when input
        image format that return alignment face image crop or image path as input
        will return None but save image to the save path.
        :image: Face image input
        :image_path: if image is None than can input image
        :save_path: path to save image
        :detector: detector = dlib.get_frontal_face_detector()
        :predictor: predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        '''
        if image is not None:
            # convert BGR format to Gray
            image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        elif image_path is not None:
            image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            image = cv2.imread(image_path)

        height, width = image.shape[:2]

        # Dector face
        dets = self.detector(image_gray, 1)

        # i donate the i_th face detected in image
        crop_images = []
        for i, det in enumerate(dets):
            shape = self.predictor(image_gray, det)

            left_eye = self.extract_left_eye_center(shape)
            right_eye = self.extract_right_eye_center(shape)

            M = self.get_rotation_matrix(left_eye, right_eye)

            rotated = cv2.warpAffine(image, M, (width, height), flags=cv2.INTER_CUBIC)

            cropped = self.crop_image(rotated, det)
            cropped = cv2.resize(cropped, (128,128), interpolation=cv2.INTER_CUBIC)

            if only_one == True:
                if save_path is not None:
                    cv2.imwrite(save_path, cropped)
                return cropped
            else:
                crop_images.append(cropped)
        return crop_images

if __name__ == "__main__":
    align = Face_Align("./shape_predictor_68_face_landmarks.dat")
    #align(image_path="./CASIA-WebFAce/0000045/011.jpg",save_path="./WebFace-align128/test.jpg")
    root1 = "CASIA-WebFace"
    root2 = "WebFace-align128"
    data_list_file = "cleaned_list.txt"

    with open(data_list_file, 'r') as fd:
        imgs = fd.readlines()

    imgs1 = [os.path.join(root1, img[:-1]) for img in imgs]
    imgs2 = [os.path.join(root2, img[:-1]) for img in imgs]

    len = len(imgs)
    print(len)
    
    for i in range(441478, len):
        splits1 = imgs1[i].split()
        splits2 = imgs2[i].split()

        img_path = splits1[0]
        save = splits2[0]
        print(save)
        print(i)

        img = Image.open(img_path)
        img = img.convert('L')
        align(image_path=img_path, save_path=save)
    