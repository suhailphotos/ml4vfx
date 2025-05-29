import hou

def onClickExecute(kwargs):
    hda   = kwargs["node"]
    py    = hda.node("solver_py")
    stash = hda.node("result_paths")

    # Trigger the Python SOP to cook (fresh paths).
    ver = py.parm("version")
    ver.set(ver.eval() + 1)       # forces recook on next evaluation
    py.cook(force=True)           # cook immediately so we can stash

    # Tell the Stash SOP to capture its input.
    stash.parm("stashinput").pressButton()
