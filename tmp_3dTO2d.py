import numpy as np

# FRONT camera
fx =  1013.13099958178
fy =  1019.58415956928
cx =  960.199484519181
cy =  618.011509455934

tovcs = np.array([
          [ 0.00341074, -0.0025734 ,  0.99999087,  1.58227253],
          [-0.99997779,  0.00571747,  0.00342541, -0.01706382],
          [-0.00572624, -0.99998034, -0.00255384,  1.40295039],
          [ 0.        ,  0.        ,  0.        ,  1.        ],
      ])

tovcs_rotation = tovcs[:3,:3]
tovcs_translation = tovcs[:3,3]

target_point_in3D = np.array([96.1144194724502, 3.9740228668449085, 0.9641461158157686])
target_point_in4D = np.array([96.1144194724502, 3.9740228668449085, 0.9641461158157686, 1])

cam_coord = np.dot(np.linalg.inv(np.array(tovcs_rotation)),
                   target_point_in3D - tovcs_translation)

print(cam_coord)


cam_coord2 = np.dot(np.linalg.inv(tovcs), target_point_in4D)
cam_coord2 = cam_coord2 / cam_coord2[3]
print(cam_coord2)
x_cam = cam_coord2[0] * fx / cam_coord2[2] + cx
y_cam = cam_coord2[1] * fy / cam_coord2[2] + cy
print(x_cam, y_cam)