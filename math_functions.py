import math


def get_euclidean_distance(p1, p2):
    return math.dist(p1, p2)

def get_angle(p1,p2, p3):
    delta_y1 = p1[1] - p2[1]
    delta_x1 = p1[0] - p2[0]
    delta_y2 = p3[1] - p2[1]
    delta_x2 = p3[0] - p2[0]
    
    angle1 = math.degrees(math.atan2(delta_y1, delta_x1))
    angle2 = math.degrees(math.atan2(delta_y2, delta_x2))
    
    angle = angle2 - angle1

    if angle > 180:
        angle = 360 - angle
        
    return angle