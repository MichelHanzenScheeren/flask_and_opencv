import numpy

image = numpy.array([[[255, 254, 253], [252, 251, 250]], [[249, 248, 247], [246, 245, 244]]])
print(image, end='\n****\n')

div = 4
quantized = image // div * div + div // 2
print(quantized)
