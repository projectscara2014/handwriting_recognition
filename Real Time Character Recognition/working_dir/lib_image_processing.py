"""
    This script is a 'utils' script which basically allows the usage of image_processing functions implemented in C.
    These functions are accessed via C-python binding which requires this script.
"""
import ctypes
import numpy

shared_object_library_name = "image_processing.dll"

_image_processing_ = ctypes.cdll.LoadLibrary(shared_object_library_name)

#Python class for defining 2dimensional array type as required by Ctypes library
class two_d_array() : 
    
    def from_param(self,param) : 
        typename = type(param).__name__
        if hasattr(self,'from_'+typename) : 
            return getattr(self,'from_'+typename)(param)
        elif isinstance(param,ctypes.Array) : 
            
            return param
        else : 
            raise TypeError('type {0} not supported'.format(typename))
    
    def from_ndarray(self,param) : 
        c_array = numpy.ascontiguousarray(param,dtype=numpy.int32)
        pointer = c_array.ctypes
        return pointer
    
    def from_list(self,param) : 
        return self.from_ndarray(param)
    
    def from_tuple(self,param) : 
        return self.from_ndarray(param)
    
two_d_array_ = two_d_array()

'''-----------------------------------------------------------------------
------------------------------ CONVOLUTION -------------------------------
-----------------------------------------------------------------------'''

#defining argtypes and restypes for _image_processing_.convolution function
_image_processing_.convolution.argtypes = [two_d_array_,two_d_array_,\
two_d_array_,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int]
_image_processing_.convolution.restype = ctypes.c_void_p

def convolution(image,kernel,convert_to_uint8=False) :

    #----------------------- VARIABLE DECLARATIONS ---------------------
    image_height = len(image)
    image_width = len(image[0])
    kernel_normalizer = kernel[0]
    kernel = kernel[1] 
    #---------------------------------------------------------------------

    #generate a new ctypes array and convert it into a numpy array
    return_c_array = numpy.ctypeslib.as_array(((ctypes.c_int*image_width)*image_height)())
    #generate a contiguous aray in memory for the image and the kernel
    image_c_array = numpy.ascontiguousarray(image,dtype=numpy.int32)
    kernel_c_array = numpy.ascontiguousarray(kernel,dtype=numpy.int32)
    
    #calling the _image_processing_.convolution function and passing appropriate parameters
    _image_processing_.convolution(image_c_array,return_c_array,kernel_c_array,\
        len(image[0]),len(image),len(kernel),kernel_normalizer)

    if convert_to_uint8 : 
        return numpy.ascontiguousarray(return_c_array,dtype=numpy.uint8)
    else :
        return numpy.ascontiguousarray(return_c_array,dtype=numpy.int32)

'''--------------------------------------------------------------------'''


'''-----------------------------------------------------------------------
----------------------------- SOBEL OPERATOR -----------------------------
-----------------------------------------------------------------------'''

_image_processing_.sobel_operator.argtypes = [two_d_array_,two_d_array_,\
    two_d_array_,ctypes.c_int,ctypes.c_int]
_image_processing_.sobel_operator.restypes = ctypes.c_void_p

def sobel_operator(image) : 

    #----------------------- VARIABLE DECLARATIONS ---------------------
    image_height = len(image)
    image_width = len(image[0])
    #---------------------------------------------------------------------

    #generate new ctypes arrays for grad_x and grad_y
    generate_c_array = (ctypes.c_int*image_width)*image_height
    magnitude = numpy.ctypeslib.as_array(generate_c_array())
    angle = numpy.ctypeslib.as_array(generate_c_array())

    #generate a contiguous array in memory for the image
    image_c_array = numpy.ascontiguousarray(image,dtype=numpy.uint8)

    #calling the _image_processing_.sobel function and passing appropriate parameters
    _image_processing_.sobel_operator(image_c_array,magnitude,angle,\
        image_width,image_height)

    return [magnitude,angle]

'''--------------------------------------------------------------------'''



'''-----------------------------------------------------------------------
------------------------- NON MAXIMUM SUPRESSION -------------------------
-----------------------------------------------------------------------'''

_image_processing_.non_maximum_supression.argtypes = [two_d_array_,\
    two_d_array_,two_d_array_,ctypes.c_int,ctypes.c_int]
_image_processing_.non_maximum_supression.restypes = ctypes.c_void_p

def non_maximum_supression(magnitude,angle) :
    
    #----------------- VARIABLE DECLARATIONS -------------------
    image_height = len(magnitude)
    image_width = len(magnitude[0])
    #-----------------------------------------------------------

    magnitude_c_array = numpy.ascontiguousarray(magnitude,dtype=numpy.int32)
    angle_c_array = numpy.ascontiguousarray(angle,dtype=numpy.int32)
    return_image_c_array = numpy.ctypeslib.as_array(((ctypes.c_int*image_width)*image_height)())

    _image_processing_.non_maximum_supression(magnitude_c_array,angle_c_array,return_image_c_array,image_width,image_height)

    return return_image_c_array

'''---------------------------------------------------------------------'''


'''-----------------------------------------------------------------------
--------------------------- IMAGE THRESHOLDING ---------------------------
-----------------------------------------------------------------------'''
_image_processing_.threshold.argtypes = [two_d_array_,ctypes.c_int,ctypes.c_int,ctypes.c_int]
_image_processing_.threshold.restypes = ctypes.c_void_p

def threshold(image,threshold=127) : 
    image_height = len(image)
    image_width = len(image[0])

    image_c_array = numpy.ascontiguousarray(image,dtype=numpy.int32)

    _image_processing_.threshold(image_c_array,threshold,image_width,image_height)

    return image_c_array

''' ----------------------------------------------------------------------------------- '''

_image_processing_.threshold2.argtypes = [two_d_array_,ctypes.c_int,ctypes.c_int,ctypes.c_int]
_image_processing_.threshold2.restypes = ctypes.c_void_p

def threshold2(image,threshold=127) : 
    image_height = len(image)
    image_width = len(image[0])

    # image = numpy.reshape(image,(image_height,image_width*3))

    image_c_array = numpy.ascontiguousarray(image,dtype=numpy.int32)

    _image_processing_.threshold2(image_c_array,threshold,image_width,image_height)
    return numpy.ascontiguousarray(image_c_array,dtype=numpy.uint8)
    # return image_c_array

''' ----------------------------------------------------------------------------------- '''

_image_processing_.threshold3.argtypes = [two_d_array_,two_d_array_,ctypes.c_int,ctypes.c_int,ctypes.c_int]
_image_processing_.threshold3.restypes = ctypes.c_void_p

def threshold3(image,threshold=127) : 
    image_height = len(image)
    image_width = len(image[0])
    ret_im = numpy.zeros((image_height,image_width))

    # image = numpy.reshape(image,(image_height,image_width*3))
    # return_c_array = numpy.ctypeslib.as_array((((ctypes.c_int)*image_width)*image_height)())

    image_c_array = numpy.ascontiguousarray(image,dtype=numpy.int32)
    return_c_array = numpy.ascontiguousarray(ret_im,dtype=numpy.int32)

    _image_processing_.threshold3(image_c_array,return_c_array,threshold,image_width,image_height)
    return numpy.ascontiguousarray(return_c_array,dtype=numpy.uint8)
    # return image_c_array

''' ----------------------------------------------------------------------------------- '''

#defining argtypes and restypes for _image_processing_.convolution function
_image_processing_.convolution2.argtypes = [two_d_array_,two_d_array_,\
two_d_array_,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int]
_image_processing_.convolution2.restype = ctypes.c_void_p

def convolution2(image,kernel,convert_to_uint8=False) :

    #----------------------- VARIABLE DECLARATIONS ---------------------
    image_height = len(image)
    image_width = len(image[0])
    kernel_normalizer = kernel[0]
    kernel = kernel[1] 
    #---------------------------------------------------------------------

    #generate a new ctypes array and convert it into a numpy array
    return_c_array = numpy.ctypeslib.as_array((((ctypes.c_int*3)*image_width)*image_height)())
    #generate a contiguous aray in memory for the image and the kernel
    image_c_array = numpy.ascontiguousarray(image,dtype=numpy.int32)
    kernel_c_array = numpy.ascontiguousarray(kernel,dtype=numpy.int32)
    
    #calling the _image_processing_.convolution function and passing appropriate parameters
    _image_processing_.convolution(image_c_array,return_c_array,kernel_c_array,\
        len(image[0]),len(image),len(kernel),kernel_normalizer)

    if convert_to_uint8 : 
        return numpy.ascontiguousarray(return_c_array,dtype=numpy.uint8)
    else :
        return numpy.ascontiguousarray(return_c_array,dtype=numpy.int32)

def dilation(image,iterations=2):
    kernel = [9,[[1,1,1],[1,1,1],[1,1,1]]]
    # print(image.shape)
    # for i in range(iterations):
    image = convolution2(image,kernel,convert_to_uint8 = True)
    # print(image.shape)
    return image