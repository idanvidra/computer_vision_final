from draw_tracking import *
from draw_optical_flow import *
from draw_optical_flow_advanced import *


class Running_Mode:

    def __init__(self):
        a = 5

    def start(self,running_type):
        if running_type == "optical flow":
            dop = optical_flow_tracker()
            dop.start()
        elif running_type == "tracking":
            dt = draw_tracker()
            dt.start()
        elif running_type == "optical flow advanced":
            dopa = optical_flow_advanced_tracker()
            dopa.start()
        else:
            print("please enter running mode: optical flow or tracking")
