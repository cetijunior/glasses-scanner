# 👓 AI Glasses Detector (Version 1: Haar Cascade)

Ky është versioni i parë i projektit tonë, i ndërtuar për të detektuar në kohë reale nëse një person ka syze (glasses) apo jo, duke përdorur bibliotekën **OpenCV** dhe klasifikuesit **Haar Cascade**.

This project utilizes simple feature detection for a quick, real-time computer vision demonstration.

---

## 💻 Kërkesat (Requirements)

Për të ekzekutuar këtë projekt, ju duhen këto gjëra:

* **Python 3.x**
* **OpenCV** (`pip install opencv-python`)
* **Haar Cascade XML Files**: Dy skedarë XML janë të nevojshëm dhe duhet të vendosen në të njëjtin folder me skriptin `detector.py`:
    * `haarcascade_frontalface_default.xml` (Për detektimin e fytyrës / For face detection)
    * `haarcascade_eye_tree_eyeglasses.xml` (Për detektimin e syzeve / For glasses detection)

---

## 🚀 Si të Nisesh (How to Run)

1.  **Aktivizo** ambientin virtual (`venv`) ku keni instaluar OpenCV.
2.  **Run the script** nga terminali:

    ```bash
    python detector.py
    ```

3.  Një dritare e kamerës (webcam) do të hapet, duke treguar rezultatin e detektimit në kohë reale.

---

## ⚙️ Si Punon Skripti (Code Overview)

Skripti punon duke kaluar nëpër këto hapa (steps) kryesore në çdo frame të videos:

1.  **Face Detection:** **Scano te gjitha fytyrat** në frame duke përdorur `haarcascade_frontalface_default.xml` (me `minNeighbors=6`).
2.  **ROI Definition:** Për çdo fytyrë, përcakton zonën e interesit (**Region of Interest - ROI**).
3.  **Glasses Detection:** **Scano për syze** brenda ROI duke përdorur `haarcascade_eye_tree_eyeglasses.xml` (me `minNeighbors=4`).
4.  **Output:** **Krahaso skanimiet** dhe afishon rezultatin (`Syze: Po` ose `Syze: Jo`) mbi fytyrën e detektuar.

* **Exit:** **Shtyp "q"** për të dalë nga programi.
