from PIL import Image
import math
import time



y_sobel_operator = [[-1,-2,-1],
					[ 0, 0, 0],
					[ 1, 2, 1]]


x_sobel_operator = [[-1, 0, 1],
					[-2, 0, 2],
					[-1, 0, 1]]

class Carver(object):
	def __init__(self,imgPath):
		im = Image.open(imgPath)
		self.writablePixels = im.load()
		self.image = im
		width,height = im.size

		pixels = list(im.getdata())
		pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
		objPixels = [[None] * len(pixels[0])] * len(pixels)
		for i in xrange(len(pixels)):
			for j in xrange(len(pixels[0])):
				r,g,b = pixels[i][j]
				objPixels[i][j] = self.Pixel(r,g,b)


		img_object = self.Image_Object(objPixels,self.writablePixels)
		im.save("somepath.png")




	class Pixel(object):
		def __init__(self,r,g,b):
			self.r = r
			self.g = g
			self.b = b

		def set_energy(self,energy):
			self.energy = energy

		def get_grayscale_pixel(self):
			luminance =  (0.2126*self.r + 0.7152*self.g + 0.0722*self.b)
			r,g,b = (luminance,) * 3
			grayscale = self.__class__(r,g,b)
			return grayscale
		def get_pixel_as_tuple(self):
			return (self.r,self.g,self.b)


	class Image_Object(object):

		def __init__(self, arrPixel,writablePixels):
			self.writablePixels = writablePixels
			self.arrPixel = arrPixel
			self.set_energies()


		# This functions sets the energies for each pixel
		# The higher the energy, the less likely this pixel is going
		# to be carved as it is important for the picture.
		def set_energies(self):
			self.energy = [[0]*len(self.arrPixel[0])] * len(self.arrPixel)
			#From i = 0 .. i = height of image
				#From j = 0 .. j = width of image
					# Get a pixel, p, from image, img, by p = img[i,j]	
					# Get the x derivative of p
					# Get the y derivative of p
					# Set the sum of the two derivatives as energy of the pixel [i,j] 
			for i in xrange(len(self.arrPixel)):
				for j in xrange(len(self.arrPixel[i])):
					self.energy[i][j] = self.get_energy(j,i)

		def get_energy(self,x,y):
			x_prime = self.der(x,y,x_sobel_operator)
			y_prime = self.der(x,y,y_sobel_operator)		

			self.writablePixels[x,y] = (int((x_prime + y_prime)),) * 3

			return x_prime + y_prime


		def der(self,x,y,sobel_filter):
			filteredSum = 0
			rgbTuple = [0,0,0]
			for i in xrange(-1,2):
				for j in xrange(-1,2):
					height,width = (len(self.arrPixel),len(self.arrPixel[0]))
					if x + i < 0 or y + j < 0 or y + j >= height or x + i >= width:
						return 0
					filterMultiple = sobel_filter[j+i][i+1]
					currentPixel = self.arrPixel[y + j][x+ i]	
					filteredSum += currentPixel.get_grayscale_pixel().r * filterMultiple

			return filteredSum/9

def main():
	carver  = Carver("valve.png")




if __name__ == '__main__':
	main()
