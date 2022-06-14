import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst

Gst.init(None)

Gst.debug_set_active(True)
Gst.debug_set_default_threshold(3)

videotestsrc = Gst.ElementFactory.make('videotestsrc', None)
pipeline = Gst.Pipeline("my_videotestsrc")
ximagesink = Gst.ElementFactory.make('ximagesink', None)
pipeline.add(videotestsrc, ximagesink)
videotestsrc.link(ximagesink)
pipeline.set_state(Gst.State.PLAYING)
Gst.debug_bin_to_dot_file(pipeline, Gst.DebugGraphDetails.ALL,
                          "./debug_graph")

loop = GLib.MainLoop()
loop.run()
