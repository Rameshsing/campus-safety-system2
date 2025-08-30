py -3.11 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt


<---
// only if required

pip uninstall tensorflow tensorflow-intel tf-keras ml-dtypes tensorboard keras -y
pip install tensorflow==2.17.1
pip install keras==2.12.0
pip install ml-dtypes==0.4.1
pip install tensorboard==2.17.1
pip install deepface==0.0.79
pip install retina-face==0.0.13


pip uninstall tensorflow keras
pip install tensorflow==2.12.0 keras==2.12.0

--->

python app.py
