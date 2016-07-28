im = [[0,1,1,0,0,0,1],[0,1,1,1,0,0,1],[0,0,1,0,0,1,0],[0,0,0,0,0,0,1],[1,0,1,0,1,0,1],[0,0,1,1,0,0,1],[0,1,0,0,0,1,0],[0,0,1,1,1,0,0]]
def print_(im,im2=None):
    for i in range(len(im)):
        if(im2 == None): print im[i]
        else: print(str(im[i]) + "        " + str(im2[i]))

print_(im)
def get_bool(r,c):
	global l_r,l_c
	if(r<0 or c<0 or r>l_r or c>l_c):
		return False
	else:
		return True

def segmentor(im):
	global l_r,l_c
	global black,white
	black = 0
	white = 1
	count = 3
	l_r = len(im)
	l_c = len(im[0])
	for i in range(l_r):
		for j in range(l_c):
			if(im[i][j] == white):
				# print("i = "+str(i)+" j = "+str(j))
				im = check_surroundings(im,i,j)
	return im

def check_surroundings(im,r,c):
	global black,white
	if(get_bool(r,c-1)):
		if(im[r][c-1] == white):
			im[r][c] = min_(im[r][c],im[r][c-1])
	if(get_bool(r-1,c-1)):
		pass
	if(get_bool(r-1,c)):
		pass
	if(get_bool(r-1,c+1)):
		pass	
	return im

def min_(a,b):
	if(a>b):
		return b
	return a

print("-----------")
print_(segmentor(im))