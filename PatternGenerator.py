# -*- coding: utf-8 -*-
"""
Some basic functions for designing pattern.
"""
import numpy as np

def dotPattern(x,y,dose=1):
    '''just dots and dose.'''
    return np.array([[x,y,dose]])

def linPattern(x1,y1,x2,y2,ss,dose=1):
    '''line start at (x1,y2), end at (x2,y2), step and dose at each step.'''
    assert ss > 0
    d=np.sqrt((x2-x1)**2+(y2-y1)**2)
    a=np.arctan((y2-y1)/(x2-x1))
    n=int(round(d/ss))
    pattern=np.zeros((n, 3), dtype = np.float32)
    for i in range(n):
        pattern[i] = [x1+i*ss*np.cos(a),y1+i*ss*np.sin(a),dose]
    return pattern

#l=linPattern(0,0,100,0,4)

def rectPattern(x1,y1,x2,y2,ss,dose=1):
    '''rectangle = rows x lines.'''
    assert ss > 0
    nx=int(round(abs(x2-x1)/ss))
    ny=int(round(abs(y2-y1)/ss))
    pattern=np.zeros((nx*ny, 3), dtype = np.float32)
    for i in range(ny):
        pattern[i*nx:(i+1)*nx]=linPattern(x1,y1+i*ss,x2,y1+i*ss,ss,dose)
    return pattern

#rect=rectPattern(0,0,20,10,3)

def ringPattern(x,y,r,ss,dose=1):
    '''ring center (x,y), radius r, step size and dose.
    '''
    assert ss > 0
    n=int(2*np.pi*r/ss)
    pattern=np.zeros((n, 3), dtype = np.float32)
    try:
        a=2*np.pi/n
        for i in range(n):
            pattern[i]=[x+r*np.cos(a*i),y+r*np.sin(a*i),1]
    except ZeroDivisionError:
        pattern=dotPattern(x,y,dose)
    return pattern

#ring=ringPattern(0,0,r,4)

def circPattern(x,y,r,ss,dose=1):
    '''circle filled center at (x,y), radius, step size and dose.'''
    assert ss > 0
    pattern=np.zeros((0, 3), dtype = np.float32)
    nr=int(r/ss)
    for i in range(nr):
        pattern=np.append(pattern,ringPattern(x,y,i*ss,ss,dose),axis=0)
    return pattern

#circ=circPattern(0,0,r,ss)

def trianPattern(x,y,a,ss,dose=1):
    '''todo!'''
    return

def polyPattern(points,ss,dose=1):
    '''todo!'''
    return

def rot(alpha):
    '''rotation angle alpha.
    use case:
        l=linPattern(0,0,36,0,4)
        rota=rot(np.pi/3)
        l2=l[:,:-1]*rota'''
    return np.matrix( [[np.cos(alpha),-np.sin(alpha)],[np.sin(alpha),np.cos(alpha)]] )

def addPattern(pattern1,pattern2):
    '''add pattern1 to pattern2.'''
    pout=np.append(pattern2,pattern1,axis=0)
    return pout

def mvPattern(x,y,pattern):
    '''move pattern to (x,y).'''
    pout=np.zeros_like(pattern)
    for i in range(pattern.shape[0]):
        pout[i,:-1]=[x,y]-pattern[i,:-1]
        pout[i,-1]=pattern[i,-1]
    return pout

def replacePointsByPattern(points, pattern):
    '''map pattern to each site of points.'''
    pout=mvPattern(points[0,0],points[0,1],pattern)
    for point in points[1:]:
        pout=np.append(pout,mvPattern(point[0],point[1],pattern),axis=0)
    return pout

def PCsPattern(size,radius,a):
    '''create sites for PhCs.'''
    h=a*np.sin(np.pi/3) #space between 2 holes in y line
    nx=int((size-2*radius)/a);Lx=a*nx+2*radius
    ny=int((size-2*radius)/h);Ly=h*ny+2*radius
    pattern = np.zeros((0, 2), dtype = np.float32)
    for i in range(ny+1):
        y = i*h - Ly/2 + radius
        for j in range(nx+1-(i%2)):
            x = (j + (i%2)*0.5)*a -Lx/2 + radius
            pattern=np.append(pattern,[[x,y]],axis=0)
    return np.array(pattern)

def PCsPattern2(a):
    '''another PhCs sites.'''
    cols=np.arange(-12,12,1)
    rows=np.arange(-14,13,2)
    site_points=np.zeros((0, 2), dtype = np.float32)
    h=a*np.sin(np.pi/3)
    for row in rows[::-1]:
        for col in cols:
            yd = row*h
            xd = col*a
            yu = yd + h
            xu = xd + a/2
            site_points=np.append(site_points,[[xu,yu]],axis=0)
            site_points=np.append(site_points,[[xd,yd]],axis=0)
    return site_points

def raithDots(p=1000,start_dose=1,dose_step=0.1,nx=30,ny=70):
    '''Raith Demo dots dose test: pitch=1 (default) or 0.5 µm.'''
    pattern = np.zeros_like(np.ndarray(((nx+1)*(ny+1),3)))
    for i in range(pattern.shape[0]):
        x = -nx*p/2 + (i%(nx+1))*p
        stepy=int(i/(nx+1))
        y = -ny*p/2 + stepy*p
        dose = start_dose + stepy*dose_step
        pattern[i]=[x,y,dose]
    return pattern

