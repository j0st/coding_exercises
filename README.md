# Submission Coding Exercises
In this repo, you can find my submission for the coding tasks. The fine-tuning script for Task 1 can be found in `fine-tuning.ipynb`. How to start the frontend and backend server for Task 2 is explained in the next section.

**Note:** The weights of the fine-tuned model can be found at https://huggingface.co/jost/mistral7b_plantuml. To run the model in the backend, you require a GPU with cuda support. If a GPU is not available, a dummy PlantUML code is generated and displayed in the frontend. However, you can test the fine-tuned model in Google Colab with the free T4 GPU (as shown in `inference.ipynb`).

## Getting Started

1. **Clone the repository**:
    ```bash
    git clone https://github.com/j0st/coding_exercises
    cd <repository-directory>
    ```

2. **Set up the environment**:

    Ensure you have Python and Node.js installed and install dependencies.
   ```bash
    pip install -r requirements.txt
    ```
      
3. **Start backend server**:
    ```bash
    cd backend
    uvicorn app:app
    ```

4. **Start frontend server**:
    ```bash
    cd frontend/coding_exercises
    npm start
    ```
## Frontend Screenshot
![image](https://github.com/j0st/coding_exercises/assets/73901378/82dca4dc-bd1b-4de6-bde0-45bbef8fc7f4)

