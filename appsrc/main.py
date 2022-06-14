import gi
import numpy as np
gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")

from gi.repository import Gst, GLib, GstApp

Gst.init(None)

def on_buffer(sink, data):
    sample = sink.emit("pull-sample")
    buf = sample.get_buffer()


def main():
    loop = GLib.MainLoop()
    pipeline = Gst.Pipeline("simple")
    # appsrc = Gst.ElementFactory.make("appsrc")
    appsrc = GstApp.AppSrc()
    # from ipdb import set_trace; set_trace(context=20)
    videoconvert = Gst.ElementFactory.make("videoconvert")
    xvimagesink = Gst.ElementFactory.make("autovideosink")
    queue = Gst.ElementFactory.make("queue")
    appsrc.set_property("format", Gst.Format.TIME)
    appsrc.set_property("block", True)
    appsrc.set_property("emit-signals", True)
    appsrc.set_property("is-live", True)
    appsrc.set_caps(Gst.Caps.from_string("video/x-raw,format=RGB,width=640,height=480,framerate=60/1"))
    queue.set_property("max-size-buffers", 4)
    pipeline.add(appsrc)
    pipeline.add(queue)
    pipeline.add(videoconvert)
    pipeline.add(xvimagesink)
    appsrc.link(queue)
    queue.link(videoconvert)
    videoconvert.link(xvimagesink)
    pipeline.set_state(Gst.State.READY)
    Gst.debug_bin_to_dot_file(pipeline, Gst.DebugGraphDetails.ALL, "./simple")
    try:
        pipeline.set_state(Gst.State.PLAYING)
        array_to_buf = lambda buf: Gst.Buffer.new_wrapped(array.tobytes())
        for _ in range(1024 ** 2):
            array = np.random.randint(low=0, high=255,
                                      size=(480, 640, 1),
                                      dtype=np.uint)
            appsrc.emit("push-buffer", array_to_buf(array))
        appsrc.emit("end-of-stream")
        pipeline.set_state(Gst.State.NULL)
    except:
        pipeline.set_state(Gst.State.NULL)


if __name__ == "__main__":
    main()
