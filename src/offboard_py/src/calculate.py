import math

def exp(x):
    return math.exp(x)

def backupcontroller(x, y, z, hx, hy, hz, hvx, hvy, cb, beta, dx, dy, dz, bv, b0v):
    distance = ((x - hx) ** 2 + (y - hy) ** 2 + (z - hz) ** 2) ** 0.5
    hdv = cb ** 2 - (x - hx) ** 2 - (y - hy) ** 2 - (z - hz) ** 2
    lambda0 = 1 - exp(-1 * beta * max(hdv, 0))

    if dx > 0 and x - hx >= 0:
        ux = lambda0 * dx + (1 - lambda0) * (-1 * bv + hvx)          
    elif dx < 0 and x - hx < 0:
        ux = lambda0 * dx + (1 - lambda0) * (1 * bv + hvx) 
    elif dx == 0 and x - hx > 0 :
        ux = lambda0 * dx + (1 - lambda0) * (-1 * b0v + hvx)
    elif dx == 0 and x - hx < 0 :
        ux = lambda0 * dx + (1 - lambda0) * (1 * b0v + hvx) 
    else :
        ux = dx  

    if dy > 0 and y - hy >= 0:
        uy = lambda0 * dy + (1-lambda0) * (-1 * bv + hvy)  
    elif dy < 0 and y - hy < 0: 
        uy = lambda0 * dy + (1-lambda0) * (1 * bv + hvy)
    elif dy == 0 and y - hy > 0:
        uy = lambda0 * dy + (1-lambda0) * (-1 * b0v + hvy)
    elif dy == 0 and y - hy < 0:
        uy = lambda0 * dy + (1-lambda0) * (1 * b0v + hvy)       
    else :  
        uy = dy
    uz = lambda0 * dz + (1-lambda0) * (-1 *  0.05)

    return ux, uy, uz ,distance