# COMP9021 19T3 - Rachid Hamadi
# Assignment 2 *** Due Sunday Week 10
#Student name: Pablo Pacheco


# IMPORT ANY REQUIRED MODULE


class MazeError(Exception):
    def __init__(self, message):
        self.message = message


class Maze:
    def __init__(self, filename):
        self.filemaze_name=filename[:-4]
        f=open(filename)
        lines=f.readlines()
        self.numb_lines = 0
        self.grid = []
        self.length_line=0
        for line in lines:
            new_line2 = line.replace(' ','')
            new_line = new_line2.replace('\n','')
            if new_line != '':
                self.length_line = len(new_line)
                break
                
        for line in lines:
            new_line2 = line.replace(' ','')
            new_line = new_line2.replace('\n','')
            if new_line != '':
                self.numb_lines +=1
                if len(new_line) > 31 or len(new_line)<2 or len(new_line) != self.length_line:
                    raise MazeError('Incorrect input.')
                if new_line[-1] == '1' or new_line[-1] == '3':
                    raise MazeError('Input does not represent a maze.')
                for i in new_line:
                    if i not in ['0', '1', '2', '3']:
                        raise MazeError('Incorrect input.')
                self.grid.append(new_line)        
                
                      
        if self.numb_lines > 41 or self.numb_lines < 2:
            raise MazeError('Incorrect input.')
            
        for line in reversed(lines):
            new_line2 = line.replace(' ','')
            new_line = new_line2.replace('\n','')
            if new_line !='':
                for i in new_line:
                    if i not in ['0','1']:
                        raise MazeError('Input does not represent a maze.')
                break
 

        self.framegrid = [[None for _ in range(self.length_line+2)] for _ in range(self.numb_lines+2)]
        for i in range(1,self.numb_lines+1):
            for j in range(1,self.length_line+1):
                self.framegrid[i][j]=self.grid[i-1][j-1]
         
        self.framegrid_o = [[None for _ in range(self.length_line+2)] for _ in range(self.numb_lines+2)]
        for i in range(1,self.numb_lines+1):
            for j in range(1,self.length_line+1):
                self.framegrid_o[i][j]=self.grid[i-1][j-1]
                
        self.inner_framegrid = [[[] for _ in range(self.length_line+1)] for _ in range(self.numb_lines+1)]
        for i in range(1,self.numb_lines):
            for j in range(1,self.length_line):
                if self.framegrid_o[i][j]=='0' or self.framegrid_o[i][j]=='2':
                    self.inner_framegrid[i][j].append('u')
                if self.framegrid_o[i+1][j]=='0' or self.framegrid_o[i+1][j]=='2':
                    self.inner_framegrid[i][j].append('d')
                if self.framegrid_o[i][j]=='0' or self.framegrid_o[i][j]=='1':
                    self.inner_framegrid[i][j].append('l')
                if self.framegrid_o[i][j+1]=='0' or self.framegrid_o[i][j+1]=='1':
                    self.inner_framegrid[i][j].append('r')
                    
        for i in range(self.numb_lines+1):
            self.inner_framegrid[i][0]='x'
            self.inner_framegrid[i][self.length_line]='x'
        for j in range(self.length_line+1):
            self.inner_framegrid[0][j]='x'
            self.inner_framegrid[self.numb_lines][j]='x'
        
        f.close()
        
        #gates
        self.gates=0
        for j in range(1,self.length_line):
            if self.grid[0][j-1] in ['0','2']:
                self.gates +=1
            if self.grid[self.numb_lines-1][j-1] in ['0','2']:
                self.gates +=1
        
        for i in range(1,self.numb_lines):
            if self.grid[i-1][0] in ['0','1']:
                self.gates +=1
            if self.grid[i-1][self.length_line-1] in ['0','1']:
                self.gates +=1
    
        #Walls
        self.walls=3
        for i in range(1,self.numb_lines+1):
            valid_in_row = self.framegrid[i].count('1')+self.framegrid[i].count('2')+self.framegrid[i].count('3')
            if valid_in_row < 1:
                continue
            for j in range(1,self.length_line+1):
                if self.framegrid[i][j]=='1' or self.framegrid[i][j]=='2' or self.framegrid[i][j]=='3':
                    self.walls +=1
                    self.recursive_colour(self.framegrid,i,j,self.walls,'right')
          
        #innaccesible inner points and accesible areas                                       
        self.inac_grid = [['ina' for _ in range(self.length_line+1)] for _ in range(self.numb_lines+1)]
        for i in range(self.numb_lines+1):
            self.inac_grid[i][0]='x'
            self.inac_grid[i][self.length_line]='x'
        for j in range(self.length_line+1):
            self.inac_grid[0][j]='x'
            self.inac_grid[self.numb_lines][j]='x'    
    
        
        self.acc_area = 0
        
        for j in range(1,self.length_line):
            if 'u' in self.inner_framegrid[1][j]:
                if self.inac_grid[1][j]=='ina':
                    self.acc_area +=1
                    self.recursive_inac(self.inner_framegrid,self.inac_grid,1,j,self.acc_area)
            if 'd' in self.inner_framegrid[self.numb_lines-1][j]:
                if self.inac_grid[self.numb_lines-1][j]=='ina':
                    self.acc_area +=1
                    self.recursive_inac(self.inner_framegrid,self.inac_grid,self.numb_lines-1,j,self.acc_area)
        
        for i in range(1,self.numb_lines):
            if 'l' in self.inner_framegrid[i][1]:
                if self.inac_grid[i][1]=='ina':
                    self.acc_area +=1
                    self.recursive_inac(self.inner_framegrid,self.inac_grid,i,1,self.acc_area)
            if 'r' in self.inner_framegrid[i][self.length_line-1]:
                if self.inac_grid[i][self.length_line-1]=='ina':
                    self.acc_area +=1
                    self.recursive_inac(self.inner_framegrid,self.inac_grid,i,self.length_line-1,self.acc_area)
      
        self.inac_inner_points= 0
        for i in range(1,self.numb_lines):
            for j in range(1,self.length_line):
                if self.inac_grid[i][j]=='ina':
                    self.inac_inner_points +=1
        
        #cul de sacs
        for i in range(1,self.numb_lines):
            for j in range(1,self.length_line):
                if len(self.inner_framegrid[i][j])==1:
                    self.recursive_cul(self.inner_framegrid,self.inac_grid,i,j,'C')
           
        self.inac_grid2 = [[None for _ in range(self.length_line+1)] for _ in range(self.numb_lines+1)]
        for i in range(self.numb_lines+1):
            for j in range(self.length_line+1):
                self.inac_grid2[i][j]=self.inac_grid[i][j]
        
        self.n_cul_desacs = 1500
        
        for i in range(1,self.numb_lines):
            for j in range(1,self.length_line):
                if self.inac_grid[i][j]=='C':
                    self.n_cul_desacs +=1
                    self.recursive_cul_colour(self.inner_framegrid,self.inac_grid,i,j,'C',self.n_cul_desacs)
        
        
        #Entry-exit path
        self.area_path_list=[]
        for area in range(1,self.acc_area+1):
            area_gates = 0 
            for j in range(1,self.length_line):
                if 'u' in self.inner_framegrid[1][j] and self.inac_grid2[1][j]==area:
                    area_gates +=1            
                if 'd' in self.inner_framegrid[self.numb_lines-1][j] and self.inac_grid2[self.numb_lines-1][j] == area:
                    area_gates +=1
                    
            for i in range(1,self.numb_lines):
                if 'l' in self.inner_framegrid[i][1] and self.inac_grid2[i][1]==area:
                    area_gates +=1     
                if 'r' in self.inner_framegrid[i][self.length_line-1] and self.inac_grid2[i][self.length_line-1]==area:
                    area_gates +=1
                    
            if area_gates ==2:
                self.area_path_list.append(area)
        
        extract_from_area_list = []        
        for area in self.area_path_list:
            for i in range(1,self.numb_lines):
                for j in range(1,self.length_line):
                    if self.inac_grid2[i][j]==area:
                        if (len(self.inner_framegrid[i][j]) - self.cul_neigh(self.inner_framegrid,self.inac_grid2,i,j,'C'))>2:
                            if not area in extract_from_area_list:
                                extract_from_area_list.append(area)
                    
        
        for i in extract_from_area_list:
            self.area_path_list.remove(i)
       

        for area in self.area_path_list:
            for j in range(1,self.length_line):
                if 'u' in self.inner_framegrid[1][j] and self.inac_grid2[1][j]==area:
                    self.recursive_cul_colour(self.inner_framegrid,self.inac_grid2,1,j,area,'P')           
                if 'd' in self.inner_framegrid[self.numb_lines-1][j] and self.inac_grid2[self.numb_lines-1][j] == area:
                    self.recursive_cul_colour(self.inner_framegrid,self.inac_grid2,self.numb_lines-1,j,area,'P')
                    
            for i in range(1,self.numb_lines):
                if 'l' in self.inner_framegrid[i][1] and self.inac_grid2[i][1]==area:
                    self.recursive_cul_colour(self.inner_framegrid,self.inac_grid2,i,1,area,'P')                        
                if 'r' in self.inner_framegrid[i][self.length_line-1] and self.inac_grid2[i][self.length_line-1]==area:
                    self.recursive_cul_colour(self.inner_framegrid,self.inac_grid2,i,self.length_line-1,area,'P')

        
        
    def recursive_colour(self,a,x,y,c,d):
 # d = in which direction the previos iteration was moved.
        #Apply number rule
        if a[x][y]=='1':
            a[x][y]=c
            self.recursive_colour(a,x,y+1,c,'right')            

        elif a[x][y]=='2':
            a[x][y]=c
            self.recursive_colour(a,x+1,y,c,'down')            

        elif a[x][y]=='3':
            a[x][y]=c
            self.recursive_colour(a,x,y+1,c,'right')
            self.recursive_colour(a,x+1,y,c,'down')
            
        #Look for left or up connection
        if d != 'right':
            if a[x][y-1]=='1' or a[x][y-1]=='3':
                a[x][y]=c
                self.recursive_colour(a,x,y-1,c,'left')
                
        if d != 'down':
            if a[x-1][y]=='2' or a[x-1][y]=='3':
                a[x][y]=c
                self.recursive_colour(a,x-1,y,c,'up')
        
        a[x][y]=c        

     
    def recursive_inac(self,a,b,x,y,c):
        if b[x][y] == 'ina':
            
            if 'l' in a[x][y]:
                b[x][y]=c
                self.recursive_inac(a,b,x,y-1,c)
            if 'u' in a[x][y]:
                b[x][y]=c
                self.recursive_inac(a,b,x-1,y,c)
            if 'd' in a[x][y]:
                b[x][y]=c
                self.recursive_inac(a,b,x+1,y,c)
            if 'r' in a[x][y]:
                b[x][y]=c
                self.recursive_inac(a,b,x,y+1,c)
        if b[x][y] != 'x': 
            b[x][y]=c
    
    def cul_neigh(self,a,b,x,y,c):
        neighbour=0
        if 'l' in a[x][y]:
            if b[x][y-1]==c:
                neighbour +=1
        if 'u' in a[x][y]:
            if b[x-1][y]==c:
                neighbour +=1
        if 'd' in a[x][y]:
            if b[x+1][y]==c:
                neighbour +=1
        if 'r' in a[x][y]:
            if b[x][y+1] ==c:
                neighbour +=1
        return neighbour
    
    def recursive_cul(self,a,b,x,y,c):
        if len(a[x][y])==1 and b[x][y] != c and b[x][y] != 'ina' and b[x][y] != 'x':
            b[x][y]=c
            if 'l' in a[x][y]:
                self.recursive_cul(a,b,x,y-1,c)
            if 'u' in a[x][y]:
                self.recursive_cul(a,b,x-1,y,c)
            if 'd' in a[x][y]:
                self.recursive_cul(a,b,x+1,y,c)
            if 'r' in a[x][y]:
                self.recursive_cul(a,b,x,y+1,c)
                
        elif (len(a[x][y])- self.cul_neigh(a,b,x,y,c))==1 and b[x][y] != c and b[x][y] != 'ina' and b[x][y] != 'x':
            b[x][y]=c
            if 'l' in a[x][y] and b[x][y-1] != c:
                self.recursive_cul(a,b,x,y-1,c)
            elif 'u' in a[x][y] and b[x-1][y] !=c:
                self.recursive_cul(a,b,x-1,y,c)
            elif 'd' in a[x][y] and b[x+1][y] !=c:
                self.recursive_cul(a,b,x+1,y,c)
            elif 'r' in a[x][y] and b[x][y+1] !=c:
                self.recursive_cul(a,b,x,y+1,c)
        
    def recursive_cul_colour(self,a,b,x,y,cul,c):
        if b[x][y]==cul:
            b[x][y]=c
            if 'l' in a[x][y]:
                self.recursive_cul_colour(a,b,x,y-1,cul,c)
            if 'u' in a[x][y]:
                self.recursive_cul_colour(a,b,x-1,y,cul,c)
            if 'd' in a[x][y]:
                self.recursive_cul_colour(a,b,x+1,y,cul,c)
            if 'r' in a[x][y]:
                self.recursive_cul_colour(a,b,x,y+1,cul,c)
    
    
    def analyse(self):
        
    #gates
                
        if self.gates == 0:
            print('The maze has no gate.')
        elif self.gates ==1:
            print('The maze has a single gate.')
        elif self.gates > 1:
            print('The maze has {} gates.'.format(self.gates))
            
    #walls
                    
        if self.walls == 3:
            print('The maze has no wall.')
        if self.walls == 4:
            print('The maze has walls that are all connected.')
        if self.walls >4:
            print('The maze has {} sets of walls that are all connected.'.format(self.walls-3))
        
    
    #innaccesible inner points and accesible areas                                       
                
        if self.inac_inner_points == 0:
            print('The maze has no inaccessible inner point.')
        if self.inac_inner_points == 1:
            print('The maze has a unique inaccessible inner point.')
        if self.inac_inner_points >1:
            print('The maze has {} inaccessible inner points.'.format(self.inac_inner_points))
        

        if self.acc_area == 0:
            print('The maze has no accessible area.')
        if self.acc_area == 1:
            print('The maze has a unique accessible area.')
        if self.acc_area >1:
            print('The maze has {} accessible areas.'.format(self.acc_area))


        #cul de sacs
                    
        if self.n_cul_desacs - 1500 == 0:
            print('The maze has no accessible cul-de-sac.')
        if self.n_cul_desacs - 1500 == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        if self.n_cul_desacs - 1500 >1:
            print('The maze has {} sets of accessible cul-de-sacs that are all connected.'.format(self.n_cul_desacs - 1500))
        
                
#Entry-exit path

        
        if len(self.area_path_list) == 0:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        if len(self.area_path_list) == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        if len(self.area_path_list) >1:
            print('The maze has {} entry-exit paths with no intersections not to cul-de-sacs.'.format(len(self.area_path_list)))
        
    def in_row_horizontal(self,a,x,y,i):
        count=i
        if a[x][y]=='1' or a[x][y]=='3':
            count +=1
            return self.in_row_horizontal(a,x,y+1,count)
        return count
    
    def in_row_vertical(self,a,x,y,i):
        count=i
        if a[x][y]=='2' or a[x][y]=='3':
            count +=1
            return self.in_row_vertical(a,x+1,y,count)
        return count
    
    def in_row_horizontal_path(self,a,b,x,y,i,j,k):
        count=i
        first_gate=j
        last_gate=k
        if b[x][y]=='P':
            count +=1
            if b[x][y-1]=='x' and 'l' in a[x][y]:
                first_gate=1
            if b[x][y+1]=='P' and 'r' in a[x][y]:
                return self.in_row_horizontal_path(a,b,x,y+1,count,first_gate,last_gate)
            if b[x][y+1]=='x' and 'r' in a[x][y]:
                last_gate=1
        return [count,first_gate,last_gate]
    
    def in_row_vertical_path(self,a,b,x,y,i,j,k):
        count=i
        first_gate=j
        last_gate=k
        if b[x][y]=='P':
            count +=1
            if b[x-1][y]=='x' and 'u' in a[x][y]:
                first_gate=1
            if b[x+1][y]=='P' and 'd' in a[x][y]:
                return self.in_row_vertical_path(a,b,x+1,y,count,first_gate,last_gate)
            if b[x+1][y]=='x' and 'd' in a[x][y]:
                last_gate=1
        return [count,first_gate,last_gate]        
    
    def display(self):
        complete_name=self.filemaze_name + '.tex'
        with open(complete_name,'w') as file:
            print('\\documentclass[10pt]{article}\n'
                  '\\usepackage{tikz}\n'
                  '\\usetikzlibrary{shapes.misc}\n'
                  '\\usepackage[margin=0cm]{geometry}\n'
                  '\\pagestyle{empty}\n'
                  '\\tikzstyle{every node}=[cross out, draw, red]\n'
                  '\n'
                  '\\begin{document}\n'
                  '\n'
                  '\\vspace*{\\fill}\n'
                  '\\begin{center}\n'
                  '\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n'
                  '% Walls', file=file)
            
            for i in range(1,self.numb_lines+1):
                for j in range(1,self.length_line+1):
                    in_row = self.in_row_horizontal(self.framegrid_o,i,j,0)
                    if in_row > 0 and self.framegrid_o[i][j-1]!='1' and self.framegrid_o[i][j-1]!='3':
                        print('    \\draw ({0},{1}) -- ({2},{1});'.format(j-1,i-1,j-1+in_row),end='\n',file=file) 
            
            for j in range(1,self.length_line+1):
                for i in range(1,self.numb_lines+1):
                    in_row = self.in_row_vertical(self.framegrid_o,i,j,0)
                    if in_row > 0 and self.framegrid_o[i-1][j]!='2' and self.framegrid_o[i-1][j]!='3':
                        print('    \\draw ({0},{1}) -- ({0},{2});'.format(j-1,i-1,i-1+in_row),end='\n',file=file)
            
            print('% Pillars',end='\n',file=file)
            
            for i in range(1,self.numb_lines+1):
                for j in range(1,self.length_line+1):
                    if self.framegrid[i][j]=='0':
                        print('    \\fill[green] ({0},{1}) circle(0.2);'.format(j-1,i-1),end='\n',file=file)
            
            
            print('% Inner points in accessible cul-de-sacs',end='\n',file=file)
            
            for i in range(1,self.numb_lines):
                for j in range(1,self.length_line):
                    if self.inac_grid2[i][j]=='C':
                        print('    \\node at ({0},{1}) {{}};'.format(j-0.5,i-0.5),end='\n',file=file)
                        
            
            print('% Entry-exit paths without intersections',end='\n',file=file)
            
            for i in range(1,self.numb_lines):
                for j in range(1,self.length_line):
                    in_row = self.in_row_horizontal_path(self.inner_framegrid,self.inac_grid2,i,j,0,0,0)
                    if in_row[0] > 0:
                        if (self.inac_grid2[i][j-1]=='P' and 'l' in self.inner_framegrid[i][j]) or (in_row[0]==1 and in_row[1]==0 and in_row[2]==0):
                            continue
                        else:
                            print('    \\draw[dashed, yellow] ({0},{1}) -- ({2},{1});'.format(j-0.5-1*in_row[1], i-0.5, j-0.5+in_row[0]-1+1*in_row[2]),end='\n',file=file)
                                       
            for j in range(1,self.length_line):
                for i in range(1,self.numb_lines):
                    in_row = self.in_row_vertical_path(self.inner_framegrid,self.inac_grid2,i,j,0,0,0)
                    if in_row[0] > 0:
                        if (self.inac_grid2[i-1][j]=='P' and 'u' in self.inner_framegrid[i][j]) or (in_row[0]==1 and in_row[1]==0 and in_row[2]==0):
                            continue
                        else:
                            print('    \\draw[dashed, yellow] ({0},{1}) -- ({0},{2});'.format(j-0.5, i-0.5-1*in_row[1], i-0.5+in_row[0]-1+1*in_row[2]),end='\n',file=file)
                        
            
            print('\\end{tikzpicture}\n'
                  '\\end{center}\n'
                  '\\vspace*{\\fill}\n'
                  '\n'
                  '\\end{document}', file=file)
        

        
