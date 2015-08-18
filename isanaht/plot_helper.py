import os
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.font_manager as font_manager
import palettable as pbl

# define some useful property settings
side_legend_settings = {"bbox_to_anchor": (1.02, 1),
                        "loc": 2,
                        "borderaxespad": 0.0,
                        "numpoints": 1}

cmap3 = pbl.colorbrewer.get_map('Set1', 'Qualitative', 3)
cmap5 = pbl.colorbrewer.get_map('Set1', 'Qualitative', 5)
cmap7 = pbl.colorbrewer.get_map('Set1', 'Qualitative', 7)


def set_plot_defaults_1():
    mpl.rc('legend', fancybox=False, numpoints=1, markerscale=1.5, borderaxespad=0.5)
    mpl.rc('axes', linewidth=1.5, edgecolor='k', labelsize=22, grid=False, axisbelow=True)
    mpl.rc('grid', linewidth=1)

    # f = get_font("GillSans", "")
    # mpl.rc('font', family=f.get_family(), style=f.get_style(), weight=f.get_weight(), size=16)

    mpl.rc('ytick.major', size=5, width=1.5, pad=8)
    mpl.rc('xtick.major', size=5, width=1.5, pad=8)


def fmt_ax(ax):

    labelfont = get_font("GillSans", "")
    labelfont.set_size(22)
    la_pad = 12

    ax.set_xlabel(ax.get_xlabel(), fontproperties=labelfont, labelpad=la_pad)
    ax.set_ylabel(ax.get_ylabel(), fontproperties=labelfont, labelpad=la_pad)

    tickfont = get_font("Avenir Next", "Medium")
    tickfont.set_size(16)
    set_tick_label_font(ax, tickfont)


    Le = ax.get_legend()
    # set_border_width(Le.axes, 1.5)
    if Le is not None:
        fr = Le.get_frame()
        fr.set_linewidth(1.5)
        fr.set_edgecolor("k")

    ax.grid(True)


# helper functions to clean up plot style
def get_font(fontname, style=""):
    font_dir = "/Users/thanasi/.mplfonts/"

    if style is "":
        fstyle = ""
    else:
        fstyle = "-" + style.replace(" ", "")

    filename = font_dir + fontname.replace(" ", "") + fstyle + ".ttf"

    assert os.path.exists(filename), "Need to pick a font file from: " + str(os.listdir(font_dir))

    return font_manager.FontProperties(fname=filename)


def set_legend_title_size(ax, s='large'):
    plt.setp(ax.get_legend().get_title(), fontsize=s)


def set_tick_label_font(ax, fontprop):
        [i.set_fontproperties(fontprop) for i in (ax.get_xticklabels() + ax.get_yticklabels())]


def set_ax_border_prop(ax, w=2, c='k'):
    for i in ax.spines.itervalues():
        i.set_linewidth(w)
        i.set_color(c)


def set_border_width(ax, w=2):
    for i in ax.spines.itervalues():
        i.set_linewidth(w)


def fix_image_axes(ax):
    ims = ax.get_images()
    if ims is not None:
        ny, nx = ims[0].get_array().shape
        ax.set_xlim(0, nx)
        ax.set_ylim(ny, 0)

