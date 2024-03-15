For running the code you can use the following steps:
1. cloning the repo:

```
git clone https://github.com/sepehratwork/FaceRecognitionFastAPI.git
```

2. change the directory to the following repo:

```
cd FaceRecognitionFastAPI
```

3. run the fastapi web application using this:

```
python main.py
```

4. now you can go to the following link in your browser and upload your files:

```
http://127.0.0.1:8000/
```

5. after that a json will be returned showing the list of iploaded files with their type and you will automatically headed to :
```
http://127.0.0.1:8000/uploadfiles/
```
for finding the face of the person you want you can go to the following link:
```
http://127.0.0.1:8000/recognize/
```
this would take too long. finally a list of frames in which the wanted person has been recognized will appear.
