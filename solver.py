from numpy.linalg import norm
from numpy import sign, eye, zeros, copy, matrix, array, multiply, dot
import pdb

class DALMSolver(object):
	def solve(self, A, b, maxiter=1000):
		A = matrix(A)
		b = matrix(b)

		tol = 1e-8
		lam = 1e-1
		m, n = A.shape
		beta = norm(b, 1) / m
		
		x = zeros((n, 1), dtype='float64')
		y = zeros((m, 1), dtype='float64')
		z = zeros((m+n, 1), dtype='float64')
		#pdb.set_trace()		
		Aty = A.T * y
		niter = 0
		while niter < maxiter:
			#print("=== iter: %d ==="%niter)
			x0 = copy(x)
			#pdb.set_trace()
			t = Aty + x / beta
			z = multiply(sign(t), matrix([[min(1, abs(i[0]))] for i in array(t)], dtype='float64'))
			g = lam * y - b + A * (beta * (Aty - z) + x)
			#pdb.set_trace()

			Atg = A.T * g
			a = g.T * g / (lam * g.T * g + beta * Atg.T * Atg)
			#pdb.set_trace()

			y = y - multiply(a, g)
			#y = (1 / (A * A.T)) * (A * z - (A * x - b) / beta)
			#pdb.set_trace()
			Aty = A.T * y
			x = x - beta * (z - Aty)
			#pdb.set_trace()

			if norm(x0 - x, 2) < tol * norm(x0, 2):
				break
			niter += 1
		#pdb.set_trace()
		return x