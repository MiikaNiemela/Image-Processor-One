import os
from dotenv import load_dotenv
import time
from contextlib import closing
import sqlite3
import base64
from io import BytesIO
from PIL import Image
import glob
import uuid
from colorama import Fore, Style
from langchain_core.documents import Document
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_chroma import Chroma
from ImageDetails import ImageDetails
import ImageDetailsFactory

load_dotenv()

def get_jpeg_files(directory):
    file_extensions = ['jpg', 'jpeg']
    all_files = []
    for ext in file_extensions:
        pattern = os.path.join(directory, '**', f'*.{ext}')
        all_files.extend(glob.glob(pattern, recursive=True))
    return all_files

def convert_to_base64(pil_image)->str:
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def get_processed_files():
    with closing(sqlite3.connect(f"./{db_name}/chroma.sqlite3")) as connection:
        sql = "select string_value from embedding_metadata where key='file_name'"
        rows = connection.execute(sql).fetchall()
        processed_files = [file_name for file_name, in rows]
    return processed_files

def get_vision_system_message()->str:
    system_message_text = '''
You're an expert image and photo analyzer.
You are very perceptive in analyzing images and photos. 
You possess excelent vision. 
Do not read any text unless it is the most prominent in the image. 
Your description should be neutral in tone.
'''
    return system_message_text

def get_object_system_message()->str:
    system_message_text = '''
You're an expert image and photo analyzer.
You are very perceptive in analyzing images and photos. 
You possess excelent vision. 
Do not read any text unless it is the most prominent in the image. 
You should always output your results in json format, for example:

[
 {'name': 'a detected object', 'description': 'the detected object's description'},
 {'name': 'another detected object', 'description': 'the other detected object's description'}
]
'''
    return system_message_text

def prompt_func(data):
    text = data["text"]
    image = data["image"]
    system_message = SystemMessage(content=data["system_message_text"])
    image_part = {
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{image}",
    }
    content_parts = []
    text_part = {"type": "text", "text": text}
    content_parts.append(image_part)
    content_parts.append(text_part)
    human_message = HumanMessage(content=content_parts)
    return [system_message, human_message]

def analyze_image(image_file, vision_chain, object_chain)->ImageDetails:
    start_time = time.time()
    model = vision_chain.steps[1].model
    with Image.open(image_file) as img: 

        print(f'PROCESSING FILE: {image_file}')
        print('CONVERTING TO B64...')
        image_b64 = convert_to_base64(img)
        print('OK')
        
        print('DETECTING OBJECTS...')
        detected_objects = object_chain.invoke({"text":"Identify objects in the image. Return a json list of json items of the detected objects. Include only the names of each object and a short description of the object. The field names should be 'name' and 'description' respectively.", "image": image_b64, "system_message_text":get_object_system_message()})
        print('OK')
        
        print('GENERATING DESCRIPTION...')
        image_description = vision_chain.invoke({"text": "Describe the image in as much detail as possible. Do not try to read any text.", "image": image_b64, "system_message_text":get_vision_system_message()})
        print('OK')

        print('CREATING OBJECT...')
        image_details = ImageDetailsFactory.create(image_file, img, detected_objects, image_description, model)
        print('OK')

        print('ADDING TO VECTOR STORE...')
        doc = Document(id=str(uuid.uuid4()), page_content=image_details.get_page_content(), metadata=image_details.to_dict())
        db.add_documents([doc])
        print('OK')

        print(f"{Fore.CYAN}Description:\n{Style.RESET_ALL}{image_details.description}")
        print(f"{Fore.CYAN}Detected Objects:\n{Style.RESET_ALL}{image_details.get_detected_objects_text()}")
        print('<=----------------------------------------------=>')

    end_time = time.time()
    execution_time = end_time - start_time
    print('\n')
    print(f"{Fore.YELLOW}Execution time: {execution_time:.4f} seconds{Style.RESET_ALL}")

    print(str(image_details))

    return image_details

if __name__ == '__main__':

    root_image_dir = os.getenv('ROOT_IMAGE_DIR')
    db_name = os.getenv('DB_NAME')
    db_collection_name = os.getenv('DB_COLLECTION_NAME')
    vision_model = os.getenv('VISION_MODEL')
    embedding_model = os.getenv('EMBEDDING_MODEL')

    image_files = get_jpeg_files(root_image_dir)
    embedding_function = OllamaEmbeddings(model=embedding_model)

    llm = ChatOllama(model=vision_model, temperature=0.2, num_gpu=-1)
    vision_chain = prompt_func | llm | StrOutputParser()
    object_chain = prompt_func | llm | JsonOutputParser()

    db = Chroma(
        collection_name=db_collection_name,
        embedding_function=embedding_function,
        persist_directory=f"./{db_name}")

    processed_files = get_processed_files()

    counter = 1;
    for file in image_files:
        print('---------------------------------------------------------------')
        print(f'{counter} / {len(image_files)}')
        print(file)
        print('\n\n')
        if file in processed_files:
            print(f'{Fore.LIGHTYELLOW_EX}FILE ALREADY PROCESSED, SKIPPED{Style.RESET_ALL}')
        else:
            analyze_image(file, vision_chain, object_chain)
        counter += 1