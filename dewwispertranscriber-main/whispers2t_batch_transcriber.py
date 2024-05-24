import os
import gc
from PySide6.QtCore import QThread, Signal, QElapsedTimer
from pathlib import Path
import whisper_s2t
from queue import Queue
import torch
from threading import Event

class TranscriptionWorker(QThread):
    finished = Signal(str)
    progress = Signal(str)

    def __init__(self, directory, recursive, output_format, device, model_size, quantization, beam_size, batch_size, task, file_extensions):
        super().__init__()
        self.directory = directory
        self.recursive = recursive
        self.output_format = output_format
        self.device = device
        self.model_size = model_size
        self.quantization = quantization
        self.beam_size = beam_size
        self.batch_size = batch_size
        self.task = task.lower()
        self.file_extensions = file_extensions
        self.file_queue = Queue()
        self.enumeration_done = False
        self.stop_requested = Event()
        self.total_files = 0

    def request_stop(self):
        self.stop_requested.set()

    def release_resources(self, model):
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()

    def gather_files(self, directory_path, patterns):
        for pattern in patterns:
            if self.recursive:
                for file_path in directory_path.rglob(pattern):
                    self.file_queue.put(file_path)
                    self.total_files += 1
            else:
                for file_path in directory_path.glob(pattern):
                    self.file_queue.put(file_path)
                    self.total_files += 1
        self.enumeration_done = True

    def run(self):
        directory_path = Path(self.directory)
        patterns = [f'*{ext}' for ext in self.file_extensions]

        self.gather_files(directory_path, patterns)

        model_id = f"ctranslate2-4you/whisper-{self.model_size}-ct2-{self.quantization}"
        model = whisper_s2t.load_model(model_identifier=model_id, backend='CTranslate2', device=self.device, compute_type=self.quantization, asr_options={'beam_size': self.beam_size}, cpu_threads=os.cpu_count())

        timer = QElapsedTimer()
        timer.start()

        processed_files = 0

        while not self.file_queue.empty() or not self.enumeration_done:
            if self.stop_requested.is_set():
                break
            try:
                audio_file = self.file_queue.get(timeout=1)
                processed_files += 1
                progress_message = f"Processing {audio_file} ({processed_files}/{self.total_files})"
                self.progress.emit(progress_message)
                transcription_output = model.transcribe_with_vad([str(audio_file)], lang_codes=['en'], tasks=[self.task], initial_prompts=[None], batch_size=self.batch_size)
                output_file = str(audio_file.with_suffix(f'.{self.output_format}'))
                whisper_s2t.write_outputs(transcription_output, format=self.output_format, op_files=[output_file])
                completion_message = f"Completed {audio_file} to {output_file} ({processed_files}/{self.total_files})"
                self.progress.emit(completion_message)
                self.file_queue.task_done()
            except Exception as e:
                error_message = f"Error processing file {audio_file if 'audio_file' in locals() else 'unknown'}: {e} ({processed_files}/{self.total_files})"
                self.progress.emit(error_message)
                print(f"\033[33m{error_message}\033[0m")
        
        self.release_resources(model)

        total_time = timer.elapsed() / 1000.0
        self.finished.emit(f"Total processing time: {total_time:.2f} seconds")
