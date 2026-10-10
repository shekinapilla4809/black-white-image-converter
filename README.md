# 🖤 Black & White Image Converter

### 🚀 Simple Online Image Converter Built with Python & Streamlit

**Black & White Image Converter** is a user-friendly web application built with Python and Streamlit that allows users to convert color images into black-and-white images with customizable intensity, brightness, and contrast settings.

The application provides a clean, responsive interface with Light Mode and Dark Mode, drag-and-drop image uploads, before-and-after image previews, batch image processing, and downloadable output files.

---

# 🚀 Project Overview

Black & White Image Converter provides a simple workflow for converting and customizing images directly in your browser.

```text
Open the Application
         ↓
Upload One or More Images
         ↓
Adjust B&W Intensity
         ↓
Customize Brightness & Contrast
         ↓
Preview Before & After
         ↓
Choose Output Format
         ↓
Download Converted Images
```

---

# ✨ Features

- 🖼️ Upload single or multiple images
- 📂 Drag-and-drop image upload
- 🖤 Convert color images to black and white
- 🎚️ Adjustable black-and-white intensity
- ☀️ Brightness adjustment
- 🌗 Contrast adjustment
- 👀 Before-and-after image comparison
- 📦 Batch image conversion
- 📥 Download individual converted images
- 🗜️ Download multiple converted images as a ZIP file
- 🖼️ Support for PNG, JPG, JPEG, WEBP, BMP, TIF, and TIFF
- 🎨 Light Mode and Dark Mode
- 📱 Responsive and user-friendly interface
- ⚡ Fast image processing using Pillow
- 📏 Display image dimensions and file information
- 🔄 Reset adjustment settings
- 🐍 Python-based application
- ☁️ Streamlit Community Cloud deployment support

**Note:** Supported image formats, file sizes, and processing performance depend on the application configuration and available system resources.

---

# 🧠 How It Works

## 1️⃣ Open the Application

Open Black & White Image Converter in your browser.

The application displays an easy-to-use interface where you can upload images and customize conversion settings.

## 2️⃣ Upload Images

Select one or more images from your computer, or drag and drop them into the upload area.

Supported file formats include:

```text
PNG
JPG
JPEG
WEBP
BMP
TIF
TIFF
```

## 3️⃣ Adjust Black-and-White Intensity

Use the intensity slider to control how strongly the black-and-white effect is applied.

```text
Upload Image
     ↓
Adjust Intensity
     ↓
Apply Grayscale Effect
     ↓
Preview Converted Image
```

The intensity setting blends the original image with its grayscale version, allowing different levels of the effect.

## 4️⃣ Customize Brightness and Contrast

Use the adjustment controls to customize the converted image.

- **Brightness:** Makes the image lighter or darker.
- **Contrast:** Changes the difference between lighter and darker areas.
- **B&W Intensity:** Controls the strength of the grayscale effect.

You can reset the settings and try different combinations.

## 5️⃣ Compare Before and After

The application displays the original image alongside the converted image.

This helps you compare the results before downloading.

## 6️⃣ Download Converted Images

Choose the output format and download your converted images.

Depending on the selected options, you can download an individual image or a ZIP archive containing multiple converted images.

---

# 🛠️ Technologies Used

## Programming Language

- Python

## User Interface

- Streamlit
- HTML
- CSS

## Image Processing

- Pillow (PIL)

## Python Libraries

- Streamlit
- Pillow
- Python Standard Library

## Version Control

- Git
- GitHub

## Deployment

- Streamlit Community Cloud

---

# 📁 Project Structure

```text
black-white-image-converter/
│
├── app.py
│
├── requirements.txt
│
└── README.md
```

### File Description

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application, UI, image upload, conversion, adjustments, previews, and downloads |
| `requirements.txt` | Python dependencies required to run the application |
| `README.md` | Project documentation, features, installation, and deployment instructions |

This structure describes the main repository files. Additional files can be added as the project develops.

---

# 💻 Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/black-white-image-converter.git
```

Replace `YOUR_GITHUB_USERNAME` with your GitHub username.

## 2️⃣ Open the Project Folder

```bash
cd black-white-image-converter
```

## 3️⃣ Create a Virtual Environment

Creating a virtual environment is recommended.

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

## 4️⃣ Install Python Dependencies

```bash
python -m pip install -r requirements.txt
```

## 5️⃣ Run the Application

```bash
python -m streamlit run app.py
```

The application normally opens in your default browser.

Local URL:

```text
http://localhost:8501
```

---

# 📦 Requirements

## `requirements.txt`

```text
streamlit>=1.40.0
Pillow>=10.4.0
```

### Streamlit

Streamlit is used to build the interactive web application, upload controls, sliders, previews, and download buttons.

### Pillow

Pillow is used to open, process, convert, adjust, and save images.

**Note:** The versions above specify minimum versions. Your installed environment may use newer compatible releases.

---

# 🎨 Theme Support

Black & White Image Converter includes two interface themes.

## ☀️ Light Mode

A bright interface with clear text, readable controls, and a clean appearance.

## 🌙 Dark Mode

A dark interface designed for comfortable viewing.

Users can switch between themes using the theme selector in the application.

---

# 🖤 Black-and-White Conversion

The application uses Pillow to convert color images into grayscale images.

A grayscale image represents pixels using shades ranging from black to white.

The conversion workflow is:

```text
Original Color Image
         ↓
Load Image Using Pillow
         ↓
Convert to Grayscale
         ↓
Apply Intensity
         ↓
Adjust Brightness & Contrast
         ↓
Generate Output Image
```

The intensity control blends the original image with the grayscale result. Therefore, lower intensity values can preserve more of the original color, while higher values produce a stronger black-and-white appearance.

---

# 🎚️ Image Adjustments

## Brightness

Brightness adjustment controls the overall lightness of the image.

It can help make darker images brighter or reduce excessive brightness.

## Contrast

Contrast adjustment controls the visual difference between light and dark areas.

Increasing contrast can make details appear more pronounced, while reducing contrast can create a softer appearance.

## Intensity

The intensity slider controls how much of the grayscale effect is applied to the original image.

These settings help users customize the output without requiring separate image-editing software.

---

# 👀 Before-and-After Comparison

The application provides a side-by-side preview of the original and converted images.

Users can:

- View the original image.
- Inspect the black-and-white result.
- Experiment with intensity, brightness, and contrast.
- Review the output before downloading.

The comparison helps users choose suitable settings for each image.

---

# 📦 Batch Image Conversion

Batch processing allows users to upload multiple supported images in one session.

The workflow is:

```text
Select Multiple Images
          ↓
Apply Conversion Settings
          ↓
Process Images
          ↓
Preview Results
          ↓
Download Individual Images
          ↓
Download ZIP Archive
```

Batch processing can save time when converting multiple images with the same settings.

Processing speed depends on image dimensions, the number of uploaded files, and available memory.

---

# 📥 Download Options

The application supports downloading converted images in the available output formats.

Depending on the current implementation, users can:

- Download a converted image individually.
- Select PNG or JPEG output.
- Download multiple converted images as a ZIP archive.

PNG is useful when lossless image output is preferred. JPEG can produce smaller files, depending on the image and encoding settings.

---

# ⚡ Performance

Black & White Image Converter uses Pillow for image processing.

Benefits include:

- Fast local image transformations
- No separate image-editing application required
- Support for multiple common image formats
- Adjustable conversion settings
- Batch processing within available system resources

Very large images or large batches may require additional memory and processing time.

---

# 🎯 Problem Statement

Converting color images to black and white and adjusting their appearance can require multiple steps in traditional image-editing applications.

Users may need a simpler way to apply grayscale effects, adjust brightness and contrast, compare results, and download processed images.

---

# 💡 Proposed Solution

Black & White Image Converter provides a browser-based image-processing interface built with Python, Streamlit, and Pillow.

The application combines image upload, grayscale conversion, intensity adjustment, brightness and contrast controls, before-and-after previews, and download options in one place.

Its goal is to make common image-conversion tasks simple and accessible.

---

# 🌟 Key Benefits

- Simple and user-friendly interface
- Multiple image format support
- Adjustable black-and-white intensity
- Brightness and contrast controls
- Before-and-after previews
- Batch image processing
- Individual and ZIP downloads
- Light and Dark themes
- No separate desktop image editor required
- Python-based implementation
- GitHub-based project management
- Optional cloud deployment

---

# ☁️ Deployment

Black & White Image Converter can be deployed using **Streamlit Community Cloud**, subject to the platform's current policies and resource limits.

## Deployment Steps

1. Push your project files to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in using your GitHub account.
4. Create a new app.
5. Select your `black-white-image-converter` repository.
6. Select the `main` branch.
7. Set the main file path to `app.py`.
8. Click **Deploy**.

Ensure that `app.py` and `requirements.txt` are included in the repository.

### Hosting Considerations

- Free hosting environments may have memory and resource limits.
- Large images may take longer to process.
- Temporary files and generated outputs may not persist after an application restart.
- Uploaded images are processed by the application environment, so avoid uploading sensitive images to a deployment you do not trust.
- ZIP generation and batch processing may require additional memory.

---

# 🔮 Future Enhancements

Potential future improvements include:

- 🎨 Sepia and vintage filters
- 🌈 Additional image effects
- 📏 Image resizing and cropping
- 🗜️ Adjustable JPEG quality
- 📊 More detailed processing progress
- 📋 Conversion history
- 📦 Batch download improvements
- 🖼️ Additional image output formats
- 📱 Further mobile interface improvements
- 🧪 Automated testing
- ⚙️ Advanced image settings

These are possible future enhancements and may not be available in the current version.

---

# ⚖️ Responsible Use

Black & White Image Converter is intended for legitimate image-processing purposes.

Users are responsible for ensuring they have the necessary rights and permissions to upload, modify, and share the images they process.

Avoid uploading confidential or sensitive images to public hosting services unless you understand the service's privacy and data-handling practices.

---

# 👩‍💻 Developer

### Shekina Pilla

**B.Tech – Computer Science & Engineering (Data Science)**

### Areas of Interest

- Python Development
- Full Stack Development
- Artificial Intelligence
- Data Science
- Web Applications
- Cloud Applications

---

# 🙏 Acknowledgements

This project uses the following technologies:

- Python
- Streamlit
- Pillow
- HTML
- CSS
- Git
- GitHub

Thanks to the developers and maintainers of these technologies.

---

# 📜 License

No specific license is declared for this project.

If you plan to distribute the application or allow others to reuse its source code, consider adding an appropriate `LICENSE` file and reviewing the licenses of its dependencies.

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ star on GitHub.

**GitHub Repository:**  
https://github.com/YOUR_GITHUB_USERNAME/black-white-image-converter

Thank you for visiting **Black & White Image Converter!** 🖤🖼️✨
