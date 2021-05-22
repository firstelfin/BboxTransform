#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : elfin
# @Time     : 2021/5/22 15:07
# @File     : BboxRotate.py
# @Project  : BboxTransform

import math
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv


class Rotate(object):
    """
    Rotate Bbox
    args:
        points: Vertices of a polygon
        center_point: the center of rotation
        theta: Angle of rotation
    """

    def __init__(self, points, center_point=(0, 0), theta=0):
        assert -1 <= theta <= 1, "excepted theta in [-1, 1]."
        self.theta = -theta * math.pi
        self.points = points
        self.center_point = center_point
        self.relative_coor = []
        self.get_relative_coord(points, center_point)
        self.rotated_points = np.array([])

    def get_relative_coord(self, points, center_point):
        self.relative_coor = []
        for point in points:
            self.relative_coor.append(
                [point[0] - center_point[0], point[1] - center_point[1]]
            )
        pass

    @staticmethod
    def elfin_round(num):
        symbol = 1 if num > 0 else -1
        number = abs(num)
        if number - int(number) < 0.5:
            return int(number) * symbol
        else:
            return (int(number) + 1) * symbol
        pass

    def handle_point(self, w, h):
        delta_x = self.elfin_round(
            w * math.cos(self.theta) - h * math.sin(self.theta)
        )
        delta_y = self.elfin_round(
            w * math.sin(self.theta) + h * math.cos(self.theta)
        )
        return delta_x, delta_y

    def rotate_bbox(self):
        res_points = []
        for coordinates in self.relative_coor:
            res_x, res_y = self.handle_point(*coordinates)
            res_points.append([
                res_x + self.center_point[0],
                res_y + self.center_point[1]
            ])
        self.rotated_points = np.array(res_points)
        return self.rotated_points

    def rotate_again(self, theta):
        assert -1 <= theta <= 1, "excepted theta in [-1, 1]."
        self.theta = -theta * math.pi
        self.get_relative_coord(self.rotated_points, center_point)
        return self.rotate_bbox()


def show(bbox, color=(255, 0, 0), img=None):
    if img is None:
        img = np.zeros((400, 400, 3))
    img = cv.polylines(img, [bbox], True, color)
    cv.imshow("rotate img", img)
    cv.waitKey(-1)
    return img


if __name__ == '__main__':
    test_points = [
        [150, 180],
        [150, 220],
        [250, 220],
        [250, 180]
    ]
    center_point = [200, 200]
    rotate = Rotate(test_points, center_point, 0.25)
    img2 = show(np.array(rotate.points))
    new_points = rotate.rotate_bbox()
    img2 = show(new_points, (0, 255, 0), img=img2)
    new_points = rotate.rotate_again(0.75)
    img2 = show(new_points, (0, 0, 255), img=img2)
