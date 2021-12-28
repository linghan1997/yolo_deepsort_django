from django.shortcuts import render

# Create your views here.
import argparse
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
import cv2
from threading import Thread

from dotenv import load_dotenv
from redis import Redis
from os import environ, getenv
from os.path import join
from utils.parser import get_config
from .tracking_thread import RealTimeTracking
from .server_config import model, deep_sort_dict

redis_cache = Redis('127.0.0.1')
environ['in_progress'] = 'off'


# /run/0 or 1
def process_manager(request, run):

    if run == 1:
        try:
            if environ.get('in_progress', 'off') == 'off':
                environ['in_progress'] = 'on'
                cfg = get_config()
                cfg.merge_from_dict(model)
                cfg.merge_from_dict(deep_sort_dict)

                # test: fix args
                class args:
                    def __init__(self):
                        self.input = 0
                        self.model = 'D:\\py_projects\\deep_sort_pytorch\\yolov3'
                        self.use_cuda = True

                args = args()

                return trigger_process(cfg, args)

            elif environ.get('in_progress', 'off') == 'on':
                return JsonResponse({"message": "Tracking is already in progress"})
        except Exception:
            environ['in_progress'] = 'off'
            return JsonResponse({"message": "Exception happens"})
    elif run == 0:
        if environ.get('in_progress', 'off') == 'off':
            return JsonResponse({"message": "Tracking is already terminated!"})
        else:
            environ['in_progress'] = 'off'
            return JsonResponse({"message": "Tracking terminated!"})


# open tracking thread
def trigger_process(cfg, args):
    try:
        t = Thread(target=tracking, args=(cfg, args))
        t.start()
        return JsonResponse({"message": "Tracking started"})
    except Exception:
        return JsonResponse({'message': "Unexpected exception occured in process"})


def tracking(cfg, args):
    tracker = RealTimeTracking(cfg, args)
    tracker.run()


def gen():
    while True:
        frame = redis_cache.get('frame')
        if frame is not None:
            yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'


@gzip.gzip_page
def live(request):
    try:
        return StreamingHttpResponse(gen(), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass


# 解析输入camera_stream， 模型model_type, GPU/CPU(default: false)
# def parse_args():
#     assert 'project_root' in environ.keys()
#     project_root = getenv('project_root')
#     parser = argparse.ArgumentParser()
#
#     environ['camera_stream'] = "0"
#
#     parser.add_argument("--input",
#                         type=str,
#                         default=getenv('camera_stream'))
#
#     parser.add_argument("--model",
#                         type=str,
#                         default=join(project_root,
#                                      getenv('model_type')))
#
#     parser.add_argument("--cpu",
#                         dest="use_cuda",
#                         action="store_false", default=True)
#     args = parser.parse_args()
#
#     return args
