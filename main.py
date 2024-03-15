from typing import Annotated
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from face_recognition import FaceRecognition, utills
import logging
import aiofiles


logging.basicConfig(filename="face_recognition.log",
                    filemode='a',
                    encoding='utf-8',
                    format='%(asctime)s %(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


app = FastAPI()


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    for file in files:
        type_file = file.content_type.split("/")[0]
        if type_file == "video":
                async with aiofiles.open(f"static/{file.filename}", 'wb') as out_file:
                    while content := await file.read(1024):  # async read chunk
                        await out_file.write(content)  # async write chunk
        elif type_file == "image":
            async with aiofiles.open(f"static/Person_db/{file.filename}", 'wb') as out_file:
                while content := await file.read(1024):  # async read chunk
                    await out_file.write(content)  # async write chunk
        else:
            logging.info("Uncorrect type of file uploaded!")
            file.close()
    logging.info("Files Saved!")
    return {"filenames": [(file.filename, file.content_type) for file in files]}


@app.get("/recognize/")
async def recognize_face():
    persons_db_path = "static/Person_db"
    person_face_db_path = "static/Person_face_db"
    persons = 1
    utills.create_person_face_db(persons_db_path, person_face_db_path, persons)
    frames = FaceRecognition.FaceRecognition.recognize()
    return {"frames": [frame for frame in frames]}



@app.get("/")
async def main():
    content = """
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<h4>Upload Your Video Here</h4>
<input name="files" type="file" multiple>
<br>
<h4>Upload Your Image(s) Here</h4>
<input name="files" type="file" multiple>
<br>
<br>
<br>
<br>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
