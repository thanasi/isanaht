try:
    # check that we've loaded ipython interactively
    __IPYTHON__
    # if not "ipykernel.zmqshell" in str(get_ipython()):
    if not "zmqshell.ZMQInteractiveShell" in str(get_ipython()):
        aaaaaaaa

    from ipywidgets import HTML
    from tempfile import NamedTemporaryFile
    from matplotlib import animation, style
    from matplotlib import pyplot as plt

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

except NameError:
    raise ImportError("This package is meant to be imported into an IPython Notebook")

