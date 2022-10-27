import time
import numpy as np
import sim
from sympy import symbols, cos, sin, pi, simplify, pprint, tan, expand_trig, sqrt, trigsimp, atan2
from sympy.matrices import Matrix


#Simulation Code *********************************************************************
 # The following code for Inverse Kinematics has been sourced from https://github.com/zahid58/Inverse-Kinematics-6-DOF-for-ERC-2019/blob/master/invKin.py 
 # However this code has been modified to be used for the used for simulations
 # As our Tesk for this Project was the Pose Estimation. This inverse Kinematics is not a part of the project it is used for Simulating Purposed only.
 # If The client wished to use this code for inverse kinematics for the real robot it has to be requested.


#Pose **************************************************************************************************************

def pose(theta, alpha, a, d):
    # returns the pose T of one joint frame i with respect to the previous joint frame (i - 1)
    # given the parameters:
    # theta: theta[i]
    # alpha: alpha[i-1]
    # a: a[i-1]
    # d: d[i]         

    r11, r12 = cos(theta), -sin(theta)
    r23, r33 = -sin(alpha), cos(alpha)
    r21 = sin(theta) * cos(alpha)
    r22 = cos(theta) * cos(alpha)
    r31 = sin(theta) * sin(alpha)
    r32 = cos(theta) * sin(alpha)
    y = -d * sin(alpha)
    z = d * cos(alpha)

    T = Matrix([
        [r11, r12, 0.0, a],
        [r21, r22, r23, y],
        [r31, r32, r33, z],
        [0.0, 0.0, 0.0, 1]
        ])

    T = simplify(T)

    return T

def eulerAnglesToRotationMatrix(theta) :
     
    R_x = np.array([[1,         0,                  0                   ],
                    [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                    [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                    ])
         
         
                     
    R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                    [0,                     1,      0                   ],
                    [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                    ])
                 
    R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                    [math.sin(theta[2]),    math.cos(theta[2]),     0],
                    [0,                     0,                      1]
                    ])
                     
                     
    R = np.dot(R_z, np.dot( R_y, R_x ))

    return R


    # Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

    # Calculates rotation matrix to euler angles
    # The result is the same as MATLAB except the order
    # of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R) :

    assert(isRotationMatrix(R))
     
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
     
    singular = sy < 1e-6

    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0

    return np.array([x, y, z])
    #---------------------------------------


def get_hypotenuse(a, b):
      # calculate the longest side given the two shorter sides 
      # of a right triangle using pythagorean theorem
      return sqrt(a*a + b*b)


def get_cosine_law_angle(a, b, c):    
    # given all sides of a triangle a, b, c
    # calculate angle gamma between sides a and b using cosine law
    cos_gamma = (a*a + b*b - c*c) / (2*a*b)
    sin_gamma = sqrt(1 - cos_gamma * cos_gamma)
    gamma = atan2(sin_gamma, cos_gamma)

    return gamma


def get_wrist_center(gripper_point, R0g, dg = 0.303):
    # get the coordinates of the wrist center wrt to the base frame (xw, yw, zw)
    # given the following info:
    # the coordinates of the gripper (end effector) (x, y, z)
    # the rotation of the gripper in gripper frame wrt to the base frame (R0u)
    # the distance between gripper and wrist center dg which is along common z axis
    # check WRITEUP.pdf for more info
    xu, yu, zu = gripper_point 

    nx, ny, nz = R0g[0, 2], R0g[1, 2], R0g[2, 2]
    xw = xu - dg * nx
    yw = yu - dg * ny
    zw = zu - dg * nz 

    return xw, yw, zw


def get_first_three_angles(wrist_center):
    # given the wrist center which a tuple of 3 numbers x, y, z
    # (x, y, z) is the wrist center point wrt base frame
    # return the angles q1, q2, q3 for each respective joint
    # given geometry of the kuka kr210
    # check WRITEUP.pdf for more info
    x, y, z  = wrist_center

    a1, a2, a3 = 0.35, 1.25, -0.054
    d1, d4 = 0.75, 1.5
    l = 1.50097168527591 # get_hypotenuse(d4, abs(a3))
    phi = 1.53481186671284 # atan2(d4, abs(a3))

    x_prime = get_hypotenuse(x, y)
    mx = x_prime -  a1
    my = z - d1 
    m = get_hypotenuse(mx, my)
    alpha = atan2(my, mx)

    gamma = get_cosine_law_angle(l, a2, m)
    beta = get_cosine_law_angle(m, a2, l)

    q1 = atan2(y, x)
    q2 = pi/2 - beta - alpha 
    q3 = -(gamma - phi)

    return q1, q2, q3 


def get_last_three_angles(R):
    #Recall that from our simplification, R36 (R) equals the following:
    #Matrix([
    #[-sin(q4)*sin(q6) + cos(q4)*cos(q5)*cos(q6), -sin(q4)*cos(q6) - sin(q6)*cos(q4)*cos(q5), -sin(q5)*cos(q4)],
    #[                           sin(q5)*cos(q6),                           -sin(q5)*sin(q6),          cos(q5)],
    #[-sin(q4)*cos(q5)*cos(q6) - sin(q6)*cos(q4),  sin(q4)*sin(q6)*cos(q5) - cos(q4)*cos(q6),  sin(q4)*sin(q5)]])
    #From trigonometry we can get q4, q5, q6 if we know numerical values of all cells of matrix R36 (R)
    #check WRITEUP.pdf for more info    
    sin_q4 = R[2, 2]
    cos_q4 =  -R[0, 2]

    sin_q5 = sqrt(R[0, 2]**2 + R[2, 2]**2) 
    cos_q5 = R[1, 2]

    sin_q6 = -R[1, 1]
    cos_q6 = R[1, 0] 

    q4 = atan2(sin_q4, cos_q4)
    q5 = atan2(sin_q5, cos_q5)
    q6 = atan2(sin_q6, cos_q6)

    return q4, q5, q6


def get_angles(x, y, z, roll, pitch, yaw):
    # input: given position and orientation of the gripper_URDF wrt base frame
    # output: angles q1, q2, q3, q4, q5, q6
    joint = []
    

    gripper_point = x, y, z
    q1, q2, q3, q4, q5, q6 = symbols('q1:7')
    alpha, beta, gamma = symbols('alpha beta gamma', real = True)
    px, py, pz = symbols('px py pz', real = True)

    # Rotation of joint 3 wrt to the base frame interms the first three angles q1, q2, q3
    R03 = Matrix([
    [sin(q2 + q3)*cos(q1), cos(q1)*cos(q2 + q3), -sin(q1)],
    [sin(q1)*sin(q2 + q3), sin(q1)*cos(q2 + q3),  cos(q1)],
    [        cos(q2 + q3),        -sin(q2 + q3),        0]])

    # Transpose of R03 
    R03T = Matrix([
    [sin(q2 + q3)*cos(q1), sin(q1)*sin(q2 + q3),  cos(q2 + q3)],
    [cos(q1)*cos(q2 + q3), sin(q1)*cos(q2 + q3), -sin(q2 + q3)],
    [            -sin(q1),              cos(q1),             0]])

    # Rotation of joint 6 wrt to frame of joint 3 interms of the last three angles q4, q5, q6
    R36 = Matrix([
    [-sin(q4)*sin(q6) + cos(q4)*cos(q5)*cos(q6), -sin(q4)*cos(q6) - sin(q6)*cos(q4)*cos(q5), -sin(q5)*cos(q4)],
    [                           sin(q5)*cos(q6),                           -sin(q5)*sin(q6),          cos(q5)],
    [-sin(q4)*cos(q5)*cos(q6) - sin(q6)*cos(q4),  sin(q4)*sin(q6)*cos(q5) - cos(q4)*cos(q6),  sin(q4)*sin(q5)]])

    # Rotation of urdf_gripper with respect to the base frame interms of alpha = yaw, beta = pitch, gamma = roll
    R0u = Matrix([
    [1.0*cos(alpha)*cos(beta), -1.0*sin(alpha)*cos(gamma) + sin(beta)*sin(gamma)*cos(alpha), 1.0*sin(alpha)*sin(gamma) + sin(beta)*cos(alpha)*cos(gamma)],
    [1.0*sin(alpha)*cos(beta),  sin(alpha)*sin(beta)*sin(gamma) + 1.0*cos(alpha)*cos(gamma), sin(alpha)*sin(beta)*cos(gamma) - 1.0*sin(gamma)*cos(alpha)],
    [          -1.0*sin(beta),                                     1.0*sin(gamma)*cos(beta),                                    1.0*cos(beta)*cos(gamma)]])

    # Total transform of gripper wrt to base frame given orientation yaw (alpha), pitch (beta), roll (beta) and position px, py, pz
    T0g_b = Matrix([
    [1.0*sin(alpha)*sin(gamma) + sin(beta)*cos(alpha)*cos(gamma),  1.0*sin(alpha)*cos(gamma) - 1.0*sin(beta)*sin(gamma)*cos(alpha), 1.0*cos(alpha)*cos(beta), px],
    [sin(alpha)*sin(beta)*cos(gamma) - 1.0*sin(gamma)*cos(alpha), -1.0*sin(alpha)*sin(beta)*sin(gamma) - 1.0*cos(alpha)*cos(gamma), 1.0*sin(alpha)*cos(beta), py],
    [                                   1.0*cos(beta)*cos(gamma),                                        -1.0*sin(gamma)*cos(beta),           -1.0*sin(beta), pz],
    [                                                          0,                                                                0,                        0,  1]])

    # Total transform of gripper wrt to base frame given angles q1, q2, q3, q4, q5, q6
    T0g_a = Matrix([
    [((sin(q1)*sin(q4) + sin(q2 + q3)*cos(q1)*cos(q4))*cos(q5) + sin(q5)*cos(q1)*cos(q2 + q3))*cos(q6) - (-sin(q1)*cos(q4) + sin(q4)*sin(q2 + q3)*cos(q1))*sin(q6), -((sin(q1)*sin(q4) + sin(q2 + q3)*cos(q1)*cos(q4))*cos(q5) + sin(q5)*cos(q1)*cos(q2 + q3))*sin(q6) + (sin(q1)*cos(q4) - sin(q4)*sin(q2 + q3)*cos(q1))*cos(q6), -(sin(q1)*sin(q4) + sin(q2 + q3)*cos(q1)*cos(q4))*sin(q5) + cos(q1)*cos(q5)*cos(q2 + q3), -0.303*sin(q1)*sin(q4)*sin(q5) + 1.25*sin(q2)*cos(q1) - 0.303*sin(q5)*sin(q2 + q3)*cos(q1)*cos(q4) - 0.054*sin(q2 + q3)*cos(q1) + 0.303*cos(q1)*cos(q5)*cos(q2 + q3) + 1.5*cos(q1)*cos(q2 + q3) + 0.35*cos(q1)],
    [ ((sin(q1)*sin(q2 + q3)*cos(q4) - sin(q4)*cos(q1))*cos(q5) + sin(q1)*sin(q5)*cos(q2 + q3))*cos(q6) - (sin(q1)*sin(q4)*sin(q2 + q3) + cos(q1)*cos(q4))*sin(q6), -((sin(q1)*sin(q2 + q3)*cos(q4) - sin(q4)*cos(q1))*cos(q5) + sin(q1)*sin(q5)*cos(q2 + q3))*sin(q6) - (sin(q1)*sin(q4)*sin(q2 + q3) + cos(q1)*cos(q4))*cos(q6), -(sin(q1)*sin(q2 + q3)*cos(q4) - sin(q4)*cos(q1))*sin(q5) + sin(q1)*cos(q5)*cos(q2 + q3),  1.25*sin(q1)*sin(q2) - 0.303*sin(q1)*sin(q5)*sin(q2 + q3)*cos(q4) - 0.054*sin(q1)*sin(q2 + q3) + 0.303*sin(q1)*cos(q5)*cos(q2 + q3) + 1.5*sin(q1)*cos(q2 + q3) + 0.35*sin(q1) + 0.303*sin(q4)*sin(q5)*cos(q1)],
    [                                                                -(sin(q5)*sin(q2 + q3) - cos(q4)*cos(q5)*cos(q2 + q3))*cos(q6) - sin(q4)*sin(q6)*cos(q2 + q3),                                                                  (sin(q5)*sin(q2 + q3) - cos(q4)*cos(q5)*cos(q2 + q3))*sin(q6) - sin(q4)*cos(q6)*cos(q2 + q3),                                     -sin(q5)*cos(q4)*cos(q2 + q3) - sin(q2 + q3)*cos(q5),                                                                                 -0.303*sin(q5)*cos(q4)*cos(q2 + q3) - 0.303*sin(q2 + q3)*cos(q5) - 1.5*sin(q2 + q3) + 1.25*cos(q2) - 0.054*cos(q2 + q3) + 0.75],
    [                                                                                                                                                            0,                                                                                                                                                             0,                                                                                        0,                                                                                                                                                                                                              1]])

    # Rotation of urdf_gripper wrt (DH) gripper frame from rotz(pi) * roty(-pi/2) and it's transpose
    Rgu_eval = Matrix([[0, 0, 1], [0, -1.00000000000000, 0], [1.00000000000000, 0, 0]])
    RguT_eval = Matrix([[0, 0, 1], [0, -1.00000000000000, 0], [1.00000000000000, 0, 0]])

    # Inverse kinematics transformations starts below

    R0u_eval = R0u.evalf(subs = {alpha: yaw, beta: pitch, gamma: roll})
    R0g_eval = R0u_eval * RguT_eval

    wrist_center = get_wrist_center(gripper_point, R0g_eval, dg = 0.303)

    j1, j2, j3 = get_first_three_angles(wrist_center)

    R03T_eval = R03T.evalf(subs = {q1: j1.evalf(), q2: j2.evalf(), q3: j3.evalf()})
    R36_eval = R03T_eval * R0g_eval

    j4, j5, j6 = get_last_three_angles(R36_eval)
    
    # The following code is been modified to be used as required 

    joint.append(j1.evalf())
    joint.append(j2.evalf())
    joint.append(j3.evalf())
    joint.append(j4.evalf())
    joint.append(j5.evalf())
    joint.append(j6.evalf())
    
    return np.fromiter(joint, dtype=complex)
  
def simulation_init(): #Function used to initialize the connection between the Simulation and The Program
    
    sim.simxFinish(-1) # just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
    error,jh1 = sim.simxGetObjectHandle(clientID, 'j1', sim.simx_opmode_oneshot_wait) 
    error,jh2 = sim.simxGetObjectHandle(clientID, 'j2', sim.simx_opmode_oneshot_wait) 
    error,jh3 = sim.simxGetObjectHandle(clientID, 'j3', sim.simx_opmode_oneshot_wait) 
    error,jh4 = sim.simxGetObjectHandle(clientID, 'j4', sim.simx_opmode_oneshot_wait) 
    error,jh5 = sim.simxGetObjectHandle(clientID, 'j5', sim.simx_opmode_oneshot_wait) 
    error,jh6 = sim.simxGetObjectHandle(clientID, 'j6', sim.simx_opmode_oneshot_wait) 
    
    
    joint_handle = np.array([jh1,jh2,jh3,jh4,jh5,jh6])
    
    return clientID, joint_handle
    
def simulation_run(px,py,pz,ex,ey,ez,joint_handle,clientID): # Function is used to calculate joint positions and Send them to the simulation
    
    joint = get_angles(px,py,pz,ex,ey,ez)
    
    if clientID!=-1:
                      
        
        #Actual Joint position
        error,joint1 =sim.simxGetJointPosition(clientID, joint_handle[0],sim.simx_opmode_oneshot)
        error,joint2 =sim.simxGetJointPosition(clientID, joint_handle[1],sim.simx_opmode_oneshot)
        error,joint3 =sim.simxGetJointPosition(clientID, joint_handle[2],sim.simx_opmode_oneshot)
        error,joint4 =sim.simxGetJointPosition(clientID, joint_handle[3],sim.simx_opmode_oneshot)
        error,joint5 =sim.simxGetJointPosition(clientID, joint_handle[4],sim.simx_opmode_oneshot)
        error,joint6 =sim.simxGetJointPosition(clientID, joint_handle[5],sim.simx_opmode_oneshot)

        
        #Setting Next Joint Position
        error= sim.simxSetJointTargetPosition(clientID, joint_handle[0], joint[0].real, sim.simx_opmode_oneshot)
        error= sim.simxSetJointTargetPosition(clientID, joint_handle[1], joint[1].real, sim.simx_opmode_oneshot)
        error= sim.simxSetJointTargetPosition(clientID, joint_handle[2], joint[2].real, sim.simx_opmode_oneshot)
        error= sim.simxSetJointTargetPosition(clientID, joint_handle[3], joint[3].real, sim.simx_opmode_oneshot)
        error= sim.simxSetJointTargetPosition(clientID, joint_handle[4], joint[4].real, sim.simx_opmode_oneshot)
        error= sim.simxSetJointTargetPosition(clientID, joint_handle[5], joint[5].real, sim.simx_opmode_oneshot)


#end Simulation Code ********************************************************************
