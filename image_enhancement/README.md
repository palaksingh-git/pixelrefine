# Image Enhancement Using OpenCV

This Python 3.9+ project applies a five-stage image processing pipeline and shows the results side by side in one Matplotlib window. It saves the four processed stages as PNG files by default.

## Install

Open PowerShell in the `image_enhancement` directory, then run:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell does not allow activation, run `.\venv\Scripts\python.exe` in place of `python` for the commands below.

## Run

Open a file selection dialog:

```powershell
python main.py
```

Or supply an image path:

```powershell
python main.py --image sample.jpg
```

An absolute path or a path relative to the current directory also works. Supported file extensions are `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tif`, `.tiff`, and `.webp`. The image must contain data OpenCV can decode. Closing the file dialog without selecting an image exits cleanly.

Optional settings:

```powershell
python main.py --image sample.jpg --kernel 7 --low 80 --high 180 --no-save
```

`--kernel` must be a positive odd integer; the default is 5. Canny thresholds must satisfy `0 <= --low < --high <= 255`; defaults are 100 and 200. `--no-save` displays the results without creating output files.

## Processing steps

1. **Grayscale:** converts the original BGR image to one brightness channel.
2. **Gaussian Blur:** smooths the grayscale image to reduce noise, using a 5×5 kernel by default.
3. **Histogram Equalization:** redistributes brightness values in the blurred image to improve contrast.
4. **Canny Edge Detection:** finds edges in the equalized image using lower and upper thresholds.
5. **Display and save:** shows the original and four processed images together. The original is converted from BGR to RGB for Matplotlib. Each processed stage is saved in `output/` as `<input-name>_grayscale.png`, `<input-name>_blurred.png`, `<input-name>_equalized.png`, or `<input-name>_edges.png`.

## Test with a sample image

Copy any supported image to this directory as `sample.jpg`, then run:

```powershell
python main.py --image sample.jpg
```

Check that one window shows **Original | Grayscale | Gaussian Blur | Histogram Equalized | Canny Edges**, and that four PNG files appear in `output/`. You can also try `--no-save` to confirm it leaves the output directory untouched.
