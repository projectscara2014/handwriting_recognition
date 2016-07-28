from classifier_python.classifier import pure_result
from classifier_python.classifier import classifier


def test_all():
	im = [[0.01] for i in range(400)]
	print(pure_result(im))
test_all()