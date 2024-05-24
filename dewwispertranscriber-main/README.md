🚀🚀WhisperS2T-transcriber🚀🚀

*Empower your transcription tasks with the WhisperS2T and Ctranslate2 libraries for efficient batch processing.*

 Requirements
1. 🐍[Python 3.10](https://www.python.org/downloads/release/python-31011/) or [Python 3.11](https://www.python.org/downloads/release/python-3117/)
2. 📁[Git](https://git-scm.com/downloads)
3. 📁[Git Large File Storage](https://git-lfs.com/)
4. 🟢[CUDA 12.1+](https://developer.nvidia.com/cuda-toolkit) for Nvidia GPU acceleration.
   - *AMD acceleration not yet supported.*
5. 🪟 Windows

> *For Linux installations, manual adjustments might be required in the installation steps. Refer to the `requirements.txt` and `setup_windows.py` files for insights into the necessary libraries.*

 Installation
1. Download the latest release and extract the files on your computer.
2. Navigate to the repository folder, open a command prompt, and execute the following commands:
   ```
   python -m venv .
   ```
   ```
   .\Scripts\activate
   ```
   > *Remember to activate the environment each time you restart the program.*
   ```
   python setup_windows.py
   ```

 Usage
Execute the following command to launch the program:
```
python whispers2t_batch_gui.py
```

The program seamlessly transcribes a variety of file types, including:
- `.mp3`
- `.wav`
- `.flac`
- `.wma`
- `.aac`
- `.m4a`
- `.avi`
- `.mkv`
- `.mp4`
- `.asf`
- `.amr`

*Experience the efficiency of batch transcription with WhisperS2T-transcriber!*
