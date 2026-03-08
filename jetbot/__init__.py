from .camera import Camera
from .heartbeat import Heartbeat
from .motor import Motor
from .robot import Robot
from .image import bgr8_to_jpeg

try:
    from .object_detection import ObjectDetector
except ImportError as e:
    _object_detection_import_error = e

    class ObjectDetector(object):
        def __init__(self, *args, **kwargs):
            raise ImportError(
                'ObjectDetector requires the TensorRT/PyTorch runtime dependencies.'
            ) from _object_detection_import_error
