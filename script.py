import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 20
  
    p = mdl.parseFile(filename)
    polygons = []
    edges = []
    if p:
        (commands, symbols) = p
        for x in commands:
            if x[0] != "rotate" and x[0] != "save" and x[0] != "display":
                t = [x[0]]
                for y in x[1:]:
                    if isinstance(y, float):
                        t.append(y)
                x = tuple(t)

            l = x[0]
            if l == 'sphere':
                add_sphere(polygons,
                            float(x[1]), float(x[2]), float(x[3]),
                            float(x[4]), step_3d)
                matrix_mult( stack[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []
            elif l == 'torus':

                add_torus(polygons,
                        float(x[1]), float(x[2]), float(x[3]),
                        float(x[4]), float(x[5]), step_3d)
                matrix_mult( stack[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []
                
            elif l == 'box':

                add_box(polygons,
                        float(x[1]), float(x[2]), float(x[3]),
                        float(x[4]), float(x[5]), float(x[6]))
                matrix_mult( stack[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []

            elif l == 'l':
                add_edge( edges,
                        float(x[1]), float(x[2]), float(x[3]),
                        float(x[4]), float(x[5]), float(x[6]) )
                matrix_mult( stack[-1], edges )
                draw_ls(edges, screen, zbuffer, color)
                edges = []

            elif l == 'scale':
                t = make_scale(float(x[1]), float(x[2]), float(x[3])) #check this
                matrix_mult( stack[-1], t )
                stack[-1] = [ x[:] for x in t]

            elif l == 'move':
                t = make_translate(float(x[1]), float(x[2]), float(x[3]))
                matrix_mult( stack[-1], t )
                stack[-1] = [ x[:] for x in t]

            elif l == 'rotate':
                o = float(x[2]) * (math.pi / 180)
                if x[1] == 'x':
                    t = make_rotX(o)
                elif x[1] == 'y':
                    t = make_rotY(o)
                else:
                    t = make_rotZ(o)
                matrix_mult( stack[-1], t )
                stack[-1] = [ x[:] for x in t]

            elif l == 'push':
                stack.append( [x[:] for x in stack[-1]] )

            elif l == 'pop':
                stack.pop()

            elif l == 'display' or l == 'save':
                 if l == 'display':
                    display(screen)
                 else:
                    save_extension(screen, x[1] + x[2])
                
    else:
        print ("Parsing failed.")
        return
