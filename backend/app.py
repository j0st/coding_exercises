import tempfile

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from peft import AutoPeftModelForCausalLM
from plantuml import PlantUML
from pydantic import BaseModel
from transformers import AutoTokenizer

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows requests from React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Class for the user input
class InputData(BaseModel):
    prompt: str

# Class for the LLM response
class OutputData(BaseModel):
    response: str

# Endpoint for querying the LLM
@app.post("/generate", response_model=OutputData)
def generate(input_data: InputData):
    template = f"[INST] {input_data.prompt} [/INST]" # Bring user input into Mistral 7B format
    
    try: # If GPU available
        model = AutoPeftModelForCausalLM.from_pretrained("jost/mistral7b_plantuml", load_in_4bit = True)
        tokenizer = AutoTokenizer.from_pretrained("jost/mistral7b_plantuml")

        inputs = tokenizer([template], return_tensors = "pt").to("cuda")
        outputs = model.generate(**inputs, max_new_tokens = 500, use_cache = True)
        full_response = tokenizer.batch_decode(outputs) # Returns the prompt as well
    
        response = full_response[0].replace(template, "") # Remove the prompt
        result = response[4:-4] # Remove special tokens (<s> and </s>)

    except Exception as e: # If no GPU is found, the web app runs in "demo" mode and returns a dummy UML code (this is the generatd example from inference.ipynb)
        result = """@startuml\nactor "Front Desk Staff" as FDS\nactor Patient as P\nparticipant "Healthcare System" as HS\n\nFDS -> P: Welcomes patient and requests information\nactivate FDS\nactivate P\nP --> FDS: Provides basic information\ndeactivate P\nFDS -> HS: Enters patient\'s information\nactivate HS\nHS --> FDS: Validates information\ndeactivate HS\nFDS -> FDS: Corrects information if necessary\nFDS -> HS: Generates unique patient identification number\nactivate HS\nHS --> FDS: Provides identification number\ndeactivate HS\nFDS -> P: Provides registration documents and instructions\nactivate P\nP --> FDS: Thanks and proceeds accordingly\ndeactivate P\ndeactivate FDS\n\nalt Existing patient information\nFDS -> HS: Alerts patient about existing record\nactivate HS\nHS --> FDS: Instructions for updating existing record\ndeactivate HS\n\nalt Technical issues\nFDS -> FDS: Informs patient about technical issue\nFDS -> FDS: Records information manually\nFDS -> HS: Transfers manually recorded information\nactivate HS\nHS --> FDS: Confirmation of transferred information\ndeactivate HS\n\n@enduml"""
        print(e)

    app.uml_code = result

    return OutputData(response=result)

# Endpoint for converting PlantUML code to a diagram
@app.post("/convert-to-diagram")
def convert_to_diagram():
    # Create a temporary .puml file from the generated PlantUML code
    with tempfile.NamedTemporaryFile(suffix='.puml', delete=False) as temp_file:
        temp_file.write(app.uml_code.encode('utf-8'))
        temp_file_name = temp_file.name

    # Send .puml file to PlantUML server which returns a diagram as .png
    server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
    output_file = "uml_diagram.png"
    server.processes_file(temp_file_name, output_file)

    return FileResponse(output_file)
