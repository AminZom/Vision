"""
Dataset creator pipeline

"""
################### Next to do items #######################
# dynamic color on generate_outline method
# review hard and easy cases

from PIL import Image, ImageDraw, ImageOps
from random import randint
from math import sqrt


class CircleGen:
    def __init__(self, width, height, count_light, count_dark, path_to_directory):
        self.width = width
        self.height = height
        self.image_count_light = count_light
        self.image_count_dark = count_dark
        self.path_to_directory = path_to_directory
        self.current_file_count = 1
        self.background_dark = [(44, 41, 6), (41, 24, 52), (21, 39, 60), (52, 0, 27), (39, 56, 50), (62, 37, 34),
                                (58, 13, 61), (62, 5, 41), (23, 20, 33), (20, 25, 50)]
        self.background_light = [(187, 180, 233), (190, 179, 152), (244, 157, 158), (167, 191, 186), (162, 208, 255),
                                 (198, 208, 195), (212, 194, 163), (223, 152, 167), (243, 186, 199), (241, 241, 242)]

    def num_object(self):
        # number of creating objects/circles in an image
        return randint(7, 15)

    def create_image_with_background(self, background_color):
        self.index = randint(0, 9)
        color = None
        if background_color == "dark":
            color = self.background_dark[self.index]
        elif background_color == "light":
            color = self.background_light[self.index]

        image = Image.new('RGBA', (self.width, self.height), color)
        return image

    def save_img(self, image, case):
        image.save(f'{self.path_to_directory}/images/circles_dataset_{self.current_file_count}_{case}.png')

    def save_annotation(self, data, case):
        # save center (x, y), radius
        [x, y, r] = data
        UL = (x-r, y-r)
        UR = (x+r, y-r)
        LR = (x+r, y+r)
        LL = (x-r, y+r)
        with open(f'{self.path_to_directory}/annotations/annotations_{self.current_file_count}_{case}.txt',
                  "a") as annotations:
            # line = str(x) + ", " + str(y) + ", " + str(r) + ", " + \
            #        str(UL) + ", " + str(UR) + ", " + str(LR) + ", " + str(LL) + "\n"
            line = str(UL) + ", " + str(UR) + ", " + str(LR) + ", " + str(LL) + "\n"
            annotations.write(line)
        annotations.close()

    def circle_radius_set(self):
        max_radius = int(self.width / 40)
        if max_radius <= 5:
            return 5
        return randint(5, max_radius)

    def random_center_position_and_radius(self, margin):
        margin = int(margin)
        x = randint(margin, self.width - margin)
        y = randint(margin, self.height - margin)
        r = self.circle_radius_set()
        return [x, y, r]

    def draw_random_circles(self, case):
        # circle size change, numbers, contrast, then save_img, then save_annotation
        circles_created = []
        for i in range(self.image_count_light):
            # print("inside light, i = " + str(i))
            new_image = self.create_image_with_background("light")
            draw = ImageDraw.Draw(new_image)
            for y in range(self.num_object()):
                # print("inside for in light, y = " + str(y))
                while True:
                    [x, y, r] = self.random_center_position_and_radius(25)
                    if (len(circles_created) == 0 or not (
                            self.is_intersecting_some_circle_or_boundary(circles_created, [x, y, r]))):
                        draw.ellipse((x - r, y - r, x + r, y + r),
                                     fill=self.generate_fill(self.get_fill("light", case)),
                                     width=self.generate_width(r))
                        circles_created.append([x, y, r])
                        self.save_annotation([x, y, r], case)
                        break
            for z in range(3):
                self.create_moon_shaped_circles(new_image, circles_created, "light", case)

            new_image = ImageOps.grayscale(new_image)
            self.save_img(new_image, case)
            self.current_file_count = self.current_file_count + 1
        for i in range(self.image_count_dark):
            # print("inside dark, i = " + str(i))
            new_image = self.create_image_with_background("dark")
            draw = ImageDraw.Draw(new_image)
            for y in range(self.num_object()):
                # print("inside for in dark, y = " + str(y))
                while True:
                    [x, y, r] = self.random_center_position_and_radius(25)
                    if (len(circles_created) == 0 or not (
                            self.is_intersecting_some_circle_or_boundary(circles_created, [x, y, r]))):
                        draw.ellipse((x - r, y - r, x + r, y + r), fill=self.generate_fill(self.get_fill("dark", case)),
                                     width=self.generate_width(r))
                        circles_created.append([x, y, r])
                        self.save_annotation([x, y, r], case)
                        break
            for z in range(3):
                new_image = self.create_moon_shaped_circles(new_image, circles_created, "dark", case)
            new_image = ImageOps.grayscale(new_image)
            self.save_img(new_image, case)
            self.current_file_count = self.current_file_count + 1

    def is_intersecting_some_circle_or_boundary(self, array_of_circles, new_circle):
        for circle in array_of_circles:
            if (self.are_two_circles_intersecting(new_circle, circle) or
                    self.is_intersecting_boundary(new_circle)):
                return True
        return False

    def are_two_circles_intersecting(self, new_circle, circle):
        [new_x, new_y, new_r] = new_circle
        [x, y, r] = circle

        dist_between_centers = sqrt(((new_x - x) ** 2) + ((new_y - y) ** 2))

        return dist_between_centers <= (new_r + r)

    def is_intersecting_boundary(self, new_circle):
        [new_x, new_y, new_r] = new_circle

        return ((new_x + new_r >= self.width) or (new_x - new_r <= 0) or
                (new_y + new_r >= self.height) or (new_y - new_r <= 0))

    def generate_fill(self, contrast):
        if contrast == "dark":
            while True:
                idx = randint(0, 9)
                if idx != self.index:
                    color_fill = self.background_dark[idx]
                    break
        elif contrast == "light":
            while True:
                idx = randint(0, 9)
                if idx != self.index:
                    color_fill = self.background_light[idx]
                    break

        return color_fill

    def generate_width(self, radius):
        # less than 25% of the radius
        return randint(1, int(radius / 4)) if int(radius / 4) >= 1 else 1

    def generate_outline(self):
        # fill outline of the circle with darker/lighter color WRT background and foreground
        return None

    def get_fill(self, bgcolor, case):
        if bgcolor == "light":
            if case == "easy":
                return "dark"
            elif case == "hard":
                return "light"
        elif bgcolor == "dark":
            if case == "easy":
                return "light"
            elif case == "hard":
                return "dark"

    def create_moon_shaped_circles(self, image, circles_array, background_color, case):
        start = randint(0, 360)
        end = start + 150
        fill = "white"
        if background_color == "dark":
            fill = "black"

        draw = ImageDraw.Draw(image)
        while True:
            [x, y, r] = self.random_center_position_and_radius(25)
            if (len(circles_array) == 0 or not (
                    self.is_intersecting_some_circle_or_boundary(circles_array, [x, y, r]))):
                draw.ellipse((x - r, y - r, x + r, y + r),
                             fill=self.generate_fill(self.get_fill(background_color, case)),
                             width=self.generate_width(r))
                draw.chord((x - r, y - r, x + r, y + r), start, end, fill)
                circles_array.append([x, y, r])
                self.save_annotation([x, y, r], case)
                break
        return image


# main start of application for image generation
circle_files = CircleGen(600, 400, 1, 1, r"C:\Users\Sophia\Documents\GitHub\Vision\Apps\database\dataset\test")
circle_files.draw_random_circles("hard")
circle_files.draw_random_circles("easy")
