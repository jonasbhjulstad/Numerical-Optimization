import matplotlib.pyplot as plt
from Collocation.collocation_coeffs import collocation_polynomials
import numpy as np
from matplotlib import cm

class collocation_plot(object):
    def __init__(self, x_plot, u_plot, thetas, tgrid):
        self.tgrid = tgrid
        self.tgrid_u = tgrid[:-1]
        self.tf = tgrid[-1]
        self.N = len(tgrid)
        self.iter  = 0
        self.d = 3
        self.x_plot = x_plot
        self.u_plot = u_plot
        self.thetas = thetas
        self.N_iter = thetas.shape[0]
        self.tgrid_poly = []


    def solution_plot(self,x_opt, u_opt):
        tgrid = np.linspace(0, self.tf, self.N + 1)
        tgrid_u = np.linspace(0, self.tf, self.N)

        # Plot the results
        fig, ax = plt.subplots(2,1)

        ax[0].plot(tgrid, x_opt.T, '-.')
        ax[0].set_title("SIR Collocation Optimization")
        ax[1].ticklabel_format(useMathText=True)
        ax[1].step(tgrid_u, u_opt.T, '-')

        ax[0].set_xlabel('time')
        ax[0].legend(['S trajectory', 'I trajectory', 'R trajectory'])
        ax[1].legend(['u trajectory'])
        ax[0].grid()
        plt.show()
        return fig, ax

    def iteration_plot(self, iteration_step, poly_resolution=10, full_plot=False):
        poly_list, tau_root = collocation_polynomials(self.d)
        t_poly = np.linspace(0,1,poly_resolution)
        self.tgrid_poly = [t_poly*(self.tgrid[k+1]-self.tgrid[k]) + self.tgrid[k] for k in range(self.N-1)]
        tgrid_u = np.linspace(0, self.tf, self.N)
        poly_vals = np.array([p(t_poly) for p in poly_list])

        def calc_poly_traj(theta_k):
            S_traj = [theta_k[0,4*i:4*i+(self.d+1)] @ poly_vals for i in range(self.N)]
            I_traj = [theta_k[1,4*i:4*i+(self.d+1)] @ poly_vals for i in range(self.N)]
            R_traj = [theta_k[2,4*i:4*i+(self.d+1)] @ poly_vals for i in range(self.N)]

            return S_traj, I_traj, R_traj


        def theta_plot(theta_k, x_plot, u_plot, axs, color='k', marker='', markersize=3):
            S_traj, I_traj, R_traj = calc_poly_traj(theta_k.values)
            [axs[0].plot(tk, s, color=color) for tk, s in zip(self.tgrid_poly, S_traj)]
            [axs[1].plot(tk, i, color=color) for tk, i in zip(self.tgrid_poly, I_traj)]
            [axs[2].plot(tk, r, color=color) for tk, r in zip(self.tgrid_poly, R_traj)]

            # axs[0].plot(self.tgrid, x_plot.values[0,:-1].T)
            # axs[1].plot(self.tgrid, x_plot.values[1,:-1].T)
            # axs[2].plot(self.tgrid, x_plot.values[2,:-1].T)

            axs[3].plot(tgrid_u, u_plot, color=color)
            if marker != '':
                [axs[0].plot([tk[0], tk[-1]], [s[0], s[-1]], color=color, marker=marker, markersize=markersize) for tk, s in zip(self.tgrid_poly, S_traj)]
                [axs[1].plot([tk[0], tk[-1]], [i[0], i[-1]], color=color, marker=marker, markersize=markersize) for tk, i in zip(self.tgrid_poly, I_traj)]
                [axs[2].plot([tk[0], tk[-1]], [r[0], r[-1]], color=color, marker=marker, markersize=markersize) for tk, r in zip(self.tgrid_poly, R_traj)]
                axs[3].plot([tgrid_u[0], tgrid_u[-1]], [u_plot[0], u_plot[-1]], color=color, marker=markersize, markersize=2.5)


        fig, axs = plt.subplots(4)
        def onclick(event):
            if(self.iter <self.N_iter):
                [ax.clear() for ax in axs]
                theta_plot(self.thetas[self.iter],self.x_plot[self.iter], self.u_plot[self.iter], axs)
                self.iter += iteration_step
        if full_plot:
            iter_steps = np.arange(self.iter, self.N_iter, iteration_step)
            colormap = cm.get_cmap('Greys', len(iter_steps))
            colors = colormap(np.linspace(.1, .8, len(iter_steps)))
            [theta_plot(self.thetas[iter],self.x_plot[iter], self.u_plot[iter], axs, color=colors[i] ) for i, iter in enumerate(iter_steps)]
            theta_plot(self.thetas[-1],self.x_plot[-1], self.u_plot[-1], axs, color=colors[-1], marker='o', markersize=3)
            axs[0].set_ylabel('S')
            axs[1].set_ylabel('I')
            axs[2].set_ylabel('R')
            axs[3].set_ylabel('R0')

            axs[0].set_title('Collocation Multiple-Shooting N = %i, ' % self.N)
            plt.show()
        else:
            fig.canvas.mpl_connect('button_press_event', onclick)
            plt.show()
            plt.draw()

        def cost_plot(self):
            def f_cost(I, u):
                return normalizing_factor*(I**2 + Wu/(u**2))


            I_vec = np.logspace(0,4.2, 7)
            u_vec = np.logspace(-5.2, -3, 7)

            I_min_con_x = np.zeros(I_vec.shape)

            X, Y = np.meshgrid(I_vec, u_vec)
            Z = f_cost(X, Y)

            N_plots = 10

            fig, axs = plt.subplots(5,2)

            for col in axs:
                for ax in col:
                    ax.contour(X, Y, Z)
                    ax.plot([N_pop]*I_vec.shape[0], u_vec)
                    ax.plot(I_vec, [u_min]*I_vec.shape[0])
                    ax.set_yscale('log')
                    ax.set_xscale('log')
            plt.show()
