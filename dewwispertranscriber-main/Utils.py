import torch
import ctranslate2

def get_available_devices():
    devices = ["cpu"]
    if ctranslate2.get_cuda_device_count() > 0:
        devices.append("cuda")
    return devices

def get_supported_quantization_types(device):
    supported_types = ctranslate2.get_supported_compute_types(device)
    filtered_types = [q for q in supported_types if q != "int16"]
    desired_order = ["float32", "float16", "bfloat16", "int8_float32", "int8_float16", "int8_bfloat16", "int8"]
    sorted_types = [q for q in desired_order if q in filtered_types]
    return sorted_types
