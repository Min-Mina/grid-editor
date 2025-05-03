# 🟥 Grid Layout Editor

A Python GUI app for drawing, resizing, moving, and managing non-overlapping rectangles on a background image using `Tkinter`.

## 🧩 Features

- Add rectangles with a single click
- Drag to move rectangles (no overlaps allowed)
- Resize with 4 corner handles
- Prevent overlap, out-of-bound, and too-small rectangles
- Save/load layout to/from JSON

## 🖼️ Interface Preview
![aaa-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/4ae12a11-6b4c-40e7-bd7c-224f011f9bee)

## 🚀 Getting Started

1. Clone this repo or download the Windows app:
   📥 [Download grid-editor_v1.0.exe](https://github.com/Min-Mina/grid-editor/releases/download/v1.0/grid-editor.exe)
2. Run the app and start creating your grid layout!

## 🖱️ Usage

- New: Add a new 100×100 grid box (default position)
- Delete: Delete the currently selected grid box
- Save: Save all grid boxes to layout.json
- Load: Load grid boxes from layout.json
- Apply: Enter width and height to resize the selected grid box

## ⚠️ Note
- Rectangles cannot overlap
- Minimum size: 20x20
- Must stay within the canvas (1358x686)


