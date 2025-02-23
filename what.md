
# Image content processor one 

A copy of code from [Medium](https://medium.com/@dimosdennis/personal-photo-library-with-langchain-ollama-llava-fully-local-e82edfe07f54) article by Dimos Dennis
AI Summary of the solution:

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
   
Overall, the code aims to process a large number of photos by extracting and storing metadata, generating descriptions, and detecting objects using AI models. It runs locally on a mid-range gaming PC with appropriate hardware to handle the workload efficiently.
_(mid-range = Ryzen 5 5600X, 64GB RAM, RTX 4060 Ti 16GB)_