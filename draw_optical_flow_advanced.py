import numpy as np
import cv2

from constants import *
from utilities import *

# average movement sensitivity
sensitivity = 2.5

class optical_flow_advanced_tracker:
    def __init__(self):
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.cam = cv2.VideoCapture(0)
        self.frame_index = 0
        self.arm = init_arm()

    def start(self):
        # main loop
        while True:
            _ret, frame = self.cam.read()

            # flipping the frame to see same side of yours
            frame = cv2.flip(frame, 1) 
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # copy to show lines on
            image_visuals_copy = frame.copy()

            # if there are tracking points
            if len(self.tracks) > 0:

                previous_image_gray, current_image_gray = self.previous_gray, frame_gray

                # collect previous points
                previous_points = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)

                # lucas-kanade to track points between images
                # the lucas-kanade parameters can be found under constants
                current_points, _st, _err = cv2.calcOpticalFlowPyrLK(previous_image_gray, current_image_gray, previous_points, None, **lk_params_advanced)

                # lucas-kanade reversed images - used for tracking lines
                previous_points_reversed, _st, _err = cv2.calcOpticalFlowPyrLK(current_image_gray, previous_image_gray, current_points, None, **lk_params_advanced)

                # calculate the distance traveled to check if tracked poits are close enough
                d = abs(previous_points - previous_points_reversed).reshape(-1, 2).max(-1)

                # calculate difference to test for movement
                average_moving_distance = (current_points - previous_points).reshape(-1, 2).mean(axis=0)[0]

                # moving condition
                check_movement(d=average_moving_distance, sensativity=sensitivity, arm=self.arm)
                
                # check if tracked points are close enough
                good = d < 1

                new_tracks = []
                for tr, (x, y), good_flag in zip(self.tracks, current_points.reshape(-1, 2), good):
                    if not good_flag:
                        continue
                    tr.append((x, y))
                    if len(tr) > self.track_len:
                        del tr[0]
                    new_tracks.append(tr)
                    cv2.circle(image_visuals_copy, (x, y), 2, (0, 255, 0), -1)

                self.tracks = new_tracks
                cv2.polylines(image_visuals_copy, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))

            # every interval number of frames
            if self.frame_index % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                # circle the collected points
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)
                
                # collect new points with goodFeaturesToTrack that uses Shi-Tomasi Corner Detector
                # that finds N strongest corners in the image
                # and adds these points to the track list
                points = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                if points is not None:
                    for x, y in np.float32(points).reshape(-1, 2):
                        self.tracks.append([(x, y)])

            # advance the frame counter
            self.frame_index += 1
            # save current frame as previous
            self.previous_gray = frame_gray
            cv2.imshow('lk_track', image_visuals_copy)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

def main():
    optical_flow_advanced_tracker().start()
    print('Done')


if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()