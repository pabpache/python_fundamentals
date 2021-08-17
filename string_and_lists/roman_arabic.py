#assignment 1
#Student's name: Pablo Pacheco


import sys

try:
    a= input('How can I help you? ').split()
    if len(a)==3:
        if a[0] != 'Please' or a[1] != 'convert' or a[2]==None:
            raise ValueError
    elif len(a)==4:
        if a[0] != 'Please' or a[1] != 'convert' or a[2]==None or a[3] != 'minimally':
            raise ValueError
    elif len(a)==5:
        if a[0] != 'Please' or a[1] != 'convert' or a[2]==None or a[3] != 'using' or a[4] ==None:
            raise ValueError
    else:
        raise ValueError
except ValueError:
    print("I don't get what you want, sorry mate!")
    sys.exit()
            
            
def valid_generalised_roman(x,y):
    gen_roman_sequence = {}

    for i in x:
        if i not in y:
            return False
        
    n_iter=0
    for i in reversed(y):
        n_iter +=1
        if n_iter%2==1 and x.count(i)>4:
            return False
        if n_iter%2==0 and x.count(i)>1:
            return False
            
        
    n_iter=0
    acum=1/2
    y_one=[]
    y_five=[]
    for i in reversed(y):
        n_iter +=1
        acum = int(acum*2)*(n_iter%2) + int(acum*5)*((n_iter+1)%2)
        gen_roman_sequence[i]= acum
        if n_iter%2 == 1:
            y_one.append(i)
        else:
            y_five.append(i)


    prev_sym=gen_roman_sequence[x[0]]
    in_row=1
    min_subs=gen_roman_sequence[y[0]]
    curr_pos=0
     
    for i in x[1:]:
        curr_pos +=1
        if gen_roman_sequence[i]<=min_subs:
           
            if i in y_one:
                if gen_roman_sequence[i]<prev_sym:
                    if i == y[0]:
                        return False
                    else:
                        prev_sym=gen_roman_sequence[i]
                        in_row = 1
                elif gen_roman_sequence[i]==prev_sym:
                    in_row +=1
                    if in_row>3:
                        return False
                    else:
                        prev_sym=gen_roman_sequence[i]
                else:
                    if len(x)>curr_pos+1:
                        if x[curr_pos+1]==x[curr_pos-1]:
                            return False

                    if gen_roman_sequence[i]>10*prev_sym or x[curr_pos-1] in y_five:
                        return False
                    elif in_row > 1:
                        return False
                    else:
                        min_subs=prev_sym
                        prev_sym=gen_roman_sequence[i]
                        in_row=1 


            elif i in y_five:
                if gen_roman_sequence[i] < prev_sym:
                    prev_sym=gen_roman_sequence[i]
                    in_row=1
                elif gen_roman_sequence[i] > prev_sym:
                    if len(x)>curr_pos+1:
                        if x[curr_pos+1]==x[curr_pos-1]:
                            return False
                    if gen_roman_sequence[i]>10*prev_sym or x[curr_pos-1] in y_five:
                        return False
                    elif in_row>1:
                        return False
                    else:
                        min_subs=prev_sym
                        prev_sym=gen_roman_sequence[i]
                        in_row=1
                else:
                    return False
            else:
                return False
        else:
            return False
    

    return True
        

def distinct_sequence(x):
    for i in x:
        if x.count(i)>1:
            return False

    return True
        
        
def gen_roman_to_arabic(x,y):
    gen_roman_sequence={}

    n_iter=0
    acum=1/2
    for i in reversed(y):
        n_iter +=1
        acum = int(acum*2)*(n_iter%2) + int(acum*5)*((n_iter+1)%2)
        gen_roman_sequence[i]= acum

    
    prev_value=gen_roman_sequence[x[0]]
    total= prev_value
    for i in x[1:]:
        if gen_roman_sequence[i] <= prev_value:
            total= total+gen_roman_sequence[i]
            prev_value=gen_roman_sequence[i]
        else:
            total= total + gen_roman_sequence[i] - 2*prev_value
            prev_value=gen_roman_sequence[i]

    return total

def max_arabic_numb(x):
    gen_roman_sequence={}
    n_iter=0
    acum=1/2
    for i in reversed(x):
        n_iter +=1
        acum = int(acum*2)*(n_iter%2) + int(acum*5)*((n_iter+1)%2)
        gen_roman_sequence[i]= acum

    if len(x)%2==1:
        return gen_roman_sequence[x[0]]*4-1
    else:
        return gen_roman_sequence[x[0]] + gen_roman_sequence[x[1]]*4-1
    

def arabic_to_gen_roman(x,y):
    arabic_gen_roman={}

    n_iter=0
    acum=1/2
    for i in reversed(y):
        n_iter +=1
        acum = int(acum*2)*(n_iter%2) + int(acum*5)*((n_iter+1)%2)
        arabic_gen_roman[acum]= i

    n_iter=0
    total=''
    for i in reversed(x):
        n_iter +=1
        min_unit= 10**(n_iter-1)
        max_unit= 10**n_iter
        curr_numb=int(i)
        if curr_numb==9:
            total= arabic_gen_roman[min_unit] + arabic_gen_roman[max_unit] + total
        elif curr_numb >= 5:
            total = (curr_numb // 5)*arabic_gen_roman[min_unit * 5] + (curr_numb % 5)*arabic_gen_roman[min_unit] + total
        elif curr_numb==4:
            total = arabic_gen_roman[min_unit] + arabic_gen_roman[min_unit*5] + total
        else:
            total= curr_numb*arabic_gen_roman[min_unit] + total

    return total


def cal_minimal(x):
    for i in x:
        if x.count(i)>4:
            return False

    sequence={x[-1]:1}
    n_iter=1
    acum=1
    curr_pos=-1
    in_row=1
   
    for i in reversed(x[:-1]):
        n_iter +=1
        curr_pos -=1
        acum = int(acum*2)*(n_iter%2) + int(acum*5)*((n_iter+1)%2)

        #Type 1
        if n_iter%2 ==1:
            if i not in x[curr_pos +1:]:
                sequence[i]=acum
                in_row=1
            else:
                
                if len(x[curr_pos+1:])>2:
                    if i == x[curr_pos +2] and i==x[curr_pos+3]:
                        return False
                if i== x[curr_pos + 1]:
                    in_row +=1
                    if in_row >3:
                        return False
                    else:
                        if acum//2 == sequence[x[curr_pos+1]]:
                            sequence[x[curr_pos+1]]=acum
                        else:
                            n_iter -=1
                            acum = acum//2

                if len(x[curr_pos+1:])>3:
                    if i in x[curr_pos +4:] and in_row != 3:
                        return False
    
                if len(x[curr_pos+1:])>1 and i != x[curr_pos +1]:
                    if i == x[curr_pos + 2]:
                        if len(x[curr_pos+1:])>2:
                            if x[curr_pos+1]==x[curr_pos+3]:
                                return False
                        else:
                            sequence[x[curr_pos+2]]=acum
                            sequence[x[curr_pos+1]]=acum//10
                            in_row=1
                            
                if len(x[curr_pos + 1:])>2 and i != x[curr_pos +1] and i != x[curr_pos +2]:
                    if i == x[curr_pos + 3]:
                        if x[curr_pos+1]== x[curr_pos+2]:
                            return False
                        if x[:curr_pos].count(x[curr_pos+2])>0:
                            return False
                        if len(x[curr_pos + 1:])>3:
                            if x[curr_pos+2] == x[curr_pos+4]:
                                return False
                        sequence[x[curr_pos+3]]= acum
                        sequence[x[curr_pos+2]]=acum//10
                        sequence[x[curr_pos+1]]=acum*5
                        in_row=1  
                
        #type 5 
        else:
            if i not in x[curr_pos +1:]:
                if in_row < 2 and x.count(x[curr_pos+1]) < 2 and x.count(i)==1:
                    if acum//5 == sequence[x[curr_pos+1]]:
                        sequence[i]=sequence[x[curr_pos+1]]
                        sequence[x[curr_pos+1]]=acum
                        in_row=1
                else:
                    sequence[i]=acum
                    in_row=1

            else:
                    
                if len(x[curr_pos+1:])>2:
                    if i == x[curr_pos +2] and i==x[curr_pos+3]:
                        return False

                if i == x[curr_pos +1]:
                    in_row +=1
                    if in_row > 3:
                        return False
                    else:
                        n_iter -=1
                        acum = acum//5

                if len(x[curr_pos+1:])>3:
                    if i in x[curr_pos +4:] and in_row != 3:
                        return False

                if len(x[curr_pos+1:])>1:
                    if i == x[curr_pos + 2] and i != x[curr_pos +1]:
                        if len(x[curr_pos+1:])>2:
                            if x[curr_pos+1]==x[curr_pos+3]:
                                return False
                        else:
                            sequence[x[curr_pos + 2]]= acum*2
                            sequence[x[curr_pos +1]]= (acum*2)//10
                            in_row=1
                if len(x[curr_pos + 1:])>2:
                    if i == x[curr_pos + 3] and i != x[curr_pos+1] and i != x[curr_pos+2]:
                        if x[curr_pos+1]== x[curr_pos+2]:
                            return False
                        if x[:curr_pos].count(x[curr_pos+2])>0:
                            return False
                        if len(x[curr_pos + 1:])>3:
                            if x[curr_pos+2] == x[curr_pos+4]:
                                return False
                        sequence[x[curr_pos+3]]=acum//5
                        sequence[x[curr_pos+2]]= (acum//5)//10
                        sequence[x[curr_pos+1]]=acum
                        in_row=1


    prev_value = sequence[x[0]]
    total= prev_value
    for i in x[1:]:
        if sequence[i] <= prev_value:
            total= total+sequence[i]
            prev_value= sequence[i]
        else:
            total= total + sequence[i] - 2*prev_value
            prev_value=sequence[i]
                

    n_iter=0
    acum=1/2
    sequence_def=''
    while acum < sorted(sequence.values())[-1]:
        n_iter +=1
        acum = int(acum*2)*(n_iter%2) + int(acum*5)*((n_iter+1)%2)
        for i in sequence.keys():
            if acum in sequence.values():
                if sequence[i]==acum:
                    sequence_def= i + sequence_def
                    break
            else:
                sequence_def= '_' + sequence_def
                break
                
        
                    
    return [sequence_def,total]
                      

        
if len(a)==3:
    if valid_generalised_roman(a[2],'MDCLXVI'):
        print('Sure! It is',gen_roman_to_arabic(a[2],'MDCLXVI'))

    else:
        if a[2][0]=='0':
            print("Hey, ask me something that's not impossible to do!")
            sys.exit()

        try:
            b=int(a[2])
        except ValueError:
            print("Hey, ask me something that's not impossible to do!")
            sys.exit()

        if 0< b < 4000:
            print('Sure! It is',arabic_to_gen_roman(a[2],'MDCLXVI'))
        else:
            print("Hey, ask me something that's not impossible to do!")
            sys.exit()
    
    
elif len(a)==5:
    if not a[4].isalpha() or not distinct_sequence(a[4]):
        print("Hey, ask me something that's not impossible to do!")
        sys.exit()
    
    if valid_generalised_roman(a[2],a[4]):
        print('Sure! It is',gen_roman_to_arabic(a[2],a[4]))

    else:
        if a[2][0]=='0':
            print("Hey, ask me something that's not impossible to do!")
            sys.exit()

        try:
            b=int(a[2])
        except ValueError:
            print("Hey, ask me something that's not impossible to do!")
            sys.exit()

        max_limit = max_arabic_numb(a[4])

        if 0< b <= max_limit:
            print('Sure! It is',arabic_to_gen_roman(a[2],a[4]))
        else:
            print("Hey, ask me something that's not impossible to do!")
            sys.exit()

        
elif len(a)==4:
    if not a[2].isalpha():
        print("Hey, ask me something that's not impossible to do!")
        sys.exit()

    if cal_minimal(a[2]) != False:

        sequen, minimal = cal_minimal(a[2])
        print('Sure! It is', minimal,'using',sequen)
    else:
        print("Hey, ask me something that's not impossible to do!")
        sys.exit()











