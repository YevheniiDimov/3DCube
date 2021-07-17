import pygame
import numpy as np
import math
import sys


height, width = 750, 750

sc = pygame.display.set_mode((height, width))

center = np.array([width/2, height/2, 0])
scale = 10

FPS = 60

pygame.init()
clock = pygame.time.Clock()

class Object3D():
    def __init__(self, position, points = np.array([])):
        self.Position = position
        self.Points = points

    def Points2D(self):
        arr = list([p[0], p[1]] for p in self.Points)
        return np.array(arr)

    def getCenter(self):
        return np.array([np.average(self.Points[:,0]), np.average(self.Points[:,1]), np.average(self.Points[:,2])])

    def getXRotationMatrix(self, theta):
        return np.array([
            [1, 0, 0],
            [0, math.cos(theta), -math.sin(theta)],
            [0, math.sin(theta), math.cos(theta)],
        ]);

    def getYRotationMatrix(self, theta):
        return np.array([
            [math.cos(theta), 0, math.sin(theta)],
            [0, 1, 0],
            [-math.sin(theta), 0, math.cos(theta)],
        ]);

    def getZRotationMatrix(self, theta):
        return np.array([
            [math.cos(theta), math.sin(theta), 0],
            [-math.sin(theta), math.cos(theta), 0],
            [0, 0, 1]
        ]);

    def getScalingMatrix(self, scale):
        return np.array([
            [scale, 0, 0],
            [0, scale, 0],
            [0, 0, scale]
        ]);

    def draw(self, xAngle, yAngle, zAngle, scale = 1):
        points = []

        self.Center = self.getCenter()
        pygame.draw.circle(sc, np.array([0, 0, 0]), np.array(self.Center + self.Position)[:-1], 5)

        for point in self.Points:
            point = point - self.Center

            point = point.dot(self.getXRotationMatrix(xAngle))
            point = point.dot(self.getYRotationMatrix(yAngle))
            point = point.dot(self.getZRotationMatrix(zAngle))
            point = point.dot(self.getScalingMatrix(scale))
            
            point = np.add(point, self.Center)
            point = np.array([point[0] + self.Position[0], point[1] + self.Position[1]])
            
            points.append(point)

        for point1 in points:
            for point2 in points:
                for point3 in points:
                    pygame.draw.polygon(sc, np.array([150, 150, 150]), np.array([point1, point2, point3]))
        
        for point in points:
            pygame.draw.circle(sc, np.array([100, 100, 100]), point, 5)
 

class Cube(Object3D):
    def __init__(self, size, position = np.array([0, 0, 0])):
        super().__init__(position)
        points = []
        for x in range(0, size+1, size):
            for y in range(0, size+1, size):
                for z in range(0, size+1, size):
                    points.append([x, y, z])

        self.Points = np.array(points)

cube1 = Cube(50, center)
xTheta, yTheta, zTheta = 0, 0, 0
vector = np.array([0, 0, 0])
scale = 1

while True:
    clock.tick(FPS)
    sc.fill((255, 255, 255))
    
    cube1.draw(xTheta, yTheta, zTheta, scale)

    for i in pygame.event.get():
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_w:
                vector[0] = -0.1
            elif i.key == pygame.K_s:
                vector[0] = 0.1
            elif i.key == pygame.K_a:
                vector[1] = -0.1
            elif i.key == pygame.K_d:
                vector[1] = 0.1
            elif i.key == pygame.K_z:
                vector[2] = -0.1
            elif i.key == pygame.K_x:
                vector[2] = 0.1
        elif i.type == pygame.KEYUP:
            vector = np.zeros(3)
        elif i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 4:
                scale += 0.05
            elif i.button == 5:
                scale -= 0.05
        elif i.type == pygame.QUIT:
            sys.exit()

    xTheta += vector[0]
    yTheta += vector[1]
    zTheta += vector[2]

    pygame.display.update()