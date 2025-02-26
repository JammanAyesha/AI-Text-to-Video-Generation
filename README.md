# 🎥 AI Text-to-Video Generation  

This project generates videos from text descriptions using **Stable Diffusion**, **OpenCV**, and **Deep Learning** models.

---

## 📌 Features  
✅ Converts text into AI-generated images  
✅ Merges generated images into a video  
✅ Supports multiple scenes with different prompts  
✅ Uses Stable Diffusion for high-quality frames  
✅ OpenCV for video processing  

---

## 🛠️ Tech Stack  
- **Python 3.8+**  
- **Stable Diffusion** (via Diffusers library)  
- **OpenCV**  
- **NumPy**  
- **TensorFlow**  

---

## 📂 Project Structure  

AI-Text-to-Video-Generation/
│── venv/ # Virtual environment (ignored in Git)
│── video_frames_/ # Folders storing generated frames
│── generated_video.mp4 # Final output video
│── t2v.py # Main script for text-to-video generation
│── test.py # Script to check dependencies
│── requirements.txt # List of dependencies
│── README.md # Project documentation


---

## 🚀 Installation & Setup  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/JammanAyesha/AI-Text-to-Video-Generation.git
cd AI-Text-to-Video-Generation

2️⃣ Set Up the Virtual Environment
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  # For Windows

3️⃣ Install Dependencies

pip install -r requirements.txt


4️⃣ Run the Main Script

python t2v.py


📜 Dependencies

Make sure you have the following dependencies installed:

pip install torch diffusers opencv-python numpy matplotlib tensorflow tqdm

📧 Contact

Developed by Jamman Ayesha

🛡️ License

This project is licensed under the MIT License.



