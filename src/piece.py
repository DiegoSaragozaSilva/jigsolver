import cv2
import random
import numpy as np
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters

from itertools import combinations
from matplotlib import pyplot as plt

from side import Side
from utils import SideType, PieceType


class Piece:

    def __init__(self, image, original_image, contour):
        self.image = image
        self.original_image = original_image
        self.contour = contour
        self.sides = []

        M = cv2.moments(self.contour)
        self.center = [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])]

    def classify(self):
        def clockwise_distance(point):
            vector = [point[0] - self.center[0], point[1] - self.center[1]]
            vector_length = np.linalg.norm(vector)

            if np.isclose(vector_length, 0.0):
                return -np.pi, 0

            vector_normalized = vector / vector_length
            vector_dot = np.dot(vector_normalized, [0, 1])
            vector_diff = vector_normalized[0]
            angle = np.arctan2(vector_diff, vector_dot)

            if angle < 0:
                return 2.0 * np.pi + angle, vector_length

            return angle, vector_length

        def point_distance(a, b):
            return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

        def point_line_distance(p, line):
            return abs(
                (line[1][0] - line[0][0]) * (p[1] - line[0][1])
                - (p[0] - line[0][0]) * (line[1][1] - line[0][1])
            ) / np.sqrt((line[1][0] - line[0][0]) ** 2 + (line[1][1] - line[0][1]) ** 2)

        def point_line_side(p, line):
            return np.sign(
                np.cross(
                    [line[1][0] - line[0][0], line[1][1] - line[0][1], 0],
                    [p[0] - line[0][0], p[1] - line[0][1], 0],
                )[2]
            )

        def point_inside_window(point, window):
            return (point[0] >= window[0][0] and point[0] <= window[1][0]) and (
                point[1] <= window[0][1] and point[1] >= window[1][1]
            )

        def polygon_distance_threshold(polygon, threshold):
            for combination in combinations(polygon, 2):
                if point_distance(combination[0], combination[1]) < threshold:
                    return False
            return True

        def polygon_distances(polygon):
            distances = []
            for combination in combinations(polygon, 2):
                distances.append(point_distance(combination[0], combination[1]))
            return distances

        def polygon_area(points):
            return (
                points[0][0] * points[1][1]
                - points[0][1] * points[1][0]
                + points[1][0] * points[2][1]
                - points[1][1] * points[2][0]
                + points[2][0] * points[3][1]
                - points[2][1] * points[3][0]
            ) / 2.0

        image_harris = cv2.cornerHarris(self.image, 4, 3, 0.005)

        image_corners = image_harris.copy()
        image_corners[image_corners < 0.3 * image_harris.max()] = 0.0
        corners_max = filters.maximum_filter(image_corners, 3)
        corners_maxima = image_corners == corners_max
        corners_min = filters.minimum_filter(image_corners, 3)
        corners_diff = (corners_max - corners_min) > 0.0
        corners_maxima[corners_diff == 0] = 0.0

        labeled, num_objects = ndimage.label(corners_maxima)
        slices = ndimage.find_objects(labeled)
        points = np.array(
            ndimage.center_of_mass(image_corners, labeled, range(1, num_objects + 1))
        )
        points = [list(reversed(point)) for point in points]
        points_x = [point[0] for point in points]
        points_y = [point[1] for point in points]

        candidates = []
        delta_distances = []
        distance_threshold = 50
        for combination in combinations(points, 4):
            if not polygon_distance_threshold(combination, distance_threshold):
                continue

            # center_of_mass = [(combination[0][0] + combination[1][0] + combination[2][0] + combination[3][0]) / 4,
            #                   (combination[0][1] + combination[1][1] + combination[2][1] + combination[3][1]) / 4]

            # ac_distance = point_distance(combination[0], center_of_mass)
            # bc_distance = point_distance(combination[1], center_of_mass)
            # cc_distance = point_distance(combination[2], center_of_mass)
            # dc_distance = point_distance(combination[3], center_of_mass)
            # delta = abs((ac_distance + cc_distance) - (bc_distance + dc_distance))
            # candidates.append(combination)
            # delta_distances.append(delta)
            slope_ab = (combination[1][1] - combination[0][1]) / (
                combination[1][0] - combination[0][0]
            )
            slope_cd = (combination[3][1] - combination[2][1]) / (
                combination[3][0] - combination[2][0]
            )
            slope_ac = (combination[2][1] - combination[0][1]) / (
                combination[2][0] - combination[0][0]
            )
            slope_bd = (combination[3][1] - combination[1][1]) / (
                combination[3][0] - combination[1][0]
            )
            delta_slope = abs((slope_ab + slope_cd) - (slope_ac + slope_bd))
            if np.isclose(delta_slope, 0, atol=0.3):
                candidates.append(combination)

        figure = plt.figure(figsize=(12, 4))
        figure.add_subplot(3, 3, 1)
        plt.imshow(self.image)
        figure.add_subplot(3, 3, 2)
        plt.imshow(image_harris)
        figure.add_subplot(3, 3, 3)
        plt.imshow(corners_maxima)
        figure.add_subplot(3, 3, 4)
        plt.imshow(self.image)
        plt.scatter(points_x, points_y)

        print(f"Found candidates {len(candidates)}")
        if len(candidates) <= 0:
            return 0

        sorted_candidates = sorted(candidates, key=polygon_area)
        best_candidate = list(sorted_candidates[0])
        # best_candidate_index = np.argmin(delta_distances)
        # best_candidate = candidates[best_candidate_index]

        best_xs = [point[0] for point in best_candidate]
        best_ys = [point[1] for point in best_candidate]

        figure.add_subplot(3, 3, 5)
        plt.imshow(self.image)
        plt.scatter(best_xs, best_ys)

        # Refine detected corners
        refinement_size = 20
        refined_corners = []
        for point in best_candidate:
            farthest_distance = 0
            farthest_point = [0, 0]
            point_window = [
                [point[0] - refinement_size, point[1] + refinement_size],
                [point[0] + refinement_size, point[1] - refinement_size],
            ]
            for i in range(len(self.contour)):
                contour_point = self.contour[i][0]
                if point_inside_window(contour_point, point_window):
                    contour_point_distance = point_distance(self.center, contour_point)
                    if contour_point_distance > farthest_distance:
                        farthest_distance = contour_point_distance
                        farthest_point = contour_point
            refined_corners.append(farthest_point)

        # Sort corner points
        refined_corners = list(sorted(refined_corners, key=clockwise_distance))
        self.corners = refined_corners

        refined_xs = [point[0] for point in refined_corners]
        refined_ys = [point[1] for point in refined_corners]

        figure.add_subplot(3, 3, 6)
        plt.imshow(self.image)
        plt.scatter(refined_xs, refined_ys)

        # Separate the four sides of the piece
        side_lines = [
            [self.corners[0], self.corners[1]],
            [self.corners[1], self.corners[2]],
            [self.corners[2], self.corners[3]],
            [self.corners[3], self.corners[0]],
        ]

        distance_threshold = 100
        unclassified_points = []
        side_points = [[], [], [], []]
        for i in range(len(self.contour)):
            closest_side = -1
            closest_distance = np.inf
            contour_point = self.contour[i][0]
            for j in range(len(side_lines)):
                side_line = side_lines[j]
                side_distance = point_line_distance(contour_point, side_line)
                if (
                    side_distance < distance_threshold
                    and side_distance < closest_distance
                ):
                    closest_side = j
                    closest_distance = side_distance
            if closest_side > -1:
                side_points[closest_side].append(contour_point)
            else:
                unclassified_points.append(contour_point)

        image_lines = self.image.copy()
        image_lines = cv2.cvtColor(image_lines, cv2.COLOR_GRAY2BGR)
        for side in side_points:
            random_color = [
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ]
            cv2.polylines(
                image_lines,
                np.int32([side]),
                isClosed=False,
                color=random_color,
                thickness=3,
            )
        cv2.circle(image_lines, self.center, 3, (255, 0, 0), -1)

        num_flats = 0
        patch_size = 5
        for side in side_points:
            if len(side) == 0:
                continue

            average_point = np.array(side).mean(axis=0)
            average_point = [int(x) for x in average_point]
            average_point_patch = self.image[
                average_point[1] - patch_size : average_point[1] + patch_size,
                average_point[0] - patch_size : average_point[0] + patch_size,
            ]

            non_zero = cv2.countNonZero(average_point_patch)
            if non_zero == 2 * patch_size * 2 * patch_size:
                self.sides.append(Side(np.array(side), SideType.HEAD))
                print(f"HEAD (R) {non_zero}")
                cv2.circle(image_lines, average_point, 3, (255, 0, 0), -1)
            elif non_zero == 0:
                self.sides.append(Side(np.array(side), SideType.HOLE))
                print(f"HOLE (G) {non_zero}")
                cv2.circle(image_lines, average_point, 3, (0, 255, 0), -1)
            else:
                self.sides.append(Side(np.array(side), SideType.FLAT))
                num_flats += 1
                print(f"FLAT (B) {non_zero}")
                cv2.circle(image_lines, average_point, 3, (0, 0, 255), -1)

        figure.add_subplot(3, 3, 7)
        plt.imshow(image_lines)

        if num_flats == 2:
            self.type = PieceType.CORNER
        elif num_flats == 1:
            self.type = PieceType.BORDER
        else:
            self.type = PieceType.CENTER
        plt.show()

    def visualize(self):
        stack_image = np.vstack(
            (cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR), self.original_image)
        )
        cv2.imshow("Jigsaw Piece", stack_image)
        while True:
            key = cv2.waitKey(33)
            if key == 27:
                break
        cv2.destroyAllWindows()
