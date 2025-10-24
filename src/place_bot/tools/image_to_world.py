import random

# from cv2 import cv2 as cv2
import cv2
import numpy as np


class ImageToWorld:
    """
    Converts an image to a world representation by extracting walls, boxes.

    Attributes:
        _img_src (cv2.Mat): Source image.
        _img_src_walls (cv2.Mat): Binary image for wall detection.
        _auto_resized (bool): Whether to auto-resize the world.
        height_world (int): Height of the world.
        width_world (int): Width of the world.
        factor (float): Scaling factor from image to world.
        lines (np.ndarray): List of detected wall segments.
        boxes (list): List of detected boxes.
    """

    _img_src: cv2.Mat
    _img_src_walls: cv2.Mat
    _auto_resized: bool
    height_world: int
    width_world: int
    factor: float
    lines: np.ndarray
    boxes: List[Tuple[int, int, int, int]]

    def __init__(self, image_source: cv2.Mat, auto_resized: bool = True) -> None:
        """
        Initializes the ImageToWorld object.

        Args:
            image_source (cv2.Mat): The source image.
            auto_resized (bool): Whether to auto-resize the world.
        """
        self._img_src = image_source
        cv2.imshow("image_source", self._img_src)
        cv2.waitKey(0)

        img_hsv = cv2.cvtColor(self._img_src, cv2.COLOR_BGR2HSV)
        # lower bound and upper bound for all color except black
        lower_bound = (0, 0, 100)
        upper_bound = (180, 255, 255)
        # find the colors within the boundaries
        mask_walls = cv2.inRange(img_hsv, lower_bound, upper_bound)
        self._img_src_walls = cv2.bitwise_not(mask_walls)
        # cv2.imshow("mask_walls", self._img_src_bw)
        # cv2.waitKey(0)

        self._auto_resized = auto_resized

        self.height_world = 750
        self.width_world = 0
        self.factor = 1.0

        # To initialize lines as an empty NumPy array for detected line segments (typically shape (0, 1, 4) for lines with 4 coordinates)
        self.lines = np.empty((0, 1, 4), dtype=np.float32)
        self.boxes = []

    def launch(self) -> None:
        """
        Runs the full image-to-world conversion process.
        """
        self.compute_dim()
        self.img_to_segments()
        self.img_to_boxes()
        self.write_lines_and_boxes()

    def compute_dim(self) -> None:
        """
        Computes the dimensions and scaling factor for the world based on the source image.
        """
        self.height_world = 750

        print("original dim world : ({}, {})"
              .format(self._img_src_walls.shape[1],
                      self._img_src_walls.shape[0]))
        print("auto_resized = {}".format(self._auto_resized))

        self.factor = self.height_world / self._img_src_walls.shape[0]
        if not self._auto_resized:
            self.factor = 1.0
            self.height_world = self._img_src_walls.shape[0]
        self.width_world = int(round(self.factor * self._img_src_walls.shape[1]))
        print("Used dim world : ({}, {}) with factor {}"
              .format(self.width_world, self.height_world, self.factor))

        print("Code to add in world_xxx.py:")
        print("\tself._size_area = ({0:.0f},{1:.0f})"
              .format(self.width_world, self.height_world))

    def img_to_segments(self) -> None:
        """
        Detects wall segments in the image and aligns them.
        """
        fld = cv2.ximgproc.createFastLineDetector(canny_aperture_size=7,
                                                  do_merge=True)
        # size_kernel = 9
        # kernel = np.ones((size_kernel, size_kernel), np.uint8)
        radius_kernel = 4
        kernel = circular_kernel(radius_kernel)
        img_erode = cv2.erode(self._img_src_walls, kernel, iterations=1)
        cv2.imshow("img_erode", img_erode)

        self.lines = fld.detect(img_erode)
        lines_corrected = self.align_segments(self.lines)
        result_img = fld.drawSegments(self._img_src_walls, self.lines)
        cv2.imshow("result_img", result_img)

        only_lines_image = np.zeros((self._img_src_walls.shape[0],
                                     self._img_src_walls.shape[1], 3),
                                    dtype=np.uint8)

        for line in lines_corrected:
            x0 = int(round(line[0][0]))
            y0 = int(round(line[0][1]))
            x1 = int(round(line[0][2]))
            y1 = int(round(line[0][3]))
            cv2.line(only_lines_image, (x0, y0), (x1, y1),
                     (0, 255, 0), 1, cv2.LINE_4)

        for line in self.lines:
            x0 = int(round(line[0][0]))
            y0 = int(round(line[0][1]))
            x1 = int(round(line[0][2]))
            y1 = int(round(line[0][3]))
            cv2.line(only_lines_image, (x0, y0), (x1, y1),
                     (0, 0, 255), 1, cv2.LINE_4)

        # Compute min and max
        # for line in self.lines:
        #     x0 = int(round(line[0][0]))
        #     x1 = int(round(line[0][2]))
        #     self.x_max = max(x0, x1, self.x_max)
        #
        #     y0 = int(round(line[0][1]))
        #     y1 = int(round(line[0][3]))
        #     self.y_max = max(y0, y1, self.y_max)

        cv2.imshow("only_lines_image", only_lines_image)

        cv2.waitKey(0)

        self.lines = lines_corrected

    def align_segments(self, segments: np.ndarray, distance_threshold: int = 5, endpoint_threshold: int = 10) -> np.ndarray:
        """
        Aligns nearly identical horizontal and vertical segments.

        Args:
            segments (np.ndarray): List of segments to align.
            distance_threshold (int): Max pixel distance for alignment.
            endpoint_threshold (int): Max pixel distance for endpoints.

        Returns:
            np.ndarray: Aligned segments.
        """
        oriented_segments = []

        for segment in segments:
            x1, y1, x2, y2 = segment[0]

            if abs(y1 - y2) < abs(x1 - x2) and x1 > x2:  # horizontal
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            elif abs(y1 - y2) > abs(x1 - x2) and y1 > y2:  # vertical
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            oriented_segments.append([[x1, y1, x2, y2]])

        segments = oriented_segments
        aligned_segments = []

        for i in range(len(segments)):
            # print("segments[i]=",segments[i])
            segment = segments[i][0]
            # print("segment=", segment)
            x1, y1, x2, y2 = segment

            for j in range(len(segments)):

                if i == j:
                    continue

                other_segment = segments[j][0]
                ox1, oy1, ox2, oy2 = other_segment

                # Vérifie si les segments sont horizontaux et presque identiques
                if abs(y1 - y2) <= 2 and abs(y1 - oy1) <= distance_threshold and abs(y2 - oy2) <= distance_threshold:
                    if abs(x1 - ox1) <= endpoint_threshold:
                        x1 = min(x1, ox1)  # (x1 + ox1) // 2
                    if abs(x2 - ox2) <= endpoint_threshold:
                        x2 = max(x2, ox2)  # ((x2 + ox2) // 2

                # Vérifie si les segments sont verticaux et presque identiques
                elif abs(x1 - x2) <= 2 and abs(x1 - ox1) <= distance_threshold and abs(x2 - ox2) <= distance_threshold:
                    if abs(y1 - oy1) <= endpoint_threshold:
                        y1 = min(y1, oy1)  # ((y1 + oy1) // 2
                    if abs(y2 - oy2) <= endpoint_threshold:
                        y2 = max(y2, oy2)  # (y2 + oy2) // 2

            aligned_segments.append([[x1, y1, x2, y2]])

        return np.array(aligned_segments)

    def img_to_boxes(self) -> None:
        """
        Detects rectangular boxes in the image and stores their coordinates.
        """
        size_kernel = 50
        kernel = np.ones((size_kernel, size_kernel), np.uint8)
        img_box = cv2.morphologyEx(self._img_src_walls, cv2.MORPH_OPEN, kernel)
        cv2.imshow("img_box", img_box)
        thresh_value, thresh_img = cv2.threshold(src=img_box, thresh=127,
                                                 maxval=255, type=0)
        contours, hierarchy = cv2.findContours(image=thresh_img,
                                               mode=cv2.RETR_LIST,
                                               method=cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow("thresh_img_box", thresh_img)

        contours_poly = []
        self.boxes = []

        for i, curve in enumerate(contours):
            perimeter = cv2.arcLength(curve=curve, closed=True)
            approx_poly = cv2.approxPolyDP(curve=curve,
                                           epsilon=0.015 * perimeter,
                                           closed=True)
            box = cv2.boundingRect(approx_poly)
            # print("approx_poly.shape[0]", approx_poly.shape[0])
            # print("abs(cv2.contourArea(approx_poly))",
            # abs(cv2.contourArea(approx_poly)))
            # print("cv2.isContourConvex(approx_poly)",
            # cv2.isContourConvex(approx_poly))

            # remove huge boxes
            # if box[2] > 0.7 * self._img_src.shape[1] and
            #    box[3] > 0.7 * self._img_src.shape[0]:
            # print("**********")
            # print("width box", box[2])
            # print("height box", box[3])
            # print("width img", self._img_src.shape[1])
            # print("height img", self._img_src.shape[0])
            # print("")
            # continue

            if (approx_poly.shape[0] == 4 and
                    abs(cv2.contourArea(approx_poly)) > 300 and
                    cv2.isContourConvex(approx_poly)):
                # print("approx_poly", approx_poly)
                contours_poly.append(approx_poly)
                self.boxes.append(box)
                # print("box", box)

        only_boxes_image = np.zeros((thresh_img.shape[0],
                                     thresh_img.shape[1], 3),
                                    dtype=np.uint8)

        for i in range(len(contours_poly)):
            color = (random.randint(0, 256),
                     random.randint(0, 256),
                     random.randint(0, 256))
            cv2.drawContours(only_boxes_image, contours_poly, i, color)
            # x, y, w, h = self.boxes[i]
            # cv2.rectangle(img=only_boxes_image, pt1=(x, y),
            #               pt2=(x + w, y + h),
            # color=color, thickness=-1)

        # Compute min and max
        # for box in self.boxes:
        #     x0 = int(round(box[0]))
        #     x1 = int(round(box[0] + box[2]))
        #     self.x_max = max(x0, x1, self.x_max)
        #
        #     y0 = int(round(box[1]))
        #     y1 = int(round(box[1] + box[3]))
        #     self.y_max = max(y0, y1, self.y_max)

        cv2.imshow("only_boxes_image", only_boxes_image)

        cv2.waitKey(0)

    def write_lines_and_boxes(self) -> None:
        """
        Writes the detected lines and boxes as Python code to a file.
        """
        f = open("generated_code.py", "w")

        f.write("\"\"\"\n")
        f.write("This file was generated by the tool 'image_to_world.py' in "
                "the directory tools.\n")
        f.write(
            "This tool permits to create this kind of file by providing it "
            "an image of the\n")
        f.write(
            "world we want to create.\n")
        f.write("\"\"\"\n")

        f.write("import sys\n")
        f.write("import pathlib\n\n")

        f.write("# Insert the parent directory of the current file's directory into sys.path.\n")
        f.write("# This allows Python to locate modules that are one level above the current\n")
        f.write("# script, in this case simulation.\n")
        f.write("sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))\n\n")

        f.write("from place_bot.simulation.elements.normal_wall import NormalWall, "
                "NormalBox\n\n\n")

        f.write("# Dimension of the world : ({}, {})\n"
                .format(self.width_world,
                        self.height_world))

        f.write("# Dimension factor : {}\n".format(self.factor))

        f.write("def add_boxes(playground):\n")

        if len(self.boxes) != 0:
            for i, box in enumerate(self.boxes):
                x0 = self.factor * box[0]
                y0 = self.factor * box[1]
                width = self.factor * box[2]
                height = self.factor * box[3]

                xw = int(round(x0 - self.width_world / 2))
                yw = int(round(-y0 + self.height_world / 2))
                width_w = int(round(width))
                height_w = int(round(height))

                f.write("    # box {}\n".format(i))
                f.write("    box = NormalBox(up_left_point=({}, {}),\n"
                        .format(xw, yw))
                f.write("                    width={}, height={})\n"
                        .format(width_w, height_w))
                f.write("    playground.add(box, box.wall_coordinates)\n\n")
        else:
            f.write("    pass\n\n")

        f.write("\n")
        f.write("def add_walls(playground):\n")

        # orient :
        #   horizontal = 0
        #   vertical = 1
        #   oblique = 2
        if len(self.lines) != 0:
            for i, line in enumerate(self.lines):
                x0 = self.factor * line[0][0]
                y0 = self.factor * line[0][1]
                x1 = self.factor * line[0][2]
                y1 = self.factor * line[0][3]

                orient = 2

                if abs(y0 - y1) < 2.0:
                    # horizontal
                    orient = 0
                    y0 = (y0 + y1) / 2
                    y1 = y0

                if abs(x0 - x1) < 2.0:
                    # vertical
                    orient = 1
                    x0 = (x0 + x1) / 2
                    x1 = x0

                # Correct orientation
                if orient == 0 and x0 > x1:  # horizontal
                    x0, x1 = x1, x0  # swap

                if orient == 1 and y0 > y1:  # vertical
                    y0, y1 = y1, y0  # swap

                if orient == 2 and x0 > x1:  # oblique
                    x0, x1 = x1, x0  # swap
                    y0, y1 = y1, y0  # swap

                # Correct size
                correction = 4
                if orient == 0:  # horizontal
                    x0 -= correction
                    x1 += correction

                if orient == 1:  # vertical
                    y0 -= correction
                    y1 += correction

                if orient == 2:  # oblique
                    x0 -= correction
                    x1 += correction
                    if y1 > y0:  # oblique
                        y0 -= correction
                        y1 += correction
                    else:
                        y1 -= correction
                        y0 += correction

                if orient == 0:
                    f.write("    # horizontal wall {}\n".format(i))
                elif orient == 1:
                    f.write("    # vertical wall {}\n".format(i))
                else:
                    f.write("    # oblique wall {}\n".format(i))

                xw0 = int(round(x0 - self.width_world / 2))
                yw0 = int(round(-y0 + self.height_world / 2))

                xw1 = int(round(x1 - self.width_world / 2))
                yw1 = int(round(-y1 + self.height_world / 2))

                f.write("    wall = NormalWall(pos_start=({}, {}),\n"
                        .format(xw0, yw0))
                f.write("                      pos_end=({}, {}))\n"
                        .format(xw1, yw1))
                f.write("    playground.add(wall, wall.wall_coordinates)\n\n")
        else:
            f.write("    pass\n\n")

        f.close()

        print("nombre de boxes =", len(self.boxes))
        print("nombre de lignes =", len(self.lines))

def main():
    # img_path = "/home/battesti/projetRobotMobile/place-bot/world_data/complete_world_1.png"
    img_path = "/world_data/intermediate_eval_1.png"
    should_auto_resized = False
    # img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.imread(img_path)
    image_to_world = ImageToWorld(image_source=img, auto_resized=should_auto_resized)
    image_to_world.launch()

if __name__ == '__main__':
    main()