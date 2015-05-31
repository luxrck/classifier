from numpy.linalg import norm, eig
from numpy import sign, eye, zeros, copy, matrix, array, multiply, dot
import pdb

class DALMSolver(object):
	def solve(self, A, b, maxiter=1000):
		A = matrix(A)
		b = matrix(b)

		tol = 1e-3
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

class PALMSolver(object):
	def solve(self, A, b, maxiter=1000, maxiter_apg=100):
		A = matrix(A)
		b = matrix(b)

		m, n = A.shape

		tol = 1e-4
		lam = zeros((m, 1), dtype='float64')

		G = A.T * A

		tau = eig(G)[1]
		#pdb.set_trace()
		tauInv = 1 / tau

		niter = 0

		mu = 2 * m / norm(b, 1)
		x = zeros((n, 1), dtype='float64')
		e = b
		pdb.set_trace()
		while niter < maxiter:
			muInv = 1 / mu

			lamScaled = muInv * lam

			e0 = copy(e)
			x0 = copy(x)

			temp2 = b + lamScaled
			temp = temp2 - A * x

			e = multiply(sign(temp), matrix([[max(abs(i) - muInv, 0)] for i in array(temp2)], dtype='float64'))

			converged_apg = 0

			temp1 = A.T * (e - temp2)

			niter_apg = 0
			t1 = 1
			z = x

			muTauInv = muInv * tauInv

			Gx = G * x
			Gz = Gx

			while niter_apg < maxiter_apg:
				xapg0 = copy(x)
				Gx0 = copy(Gx)

				temp = z - tauInv * (temp1 + Gz)

				x = multiply(sign(temp), matrix([[max(abs(i) - muTauInv, 0)] for i in array(temp)], dtype='float64'))
				Gx = G * x

				s = tau * (z - x) + Gx -Gz

				if norm(s, 2) < tol * tau * max(1, norm(x)):
					break

				t2 = (1 + sqrt(1 + 4 * t1 * t1)) / 2
				z = x + ((t1 - 1) / t2) * (x - xapg0)
				Gz = Gx + ((t1 - 1) / t2) * (Gx - Gx0)
				t1 = t2

				niter_apg += 1

			maxiter += niter_apg

			lam += mu * (y - A * x - e)

			if norm(x0 - x, 2) < tol * norm(x0) and norm(e0 - e,  2) < tol * norm(e0):
				break

		return x
