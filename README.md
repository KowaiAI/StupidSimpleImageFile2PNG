<p align="center">
  <img src="data/icons/hicolor/scalable/apps/io.github.bulkimageconverter.svg" width="128" height="128" alt="App Icon">
</p>

<h1 align="center">Stupid Simple Image File 2 PNG</h1>

<p align="center">
  <strong>Convert images to PNG and strip metadata with one click</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#supported-formats">Formats</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/GTK-4.0-green?style=flat-square&logo=gtk" alt="GTK4">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Platform-Linux-orange?style=flat-square&logo=linux&logoColor=white" alt="Linux">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="MIT License">
</p>

---

## ✨ What is this?

A **stupid simple** GTK4/Libadwaita app that does exactly what it says:

1. **Select images** (as many as you want)
2. **Click convert**
3. **Get PNGs** with all metadata stripped

No bloat. No complexity. Just PNG conversion with privacy in mind.

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 📁 **Bulk Selection** | Select multiple images at once |
| 🔒 **Metadata Stripping** | Removes EXIF, XMP, IPTC data for privacy |
| 🔄 **Format Conversion** | JPG, WebP, GIF, BMP, TIFF → PNG |
| 📂 **Custom Output** | Choose where converted files go |
| 📊 **Progress Tracking** | See conversion progress in real-time |
| 🎨 **Native Look** | Beautiful Libadwaita interface |

---

## 📦 Installation

### Option 1: Flatpak (Recommended)

```bash
# Install GNOME runtime if you don't have it
flatpak install flathub org.gnome.Platform//47 org.gnome.Sdk//47

# Clone and build
git clone https://github.com/KowaiAI/StupidSimpleImageFile2PNG.git
cd StupidSimpleImageFile2PNG
flatpak-builder --user --install --force-clean build io.github.bulkimageconverter.yml

# Run
flatpak run io.github.bulkimageconverter
```

### Option 2: Run from Source

#### 1. Install system dependencies

**Ubuntu/Debian:**
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 libadwaita-1-dev python3-venv
```

**Fedora:**
```bash
sudo dnf install python3-gobject gtk4 libadwaita python3-virtualenv
```

**Arch:**
```bash
sudo pacman -S python-gobject gtk4 libadwaita python-virtualenv
```

#### 2. Clone and setup

```bash
git clone https://github.com/KowaiAI/StupidSimpleImageFile2PNG.git
cd StupidSimpleImageFile2PNG
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Run

```bash
python main.py
```

---

## 🚀 Usage

1. **Launch the app**
2. Click **"Browse"** to select images
3. *(Optional)* Change the output folder
4. Click **"Convert to PNG"**
5. Done! Your metadata-free PNGs are ready

### Default Output Location

```
~/Pictures/converted/
```

---

## 📷 Supported Formats

| Input Format | Extensions |
|--------------|------------|
| JPEG | `.jpg`, `.jpeg` |
| WebP | `.webp` |
| GIF | `.gif` |
| BMP | `.bmp` |
| TIFF | `.tiff`, `.tif` |
| PNG | `.png` *(for metadata stripping)* |

**Output:** Always PNG with no metadata.

---

## 🔐 Why Strip Metadata?

Images can contain hidden information:

- 📍 **GPS coordinates** - Where the photo was taken
- 📅 **Timestamps** - When it was taken
- 📱 **Device info** - Camera/phone model
- 👤 **Author info** - Your name, software used

This app removes **all** of that automatically.

### Verify Metadata Removal

```bash
# Using exiftool
exiftool your_converted_image.png

# Should show minimal/no metadata
```

---

## 🛠️ Tech Stack

- **UI:** GTK4 + Libadwaita
- **Image Processing:** Pillow (PIL)
- **Language:** Python 3
- **Packaging:** Flatpak

---

## 📄 License

MIT License - Do whatever you want with it.

---

<p align="center">
  Made with ❤️ for the Linux community
</p>
