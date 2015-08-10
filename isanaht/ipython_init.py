try:
    # check that we've loaded ipython interactively
    __IPYTHON__
    if not "zmq.zmqshell" in str(get_ipython()):
        aaaaaaaa

    from IPython.display import HTML
    from tempfile import NamedTemporaryFile
    from matplotlib import animation, style
    from matplotlib import pyplot as plt

    import palettable as pbl

    VIDEO_TAG = """<video controls>
     <source src="data:video/x-m4v;base64,{0}" type="video/mp4">
     Your browser does not support the video tag.
    </video>"""

    def anim_to_html(anim):
        if not hasattr(anim, '_encoded_video'):
            with NamedTemporaryFile(suffix='.mp4') as f:
                anim.save(f.name, fps=20, extra_args=['-vcodec', 'libx264'])
                video = open(f.name, "rb").read()
            anim._encoded_video = video.encode("base64")

        return VIDEO_TAG.format(anim._encoded_video)

    def display_animation(anim):
        plt.close(anim._fig)
        return HTML(anim_to_html(anim))


    # actually run this when the package is imported
    style.use("ipython_style_inline")

    side_legend_settings = {"fontsize": 16,
                            "bbox_to_anchor": (1.02, 1),
                            "loc": 2,
                            "borderaxespad": 0.0,
                            "numpoints": 1}

    cmap3 = pbl.colorbrewer.get_map('Set1', 'Qualitative', 3)
    cmap5 = pbl.colorbrewer.get_map('Set1', 'Qualitative', 5)
    cmap7 = pbl.colorbrewer.get_map('Set1', 'Qualitative', 7)

except NameError:
    raise ImportError("This package is meant to be imported into an IPython Notebook")