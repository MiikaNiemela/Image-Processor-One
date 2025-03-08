
# Image content identification test one 

The project starts as copy of Dimos Dennis's [Medium](https://medium.com/@dimosdennis/personal-photo-library-with-langchain-ollama-llava-fully-local-e82edfe07f54) article.

The article describes a solution, that can process a good lized library of images. It will extract and store metadata, generate a textual description of the picture and detecting objects using AI models. The models are run on locally on Ollama.

The solution, and the Ollama hosted models, should run without problems on a mid-range gaming PC. Definition of _mid-range = Ryzen 5 5600X, 64GB RAM, RTX 4060 Ti 16GB_. 

The outcome is to get a descriptive catalog of one's digital photo archive. And to have fun while doing it. 

## AI Summary of the solution:

1. **Initialization**:
   - The code initializes required packages: `langchain`, `langchain-chroma`, `langchain-ollama`, `pillow`, and `colorama`.

2. **Classes and Methods**:
   - **`ImageDetails` Class**: Stores image metadata such as file name, camera make, model, date taken, aperture value, focal length, exposure time, ISO, GPS coordinates, detected objects, and a description.
   - **Helper Functions**: Extract metadata, convert coordinates, and handle image processing.

3. **Image Processing**:
   - **`analyze_image` Function**: Processes each image, converting it to base64, detecting objects, generating descriptions, and saving metadata in a Chroma vector store.
   - **Object and Vision Chains**: Use Langchain models to analyze images.

4. **Execution**:
   - The main loop processes all JPEG images in the specified directory, skipping previously processed files and adding metadata to the Chroma vector store.

5. **Configuration and Setup**:
   - create `.env` file with proper values, like this:

   ```bash
      ROOT_IMAGE_DIR=X:\\\\photos\\1999 or /img/1999/
      DB_NAME=db_photos
      DB_COLLECTION_NAME=photo_collection
      VISION_MODEL=llava:13b
      EMBEDDING_MODEL=mxbai-embed-large
   ```

Start program with `python analyzer`.
