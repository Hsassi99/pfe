from django.apps import AppConfig

import torch

class DroneAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "drone_app"

    def ready(self):
        if not hasattr(self, 'model'):
            # Load the YOLOv5 model
            self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
