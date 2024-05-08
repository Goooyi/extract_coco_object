import numpy as np
import transforms3d as t3d
import math
np.set_printoptions(precision=20)

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

# print(cam_coord)


cam_coord2 = np.dot(np.linalg.inv(tovcs), target_point_in4D)
cam_coord2 = cam_coord2 / cam_coord2[3]
# print(cam_coord2)
x_cam = cam_coord2[0] * fx / cam_coord2[2] + cx
y_cam = cam_coord2[1] * fy / cam_coord2[2] + cy
# print(x_cam, y_cam)


def quaternion_to_euler_extrinsic(quaternion):
    quaternion /= np.linalg.norm(quaternion)
    # Extract quaternion components
    x, y, z, w = quaternion
    return [
        np.arctan2(2 * (w * x - y * z), 1 - 2 * (x**2 + y**2)),  # Roll
        np.arcsin(2 * (w * y + x * z)),                          # Pitch
        np.arctan2(2 * (w * z - x * y), 1 - 2 * (y**2 + z**2))
    ]

q1 = [-0.00014999992234911112,
    -0.0018139117031107758,
    -0.007070467312846158,
    0.9999733475029894]

q1_gt = [
               -0.3256444018265790,
               -0.0036256135197273464,
               -0.01414166620399113
        ]


print("-------------q1--------------")
print("一期数据的rotation2")
print(q1_gt)
print("从四元数计算得到的rotation2")
euler = quaternion_to_euler_extrinsic(q1)
print(euler)
q1 = [ 0.9999733475029894,
     -0.00014999992234911112,
    -0.0018139117031107758,
    -0.007070467312846158
    ]
print("t3d的库计算的")
print(t3d.euler.quat2euler(q1, 'syxz'))

q2 =  [
       -0.003199679618752578,
       -0.013315740447191688,
       -0.19708431541649887,
       0.9802908883201406
       ]
q2_euler_gt  = [
          -0.011525693748717423,
          -0.024847941586722468,
          -0.3969469343146715
          ]

print("-------------q2--------------")
print("一期数据的rotation2")
print(q2_euler_gt)
print("从四元数计算得到的rotation2")
euler = quaternion_to_euler_extrinsic(q2)
print(euler)

q3 =  [
       6.113293305949686e-17,
       6.113293305949687e-17,
       -0.9999986843589164,
       0.001622122201403005
       ]
q3_euler_gt  = [
          1.2246403543690254e-16,
          -1.2206737508509172e-16,
          -3.1383484077642327
          ]

print("-------------q3--------------")
print("一期数据的rotation2")
print(q3_euler_gt)
print("从四元数计算得到的rotation2")
euler = quaternion_to_euler_extrinsic(q3)
print(euler)


# print(t3d.quaternions.quat2mat(q3)[0])
q3 =  [
       0.001622122201403005,
       6.113293305949686e-17,
       6.113293305949687e-17,
       -0.9999986843589164
       ]
print("t3d的库计算的")
print(t3d.euler.quat2euler(q3, 'syxz'))