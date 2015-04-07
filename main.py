from PIL import Image
import math
import time
import pprint
import sys

mini = False

x_sobel_operator = [[-3,0,3],
                    [-10,0,10],
                    [-3,0,3]]

y_sobel_operator = [[-3,-10,-3],
                    [0,0,0],
                    [3,10,3]]

class Carver(object):
	def __init__(self,imgPath):
		im = Image.open(imgPath)
		self.writablePixels = im.load()
		self.image = im
		width,height = im.size
		pixels = [[(0,0,0) for _ in xrange(height)] for x in xrange(width)]
		for x in xrange(width):
			for y in xrange(height):
				pixels[x][y] = self.writablePixels[x,y]
		img_object = self.Image_Object(pixels,self.writablePixels,im)
		im.save("somepath.png")
		im.show()




	class Pixel(object):
		def __init__(self,r,g,b):
			self.r = r
			self.g = g
			self.b = b

		def set_energy(self,energy):
			self.energy = energy

		def get_pixel_as_tuple(self):
			return (self.r,self.g,self.b)


	class Image_Object(object):

		def get_grayscale_pixel(self,r,g,b):
			luminance =  (0.2126*r + 0.7152*g + 0.0722*b)
			return (luminance,) * 3
		def __init__(self, arrPixel, writablePixels,im):
			self.image = im
			self.writablePixels = writablePixels
			self.arrPixel = arrPixel
			self.set_energies()
			# self.energy = [[4,5,6],
			# 			   [3,3,1],
			# 			   [1,2,2]]
			#431 843 10,4,5


			self.build_costs()
			# print self.costs
			minimum_index = self.find_lowest_cost_index()
			for x in xrange(len(self.costs)):
				self.draw_path(x,len(self.costs[0]) - 1)

		def draw_path(self,x,y):
			global mini
			top_right = 9999999999999999999999999999999999999
			top_left =  9999999999999999999999999999999999999
			top =       9999999999999999999999999999999999999
			if y == 0:
				return
			
			self.writablePixels[x,y] = (255,0,0)
			# print str((x,y))
			if x != len(self.costs) - 1:
				top_right = self.costs[x + 1][y - 1]
			if x != 0:
				top_left = self.costs[x - 1][y - 1]
			top = self.costs[x][y - 1]

			values = [top,top_right,top_left]
			if not mini:
				print max(values)
				mini = True

			min_index = values.index(min(values))
			if min_index == 0:
				self.draw_path(x,y-1)
			elif min_index == 1:
				self.draw_path(x + 1, y - 1)
			elif min_index == 2:
				self.draw_path(x - 1, y - 1)


		# This functions sets the energies for each pixel
		# The higher the energy, the less likely this pixel is going
		# to be carved as it is important for the picture.
		def set_energies(self):
			# print self.energy
			#From i = 0 .. i = height of image
				#From j = 0 .. j = width of image
					# Get a pixel, p, from image, img, by p = img[i,j]	
					# Get the x derivative of p
					# Get the y derivative of p
					# Set the sum of the two derivatives as energy of the pixel [i,j] 
			self.energy = [[self.get_energy(i,j) for j in xrange(len(self.arrPixel[0]))] for i in xrange(len(self.arrPixel))]

		def find_lowest_cost_index(self):
			bottom_costs = list()
			y = len(self.costs[0]) - 1
			for x in xrange(len(self.costs)):
				bottom_costs.append(self.costs[x][y])
			return bottom_costs.index(min(bottom_costs))


		def build_costs(self):
			self.costs= [[0 for y in xrange(len(self.energy[0]))] for x in xrange(len(self.energy))]
			self.someCosts = self.costs;
			# print self.costs 
			for y in xrange(0,len(self.energy[0]) - 1):
				for x in xrange(0,len(self.energy)):
					if y == 0:
						self.costs[x][y] = self.energy[x][y]
						#print str(self.costs[x][y])

					# All the way to the right
					if x != len(self.energy) -1 :
						if self.costs[x + 1][y + 1] == 0:
							self.costs[x + 1][y + 1] = self.costs[x][y] + self.energy[x + 1][y + 1]
						else:
							if self.costs[x + 1][y + 1] > self.costs[x][y] + self.energy[x + 1][y + 1]:
								self.costs[x + 1][y + 1] = self.costs[x][y] + self.energy[x + 1][y + 1]
					if x != 0:
						if self.costs[x - 1][y + 1] == 0:
							self.costs[x - 1][y + 1] = self.costs[x][y] + self.energy[x - 1][y + 1]
						else:
							if self.costs[x - 1][y + 1] > self.costs[x][y] + self.energy[x - 1][y + 1]:
								self.costs[x - 1][y + 1] = self.costs[x][y] + self.energy[x - 1][y + 1]
					if self.costs[x][y + 1] == 0:
						self.costs[x][y + 1] = self.costs[x][y] + self.energy[x][y + 1]
					else:
						if self.costs[x][y + 1] > self.costs[x][y] + self.energy[x][y + 1]:
							self.costs[x][y + 1] = self.costs[x][y] + self.energy[x][y + 1]
					# if self.costs[8][107] == 0:
					# 	# print str((x,y))
					# 	pass
					# print self.costs[8][107]


				# if x == len(self.energy) - 1:
				# 	print self.costs[8][107]
				# 	self.someCosts = self.costs








		def is_on_edge(x,y):
			return x == len(self.energy) or y == len(self.energy[0]) or x == 0



		def get_energy(self,x,y):
			x_prime = self.der(x,y,x_sobel_operator) ** 2
			y_prime = self.der(x,y,y_sobel_operator) ** 2

			result = int(math.sqrt(x_prime + y_prime))
			if result > 255:
				result = 255
			if result < 0:
				result = 0

			self.writablePixels[x,y] = (result,)*3
			return result


		def der(self,x,y,sobel_filter):
			filteredSum = 0
			rgbTuple = [0,0,0]
			for i in xrange(-1,2):
				for j in xrange(-1,2):
					width,height= (len(self.arrPixel),len(self.arrPixel[0]))
					if x + i < 0 or y + j < 0 or y + j >= height or x + i >= width:
						continue
					filterMultiple = sobel_filter[j+i][i+1]
					currentPixel = self.arrPixel[x + i][y+ j]	
					r,g,b = currentPixel
					filteredSum += self.get_grayscale_pixel(r,g,b)[0] * filterMultiple

			return filteredSum/9

def main():
	sys.setrecursionlimit(10000)
	carver  = Carver("waterfall.png")




if __name__ == '__main__':
	main()









