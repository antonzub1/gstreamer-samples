import sys

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst

Gst.init(None)

Gst.debug_set_active(True)
Gst.debug_set_default_threshold(Gst.DebugLevel.INFO)

command = """
videotestsrc !
decodebin name=dec !
videoconvert !
chromahold target-r=0 target-g=0 target-b=255 !
videoconvert !
perspective !
autovideosink
"""


def link(src, sink):
    if not src.link(sink):
        print(f"Failed to link {src.name} to {sink.name}")
        sys.exit(1)

def main():
    pipeline = Gst.parse_launch(command)
    # Initialize a 2D perspective matrix, you can use
    # cvGetPerspectiveTransform() from OpenCV to build it
    # from a quad-to-quad transformation
    # https://git.ao2.it/experiments/gstreamer.git/blob/HEAD:/c/gst-perspective-example/gst-perspective-example.c
    perspective = pipeline.get_by_name("perspective0")
    perspective.set_property("matrix", Gst.ValueArray([
        1.9999999999999982,
        0.8333333333333287,
        -399.99999999999926,
        3.9968028886505525e-15,
        1.9999999999999978,
        -8.277822871605139e-13,
        2.428612866367518e-18,
        0.0020833333333333294,
        0.9999999999999996
    ]))
    pipeline.set_state(Gst.State.PLAYING)
    loop = GLib.MainLoop()
    loop.run()


main()
