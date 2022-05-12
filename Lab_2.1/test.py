import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def plot_3d(x_, y_, z_, labels=['X', 'Y', 'Z']):
  fig = plt.figure(figsize=[18, 10])
  ax = fig.add_subplot(projection='3d')
  ax.plot(x_, y_, z_, label='solution')
  ax.set_xlabel(labels[0], fontsize=15)
  ax.set_ylabel(labels[1], fontsize=15)
  ax.set_zlabel(labels[2], fontsize=15)
  plt.draw()
  plt.show()

def diff_v5(func, h, x, xid=0):
      h_vec = np.zeros(len(x))
      h_vec[xid] = h
      return 3 * (func(x + h_vec) - func(x - h_vec)) / (2 * 2 * h) - 3 * (func(x + 2 * h_vec) - func(x - 2 * h_vec)) / (
                  5 * 4 * h) + 1 * (func(x + 3 * h_vec) - func(x - 3 * h_vec)) / (10 * 6 * h)

  # численное получение якобиана функции F в точке x
def calc_jacobian(F, x):
      h = 10 ** -5
      N = len(x)
      res = np.zeros([N, N])
      for fid in range(0, N):
          for xid in range(0, N):
              func = lambda x: F(x)[fid]
              res[fid, xid] = diff_v5(func, h, x, xid)

      return res

  # решение нелинейного уравнения методом Ньютона
def solve(func, x0, eps=10 ** -4):
      sol = x0
      iter_counter = 0
      J = calc_jacobian(func, sol)
      J = np.linalg.inv(J)
      # Для визуалтзации в полне хватает 10 итераций
      # Проверка на невязку убрана в целях повышения производительности
      while (iter_counter < 10):
          F = np.matrix(func(sol))

          sol = np.array((np.matrix(sol).T - J * F.T).T)[0]
          iter_counter += 1
      return sol

class RungeKutta:
      # matr - матрица метода РК. Матрица состоит из первого столбца - 'С', последней строки - 'в' и все остальное - 'а'
      # t0 - начальное время
      # Y0 - начальные условия
      # F - правая часть системы
      def __init__(self, matr, t0, Y0, F):
          # коэффициенты из матрицы метода
          self.S = len(matr) - 1
          self.C = matr[:self.S, 0].T.tolist()[0]
          self.B = matr[self.S, 1:].tolist()[0]
          self.A = matr[:self.S, 1:]
          self.explicit = RungeKutta.isExplicit(matr)
          # текущее решение (равно начальному)
          self.Y = Y0
          self.DY = F(t0, Y0)
          # текущее время
          self.t = t0
          # правая часть системы
          self.F = F
          # сохраненный след
          self.y_trace = []
          self.dy_trace = []
          for i in range(0, len(self.Y)):
              self.y_trace.append([])
              self.dy_trace.append([])
          self.t_trace = []

          self.SaveTrace()

      # Возвращает True, если matr определяет явный метод РК
      # Иначе False
      def isExplicit(matr):
          N = len(matr)
          for l in range(0, N):
              for c in range(l + 1, N):
                  if matr[l, c] != 0:
                      return False
          return True

      # dt - шаг
      # explicit - Возможно явно указать какой метод использовать
      def NextStep(self, dt, explicit=None):
          if dt < 0:
              return;
          tmp_exl = self.explicit
          if explicit is True or explicit is False:
              tmp_exl = explicit

          if tmp_exl:
              self.ExplicitNextStep(dt)
          else:
              self.ImplicitNextStep2(dt)

          self.t += dt
          self.DY = self.F(self.t, self.Y)
          self.SaveTrace()


      # решение неявным методом
      def ImplicitNextStep(self, dt):
          if dt < 0:
              return
          # Equation = lambda y_np1, dt, t, y_n: y_np1 - dt * np.copy(self.F(t, y_np1)) - y_n
          # self.Y = optimize.fsolve(Equation, x0=np.copy(self.Y), args=(dt, self.t, np.copy(self.Y)))

          ## произошло импортозамещение
          Equation = lambda y_np1: y_np1 - dt * np.copy(self.F(self.t, y_np1)) - np.copy(self.Y)
          self.Y = solve(Equation, x0=np.copy(self.Y))

      def ImplicitNextStep2(self, dt):
          if dt < 0:
              return

          def Equation(ksi):
              ksi1 = np.array(ksi[0:3])
              ksi2 = np.array(ksi[3:6])

              res1 = self.F(self.t, self.Y + dt * self.A[0, 0] * ksi1 + dt * self.A[0, 1] * ksi2) - ksi1
              res2 = self.F(self.t, self.Y + dt * self.A[1, 0] * ksi1 + dt * self.A[1, 1] * ksi2) - ksi2

              return np.append(res1, res2)

          ksi = optimize.fsolve(Equation, x0=np.zeros([6]))
          ksi1 = np.array(ksi[0:3])
          ksi2 = np.array(ksi[3:6])

          self.Y = self.Y + dt * (self.B[0] * ksi1 + self.B[1] * ksi2)

      # запустить сразу несколько стадин с одинаковым шагом
      def start(self, step, t_end, explicit=None):
          arr = np.arange(self.t, t_end + step, step)
          n = len(arr)

          for i in range(1, n):
              self.NextStep(step, explicit=explicit)

      # сохраняет текущие Y, DY и t в историю (trace)
      def SaveTrace(self):
          for i in range(0, len(self.Y)):
              (self.y_trace[i]).append(self.Y[i])

          for i in range(0, len(self.Y)):
              (self.dy_trace[i]).append(self.DY[i])

          self.t_trace.append(self.t)



# концентрация веществ A, B и C
Y0 = [1., 0., 0.]
# скорости реакции
K = [0.04, 3*10**7, 10**4]
# интервал решения
T_end = 0.3

# система дифференциальных уравнений
def dy1_(y1, y2, y3):
  return -K[0]*y1 + K[2]*y2*y3
def dy2_(y1, y2, y3):
  return K[0]*y1 - K[2]*y2*y3 - K[1]*y2**2
def dy3_(y1, y2, y3):
  return K[1]*y2**2

def F_10(t, u):
  y1 = dy1_(u[0], u[1], u[2])
  y2 = dy2_(u[0], u[1], u[2])
  y3 = dy3_(u[0], u[1], u[2])
  return [y1, y2, y3]

# таблица Бутчера
matr = np.matrix([
                  [1/2, 1/2, 0],
                  [3/2, -1/2, 2],
                  [0, 1, 0]
])

rk3 = RungeKutta(matr, 0, Y0, F_10)
rk3.start(0.00003, T_end, explicit=False)
plot_3d(rk3.t_trace, rk3.y_trace[1], rk3.y_trace[0], labels=['t', 'y2', 'y1'])
plot_3d(rk3.t_trace, rk3.y_trace[0], rk3.y_trace[1], labels=['t', 'y1', 'y2'])
plot_3d(rk3.t_trace, rk3.y_trace[0], rk3.y_trace[2], labels=['t', 'y1', 'y3'])

plot_3d(rk3.t_trace, rk3.y_trace[0], rk3.dy_trace[0], labels=['t', 'y1', 'dy1'])
plot_3d(rk3.t_trace, rk3.y_trace[1], rk3.dy_trace[1], labels=['t', 'y2', 'dy2'])
plot_3d(rk3.t_trace, rk3.y_trace[2], rk3.dy_trace[2], labels=['t', 'y3', 'dy3'])