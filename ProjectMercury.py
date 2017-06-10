"""
PROJECT MERCURY: An Accurate Edge Detection and Character Recognition Tool for 
				          Analyzing Ancient Classical Inscriptions

V1.0
Copyright 2016-2017: Prathik Naidu

In collaboration with:
	Joseph Dexter, Harvard Medical School
	Pramit Chaudhuri Ph.D., University of Texas at Austin Department of Classics
"""

from math import tan,sin,cos,atan2
import time


### Main method for detecting letters
def main():
    string = open('original1.ppm').read().split()
    string.pop(0)
    row = int(string.pop(0))
    col = int(string.pop(0))
    string.pop(0)
    rgb = list(map(int,string))
    grey = list()
    y = 0
    while y < col:
        x = 0
        while x < row:
            grey.append(int(rgb[(y*row+x)*3]*0.3+rgb[(y*row+x)*3+1]*0.59+rgb[(y*row+x)*3+2]*0.11))
            x+=1
        y+=1
    fileout = open('grey.ppm','w')
    smoothing = open('smooth.ppm','w')
    smoothingc = open('smoothc.ppm','w')
    edging = open('edges.ppm','w')
    edgingc = open('edgesc.ppm','w')
    edgingt = open('edgest.ppm','w')
    edgingtc = open('edgestc.ppm','w')
    edgingmc = open('edgesmc.ppm','w')
    smooth = [[1,2,1],[2,4,2],[1,2,1]]
    Gx = [[-1,0,1],[-2,0,2],[-1,0,1]]
    G = list()
    Gy = [[-1,-2,-1],[0,0,0],[1,2,1]]
    edging.write('P3\n'+str(row)+' '+str(col)+'\n255\n')
    edgingc.write('P3\n'+str(row)+' '+str(col)+'\n255\n')
    edgingt.write('P3\n'+str(row)+' '+str(col)+'\n255\n')
    edgingtc.write('P3\n'+str(row)+' '+str(col)+'\n255\n')
    edgingmc.write('P3\n'+str(row)+' '+str(col)+'\n255\n')
    fileout.write('P3\n'+str(row)+' '+str(col)+'\n255\n')
    smoothing.write('P3\n'+str(row)+' '+str(col)+'\n255\n')
    smoothingc.write('P3\n'+str(row)+' '+str(col)+'\n255\n')
    y = 0

    #Main algorithm for detecting letters
    while y < col:
        x = 0
        while x < row:
            changed = False
            s = str(grey[y*row+x])
            fileout.write(s+' '+s+' '+s+' ')
        #print(x,y,y*row,len(grey),row,(y+1)*row,y*row+x,(y+1)*row+x)
        
            if x == 0 or x== (row-1):
                ed = str(0)
                G.append((0,0))
            elif y==0 or y==(col-1):
                G.append((0,0))
                ed = str(0)
            else:
                totv = multiplygray(Gx,grey,y,x,row)
                toth = multiplygray(Gy,grey,y,x,row)
                Ga = abs((int)(toth))+abs((int)(totv))
                theta = atan2(toth,totv)
                G.append((Ga,theta))
                if Ga>99:
                    changed = True
            
            
            if x == 0 or x== (row-1):
                sm = s
                smc = str(rgb[(y*row+x)*3])+' '+str(rgb[(y*row+x)*3+1])+' '+str(rgb[(y*row+x)*3+2])+' '
            if y==0 or y==(col-1):
                sm = s
                smc = str(rgb[(y*row+x)*3])+' '+str(rgb[(y*row+x)*3+1])+' '+str(rgb[(y*row+x)*3+2])+' '
            else:
                sm = str(multiplygray(smooth,grey,y,x,row))
                smc = str(multiplycolor(smooth,rgb,y,x,row))
            #print(smc)
            smoothing.write(sm+' '+sm+' '+sm+' ')
            smoothingc.write(smc)
            if changed:
                edging.write('0 0 0 ')
                edgingc.write(str(rgb[(y*row+x)*3])+' '+str(rgb[(y*row+x)*3+1])+' '+str(rgb[(y*row+x)*3+2])+' ')
            else:
                edging.write('255 255 255 ')
                edgingc.write('255 255 255 ')
            x+=1
        fileout.write('\n')
        smoothing.write('\n')
        smoothingc.write('\n')
        edging.write('\n')
        edgingc.write('\n')
        y+=1
    edgeslist = []
    y = 0
    while y < col:
        x = 0
        while x < row:
            change = False
            changed = False
            if x == 0 or x== (row-1):
                ed = str(0)
            elif y==0 or y==(col-1):
                ed = str(0)
            else:
                
                a,b = thetaToInt(G[y*row+x][1])
                if G[y*row+x][0]>max(G[(y-a)*row+x-b][0],G[(y+a)*row+x+b][0]):
                        change = True
                if G[y*row+x][0]>100:
                    if change:
                        changed = True
            if changed:
                edgingt.write('0 0 0 ')
                edgeslist.append([x,y])
                edgingtc.write(str(rgb[(y*row+x)*3])+' '+str(rgb[(y*row+x)*3+1])+' '+str(rgb[(y*row+x)*3+2])+' ')
            else:
                edgingt.write('255 255 255 ')
                edgingtc.write('255 255 255 ')
            if change:
                edgingmc.write(str(rgb[(y*row+x)*3])+' '+str(rgb[(y*row+x)*3+1])+' '+str(rgb[(y*row+x)*3+2])+' ')
            else:
                edgingmc.write('255 255 255 ')
            x+=1
        edgingt.write('\n')
        edgingtc.write('\n')
        edgingmc.write('\n')
        y+=1
    #fileouta = open('Detect.ppm','w')
    
    #image = circleDetection(edgeslist,G,row,col)
    #image = lineDetection(edgeslist,G,row,col,image)
    #fileouta.write('P3\n'+str(row)+' '+str(col)+'\n255\n')
    #for x in image:
        #print(x)
     #   s = str(x)
      #  fileouta.write(s+' '+s+' '+s+'\n')

def multiplygray(matrix,grey,y,x,row):
    if (matrix[0][0]+matrix[0][1]+matrix[0][2]+matrix[1][0]+matrix[1][1]+matrix[1][2]+matrix[2][0]+matrix[2][1]+matrix[2][2]) == 0:
        return int((grey[(y-1)*row+x-2]*matrix[0][0]+grey[(y-1)*row+x-1]*matrix[0][1]+grey[(y-1)*row+x]*matrix[0][2]+grey[(y)*row+x-2]*matrix[1][0]+grey[(y)*row+x-1]*matrix[1][1]+grey[(y)*row+x]*matrix[1][2]+grey[(y+1)*row+x-2]*matrix[2][0]+grey[(y+1)*row+x-1]*matrix[2][1]+grey[(y+1)*row+x]*matrix[2][2])/(1))
    else:
        return int((grey[(y-1)*row+x-2]*matrix[0][0]+grey[(y-1)*row+x-1]*matrix[0][1]+grey[(y-1)*row+x]*matrix[0][2]+grey[(y)*row+x-2]*matrix[1][0]+grey[(y)*row+x-1]*matrix[1][1]+grey[(y)*row+x]*matrix[1][2]+grey[(y+1)*row+x-2]*matrix[2][0]+grey[(y+1)*row+x-1]*matrix[2][1]+grey[(y+1)*row+x]*matrix[2][2])/((matrix[0][0]+matrix[0][1]+matrix[0][2]+matrix[1][0]+matrix[1][1]+matrix[1][2]+matrix[2][0]+matrix[2][1]+matrix[2][2])))

def multiplycolorhelp(matrix,color,y,x,row,z):
    return str(int((color[((y-1)*row+x-2)*3+(2-z)]*matrix[0][0]+color[((y-1)*row+x-1)*3+(2-z)]*matrix[0][1]+color[((y-1)*row+x)*3+(2-z)]*matrix[0][2]+color[((y)*row+x-2)*3+(2-z)]*matrix[1][0]+color[((y)*row+x-1)*3+(2-z)]*matrix[1][1]+color[((y)*row+x)*3+(2-z)]*matrix[1][2]+color[((y+1)*row+x-2)*3+(2-z)]*matrix[2][0]+color[((y+1)*row+x)*3+(2-z)]*matrix[2][0]+color[((y+1)*row+x)*3+(2-z)]*matrix[2][2])/(matrix[0][0]+matrix[0][1]+matrix[0][2]+matrix[1][0]+matrix[1][1]+matrix[1][2]+matrix[2][0]+matrix[2][1]+matrix[2][2])))

def multiplycolor(matrix,color,y,x,row):
    return multiplycolorhelp(matrix,color,y,x,row,2)+' '+multiplycolorhelp(matrix,color,y,x,row,1)+' '+multiplycolorhelp(matrix,color,y,x,row,0)+' '

def thetaToInt(theta):
    theta = abs(theta)
    if 0.321>theta>0:
        return 1,0
    elif 1.24>theta>0.321:
        return 1,1
    elif 1.892>theta>1.24:
        return 0,1
    else:
        return 1,-1

times = []
for i in range(0,25):
    print i
    t0 = time.time()
    main()
    t1 = time.time()
    times.append(t1-t0)


print sum(times)/len(times)



