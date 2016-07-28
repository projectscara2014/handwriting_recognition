import copy
def time_this_function(function) : 
    try : 
        time
    except : 
        import time
    
    def wrapper_function(*args,**kwargs) : 
        start_time = time.time()
        return_value = function(*args,**kwargs)
        elapsed_time = (time.time() - start_time)*1000
        print(function.__name__ + ' -- elapsed_time -- ' + str(elapsed_time) + ' ms\n')
        return return_value
    return wrapper_function

def check_for_predecessor(im2,r,c,black = 0):
    if(r>0):
        prev_row = im2[r-1]
    else:
        return False
    p = []
    for i in range(c-1,c+2):
        if(i>=0 and i<len(prev_row)):
            if(prev_row[i] != black):
                p.append(prev_row[i])
    if(p==[]):
        return False
    else:
        return (p)
    
def check_predecessor2(im2,r,c,black=0):
#     print("checking for "+str(r)+" "+str(c))
    if(r>0):
        prev_row = im2[r-1]
    else:
        return im2
    for i in range(c-1,c+2):
        if(i>=0 and i<len(prev_row)):
            if(prev_row[i] != black):
                im2[r-1][i] = im2[r][c]
    return im2

@time_this_function
def segmentor(im):
    black = 0
    white = 1
    im2 = copy.deepcopy(im)
    count = 2
    l_r = len(im)
    l_c = len(im[0])
#     im3 = []
    for i in range(l_r):
#         im3.append([])
        for j in range(l_c):
#             im3[-1].append([])
            if(im[i][j] != black):
                prev_val = check_for_predecessor(im2,i,j)
                if(prev_val == False):
                    im2[i][j] = count
                    count +=1
#                     count +=50 
                else:
                    im2[i][j] = min(prev_val)
#     print_(im,im2)
#     print("------------")
    for i in range(l_r):
        for j in range(l_c):
            if(im2[l_r-i-1][j] != black):
                im2 = check_predecessor2(im2,l_r-i-1,j)
    print_(im,im2)
#     return im2
    return im2
    
h = segmentor(im)