1. "cd detector/YOLOv3/weight/" Download Yolov3.weights from https://pjreddie.com/media/files/yolov3.weights
2. Create a virtual environment
3. "pip install -r requirements.txt", pytorch should be installed seperately from https://pytorch.org/ depending on CPU/GPU
4. "python manage.py runserver" to launch the Django Server

http://127.0.0.1:8000/deepsort/run/1/: starts the tracking thread
http://127.0.0.1:8000/deepsort/stream/: shows the video
