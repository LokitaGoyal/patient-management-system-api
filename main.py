# # ---------------------------  HTTP methods------------------------
# # GET - To get data from the server
# # POST - To send data to the server
# # PUT - To update data on the server
# # DELETE - To delete data from the server

from fastapi import FastAPI , Path , HTTPException , Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Annotated , Literal, Optional
import json

app = FastAPI()

#---------------------------Patient Model-----------------------------
class Patient(BaseModel):

    id : Annotated[str , Field(..., description= "ID of the patient" , example = "P001")]
    name : Annotated[str , Field(...,description = "Name of the patient" , example = "lokita")]
    city : Annotated[str , Field(..., description = "City where patient lives" , example = "Noida")]
    age : Annotated[int , Field(... , gt = 0 , lt = 120 , description = "Age of the patient")]
    gender : Annotated[Literal["female", "male", "other"], Field(..., description = "Gender of the patient")]
    height : Annotated[float , Field(... , gt = 0 , description = "Height of the patient in mtrs")]
    weight : Annotated[float , Field(... , gt = 0 , description = "Weight of the patient in kgs")]

    # computed fields for bmi
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2), 2)
        return bmi
    
    # computed fields for verdict
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return"Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

#---------------------------Patient Update Model-----------------------------        
class PatientUpdate(BaseModel):
    name : Annotated[Optional[str], Field(default=None)]
    city : Annotated[Optional[str], Field(default=None)]
    age : Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender : Annotated[Optional[Literal["female", "male", "other"]], Field(default=None)]
    height : Annotated[Optional[float], Field(default=None, gt=0)]
    weight : Annotated[Optional[float], Field(default=None, gt=0)]

# Load patient data from JSON file
def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    
    return data

#save patient data to JSON file
def save_data(data):    
    with open("patients.json", "w") as f:
        json.dump(data, f)

#---------------------------Home page-----------------------------
@app.get("/")
def home():
    return {"message": "Patient management sysytem api is running."}

#---------------------------About the api-----------------------------
@app.get("/about")
def about():
    return {"message": "A fully functional api to manage your patients records."}

#---------------------------View all patients-----------------------------
@app.get("/patients")
def patients():
    data = load_data() 
    return data

#---------------------------View patient by id-----------------------------
@app.get("/patients/{patient_id}")
def view_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    return data[patient_id]

#---------------------Search Patient by Name or City----------------------

@app.get("/patients/search")
def search_patient(name: Optional[str] = Query(None),city: Optional[str] = Query(None)):
    
    data = load_data()

    result = {}

    for patient_id, patient in data.items():

        if name and patient["name"].lower() == name.lower():
            result[patient_id] = patient

        elif city and patient["city"].lower() == city.lower():
            result[patient_id] = patient

    if not result:
        raise HTTPException(status_code=404, detail="Patient not found")

    return result

#---------------------Patient Statistics----------------------
@app.get("/patients/stats")
def patient_statistics():

    data = load_data()

    total = len(data)

    total_bmi = 0

    underweight = 0
    normal = 0
    overweight = 0
    obese = 0

    for patient in data.values():

        total_bmi += patient["bmi"]

        if patient["verdict"] == "Underweight":
            underweight += 1

        elif patient["verdict"] == "Normal weight":
            normal += 1

        elif patient["verdict"] == "Overweight":
            overweight += 1

        else:
            obese += 1

    average_bmi = round(total_bmi / total, 2) if total else 0

    return {
        "Total Patients": total,
        "Average BMI": average_bmi,
        "Underweight": underweight,
        "Normal": normal,
        "Overweight": overweight,
        "Obese": obese
    }

#---------------------Sort Patients----------------------
@app.get("/patients/sort")
def sort_patients(sort_by: str = Query(..., description="sort on the basis of height, weight or bmi"), order: str = Query("asc", description="sort in ascending or descending order")):
   
    data = load_data()

    valid_fields = ["height", "weight", "bmi"]
    valid_orders = ["asc", "desc"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid sort_by parameter")
    
    if order not in valid_orders:
        raise HTTPException(status_code=400, detail="Invalid order parameter select between asc or desc ")
    
    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.items(), key=lambda x: x[1].get(sort_by , 0), reverse=sort_order)

    return sorted_data

#---------------------------Create Patient-----------------------------
@app.post("/patients")
def create_patient(patient: Patient):

    #load existing data
    data = load_data()

    #check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient with this id already exists")
    
    #add new patient to data if not exists
    data[patient.id] = patient.model_dump(exclude=['id'])

    #save updated data to json file
    save_data(data)

    return JSONResponse(content={"message": "Patient created successfully"}, status_code=201)

#---------------------------Update Patient data-----------------------------
@app.put("/patients/{patient_id}")
def update_patient(patient_id : str , patient_update : PatientUpdate):
    
    #load existing data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    #update patient data
    existing_patient_info = data[patient_id] #contains all fields

    #create a new patient object with updated data and convert it to a dictionary
    updated_patient_info = patient_update.model_dump(exclude_unset=True) #contains only updated fields

    for key , value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi and verdict
    existing_patient_info["id"] = patient_id

    # pydantic model -> dictionary
    existing_patient_info = Patient(**existing_patient_info).model_dump(exclude=['id'])   

    #add this dictionary to the data
    data[patient_id] = existing_patient_info

    #save updated data to json file
    save_data(data)

    return JSONResponse(content={"message": "Patient updated successfully"}, status_code=200)

#---------------------------Delete Patient data-----------------------------
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):

    #load existing data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code = 404, detail = "Patient not found")
        
    del data[patient_id]

    #save updated data to json file
    save_data(data)

    return JSONResponse(content={"message": "Patient deleted successfully"}, status_code=200)