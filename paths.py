import random, math
import Tkinter as tk
import random, math
import re
#defining the arena and some constants
step_size = 0.1
num_paths = 2
num_steps = 15
alpha = 0.2
increment = 5
corners = [[0,0],[0,100],[100,0],[100,100]]
initialLocation = [50,50]
surviving_size = 10

root = tk.Tk()

canvas = tk.Canvas(root, width=800, height=800)

def compare_paths(path1, path2):
    comparison = path1[-1]-path2[-1]
    if comparison < 0:
        return -1
    elif comparison == 0:
        return 0
    else:
        return 1
#scoring how close to the edges
def score(location):
    location = [location[0]-50, location[1]-50]
    return max(abs(location[0]), abs(location[1]))
#find the endpoint of your path
def end_point (path):
    location = [50,50]
    for step in path:
        location[0] += step[0]
        location[1] += step[1]
    return location
#find the score of your path, based on how close to the edges
def score_path(path):
    return score(end_point(path))

#normalize a dictionary
def normalizeDict(d):
    sum = sum(d.keys())
    for key in d.keys():
        d[key] /= sum
#create a new list of paths
def modify_list_of_paths(paths):
    extend_paths(paths)
    num_copies = num_paths / surviving_size
    additional_paths = []
    for i in range(len(paths)):
        for j in range(num_copies):
            newPath = paths[i]
            for k in range(len(paths[i])):
                direction = math.atan2(paths[i][k][1], paths[i][k][0])
                direction += random.uniform(-alpha, alpha)
                newPath[k][0] = math.cos(direction)
                newPath[k][1] = math.sin(direction)
            additional_paths.append(newPath)
    paths+=additional_paths

#extend paths so that there are more steps per iteration
def extend_paths(paths):
    for path in paths:
        steps = []
        for j in range(increment):
            direction = random.uniform(0, 2*math.pi)
            step = [math.cos(direction), math.sin(direction)]
            step = [step[0]*step_size, step[1]*step_size]
            steps.append(step)
        path+=steps
    global num_steps
    num_steps += increment

#actually move the rectangles
def moveRects(rects, paths, i):
    if i < num_steps:
        for j in range(num_paths):
            canvas.move(rects[j], paths[j][i][0], paths[j][i][1])
            if max(abs((rects[j].coords()[0]+rects[j].coords()[2])/2-400), abs((rects[j].coords()[1]+rects[j].coords()[3])/2-400)) > 400:
                return rects[i]
        i+=1
        canvas.after(100, moveRects, rects, paths, i)





paths = []
#initially create a set of random paths
for i in range(num_paths):
    path = []
    for j in range(num_steps):
        direction = random.uniform(0, 2*math.pi)
        step = [math.cos(direction), math.sin(direction)]
        step = [step[0]*step_size, step[1]*step_size]
        path.append(step)
    paths.append(path)
#populate with scores of paths in a dict

rects = [canvas.create_rectangle(390, 390, 410, 410) for i in range(num_paths)]
print rects

moveRects(rects, paths, 0)

#loop until we reach edge
reached_the_edge = False
while not reached_the_edge:
    for path in paths:
        path.append(score_path(path))
    sorted_paths = sorted(paths, cmp=compare_paths)
    paths = sorted_paths[0:surviving_size]
    paths = [path[:-1] for path in paths]
    paths = modify_list_of_paths(paths)
    if moveRects(rects, paths, 0) is not None:
        reached_the_edge = True
    print 'was here'
canvas.pack()
root.mainloop()
