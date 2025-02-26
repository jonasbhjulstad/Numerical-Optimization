import numpy as np
import pickle as pck
import pandas as pd
import matplotlib.pyplot as plt
from Autodiff_SIR_Sensitivity import Autodiff_SIR_Sensitivity
from Variational_SIR_Sensitivity import Variational_SIR_Sensitivity
from matplotlib import cm
from Parameters.ODE_initial import *
from tqdm import tqdm

if __name__ == '__main__':
    dts = np.flip(np.linspace(0.01,15,5))
    dfs_auto = []
    dfs_var = []
    # dt = 1e-4
    # dts = [1e-3, 5e-4, 1e-4]
    auto = True
    var = True

    for dt in tqdm(dts):
        if auto:
            dfs_auto.append(Autodiff_SIR_Sensitivity(dt, stop=T))
        if var:
            dfs_var.append(Variational_SIR_Sensitivity(dt, stop = T))
    df_plot_list = []
    df_plot_list.append(dfs_auto)
    df_plot_list.append(dfs_var)
    diff_list = []
    for df_var in dfs_var:
        locs = [dfs_auto[-1].index.get_loc(ind, method='nearest') for ind in df_var.index]
        df_auto = dfs_auto[-1].iloc[locs].set_index(df_var.index)
        diff_list.append(abs(df_var - df_auto))
    colormap = cm.get_cmap('Greys', len(dts))
    colors = colormap(np.linspace(.4, .8, len(dts)))
    fig = plt.figure(figsize=(4, 3))
    ax0 = [plt.subplot2grid((4, 3), (0, i)) for i in range(3)]
    ax1 = [plt.subplot2grid((4, 3), (1, i)) for i in range(3)]
    ax2 = [plt.subplot2grid((4, 3), (2, i)) for i in range(3)]
    ax3 = plt.subplot2grid((4, 3), (3, 0), colspan=3, rowspan=1)
    marker = ''
    figlist = []
    for j, (df_list, name) in enumerate(zip(df_plot_list, ['Autodifferentiation', 'Variational'])):
        figlist.append(plt.figure(figsize=(4, 3)))
        fig = figlist[-1]
        ax0 = [plt.subplot2grid((4, 3), (0, i)) for i in range(3)]
        ax1 = [plt.subplot2grid((4, 3), (1, i)) for i in range(3)]
        ax2 = [plt.subplot2grid((4, 3), (2, i)) for i in range(3)]
        ax3 = plt.subplot2grid((4, 3), (3, 0), colspan=3, rowspan=1)
        marker = ''
        for i, (dt, df) in enumerate(zip(dts, df_list)):
            if dt == dts[-1]:
                marker = ''
            AS = [[A[0, k] for A in df['A']] for k in range(3)]
            AI = [[A[1, k] for A in df['A']] for k in range(3)]
            BI = [B[1] for B in df['B']]
            t = np.arange(0, T, dt)
            _ = [x.plot(t, df[key], color = colors[i], marker=marker, markersize=2.5) for x, key in zip(ax0, ['S', 'I', 'R'])]
            _ = [x.plot(t, AS[k], color = colors[i], marker=marker, markersize=2.5) for k, x in enumerate(ax1)]
            _ = [x.plot(t, AI[k], color = colors[i], marker=marker, markersize=2.5) for k, x in enumerate(ax2)]
            _ = ax3.plot(t, BI, color = colors[i], marker=marker, markersize=2.5)
        _ = [x.set_ylim([0,N_pop]) for x in ax0]
        _ = [x.set_ylim([min(AS[k]), max(AS[k])]) for k, x in enumerate(ax1[:-1])]
        _ = [x.set_ylim([min(AI[k]), max(AI[k])]) for k, x in enumerate(ax2[:-1])]
        _ = [x.set_xlabel('') for x in np.concatenate([ax0, ax1, ax2])]
        _ = [x.grid() for x in np.concatenate([ax0, ax1, ax2, [ax3]])]
        _ = ax3.set_xlabel('time[days]')
        _ = ax3.set_ylim([min(BI), max(BI)])
        _ = [x.set_title(key + ' sensitivities') for key, x in zip(['S', 'I'], [ax1[1], ax2[1]])]
        _ = ax3.set_title(r'$u$ sensitivity to I')
        _ = ax0[1].set_title('Trajectories')
        plt.show()
        fig.subplots_adjust(hspace=.5)
        # fig.savefig('../Figures/Sensitivity_Trajectories.eps', format='eps')

        import numpy.linalg as la
        # A_norms = [np.mean(np.linalg.norm(df['A'])) for df in diff_list]
        A_norms = [la.norm(la.norm(df['A'])) for df in diff_list]
        # B_norms = [np.mean(np.linalg.norm(df['B'])) for df in diff_list]
        B_norms = [la.norm(la.norm(df['B'])) for df in diff_list]




        fig4, ax4 = plt.subplots(2)
        ax4[0].scatter(dts, A_norms, marker='x', color='k', label=r'$||||A_{var}-A_{auto}||_F||_F$')
        ax4[1].scatter(dts, B_norms, marker='o', color='k', label=r'$||||B_{var}-B_{auto}||_F||_F$')
        # ax3.set_yscale('log')
        # ax3.set_xscale('log')
        ax4[0].legend()
        ax4[0].grid()
        ax4[1].legend()
        ax4[1].grid()
        ax4[1].set_xlabel('$\Delta t$')
        plt.show()

        fig4.savefig('../Figures/Sensitivity_Comparison.eps', format='eps')