import math

def exp(x):
    return math.exp(x)

# define variable

# x: iris x poittion
# hx: husky x poittion
# hvx: husky x direction velocity
# dvx: desire x direction velocity
# cb: cable distance
# beta defined in main_iris.py
# bv: backup velocity ( pi in paper ) 
# b0v: backup velocity when velocity = 0
# h0: this is h in paper
# lambda0: lambda in paper

def backupcontroller(x, y, z, hx, hy, hz, hvx, hvy, cb, beta, dvx, dvy, dvz, bv, b0v):
    distance = ((x - hx) ** 2 + (y - hy) ** 2 + (z - hz) ** 2) ** 0.5
    h0 = cb ** 2 - (x - hx) ** 2 - (y - hy) ** 2 - (z - hz) ** 2 - 0.25
    lambda0 = 1 - exp(-1 * beta * max(h0, 0))

    if dvx > 0 and x - hx >= 0:
        ux = lambda0 * dvx + (1 - lambda0) * (-1 * bv + hvx)          
    elif dvx < 0 and x - hx < 0:
        ux = lambda0 * dvx + (1 - lambda0) * (1 * bv + hvx) 
    elif dvx == 0 and x - hx > 0 :
        ux = lambda0 * dvx + (1 - lambda0) * (-1 * b0v + hvx)
    elif dvx == 0 and x - hx < 0 :
        ux = lambda0 * dvx + (1 - lambda0) * (1 * b0v + hvx) 
    else :
        ux = dvx  

    if dvy > 0 and y - hy >= 0:
        uy = lambda0 * dvy + (1-lambda0) * (-1 * bv + hvy)  
    elif dvy < 0 and y - hy < 0: 
        uy = lambda0 * dvy + (1-lambda0) * (1 * bv + hvy)
    elif dvy == 0 and y - hy > 0:
        uy = lambda0 * dvy + (1-lambda0) * (-1 * b0v + hvy)
    elif dvy == 0 and y - hy < 0:
        uy = lambda0 * dvy + (1-lambda0) * (1 * b0v + hvy)       
    else :  
        uy = dvy
    uz = lambda0 * dvz + (1-lambda0) * (-1 *  0.05)

    return ux, uy, uz ,distance
