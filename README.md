RoadEye AI — Dangerous Road Detection System

About the Project

RoadEye AI is a Python-based AI application designed to perform preliminary visual screening of road images for possible potholes, cracks, and other visible surface damage.

The project uses a local Ollama vision model to analyze uploaded road images, provide a preliminary risk assessment, suggest cautious next steps, and generate JSON reports.

Project Type: College Hackathon / AI & Computer Vision
Language: Python
Interface: Streamlit
AI Model: Gemma 3 ("gemma3:4b") through Ollama

Features

- Upload road images in JPG, JPEG, PNG, and WEBP formats.
- Analyze visible road conditions using a local AI model.
- Generate preliminary risk levels: LOW, MODERATE, HIGH, or INDETERMINATE.
- Display visible evidence and suggested next steps.
- Enter a road location manually.
- Save generated reports in a local "reports" folder.
- Download reports in JSON format.
- Display a disclaimer about the limitations of AI-generated assessments.

Technology Stack

- Python
- Streamlit
- Ollama
- Gemma 3 Vision Model
- Pillow
- JSON for report generation

Installation and Setup

1. Install the prerequisites

Install Python, Git, Ollama, and Visual Studio Code.

2. Clone the repository

git clone https://github.com/ujiwal7719-ship-it/detecting-dangerous-road.git
cd detecting-dangerous-road

If the application files are inside the nested "detecting-dangerous-road" directory, enter that directory before continuing.

3. Create and activate a virtual environment

On Windows:

python -m venv .venv
.venv\Scripts\activate

4. Install the required packages

python -m pip install streamlit ollama pillow

5. Download the AI model

ollama pull gemma3:4b

6. Run the application

python -m streamlit run app.py

Open the local URL displayed in the terminal, usually "http://localhost:8501".

How to Use

1. Open the RoadEye AI dashboard.
2. Upload a road image.
3. Optionally enter the road location and additional notes.
4. Click Analyze Road Image.
5. Review the preliminary risk assessment and suggested next step.
6. Download the JSON report or find the locally saved report in the "reports" directory.

Limitations and Responsible Use

RoadEye AI provides preliminary AI-generated visual assessments. Its results are not verified road-safety inspections, and the model may miss damage or incorrectly identify visible features.

A LOW risk result does not establish that a road is safe. Suspected hazards should be assessed by appropriate road authorities or qualified inspectors.

The current version uses a vision-language model for image analysis. It should not be considered a dedicated pothole/crack object detector unless a separately trained detection model is implemented and evaluated.

Future Improvements

- Dedicated pothole and crack detection using a trained computer-vision model.
- Bounding boxes highlighting detected damage.
- Road-hazard maps using verified, user-provided location data.
- Analytics and historical report summaries.
- Evaluation against labelled test images with documented accuracy metrics.
- Improved dashboard design and deployment options.

Project Status

The initial Streamlit dashboard has been run locally, and JSON report generation has been observed. Further testing is needed to establish the reliability of the image analysis and risk classifications.
