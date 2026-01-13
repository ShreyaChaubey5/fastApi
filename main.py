from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json

app=FastAPI()

def load_data():
 with open('patient.json','r') as f:    
  data=json.load(f)
 return data

def save_data(data):
   with open('patient.json','w') as f:
      json.dump(data,f)

class Patient(BaseModel):
   id:Annotated[str,Field(..., description='Id of patient')]
   name:Annotated[str,Field(...,description='name of the patient')]
   age:Annotated[int,Field(...,gt=0,lt=180,description='Age of the patient' )]
   gender:Annotated[Literal['male','female','other'],Field(...,description='gender of the patient')]
   height:Annotated[float,Field(..., gt=0, description='height of patient in m')]
   weight:Annotated[float,Field(...,gt=0,description='weight of patient')]
   city:Annotated[str,Field(...,description='city where the patient live')]
   @computed_field
   @property
   def bmi(self)->float:
      bmi=round(self.weight/(self.height**2))
      return bmi 

class updatePatient(BaseModel):
  name:Annotated[Optional[str],Field(default=None)]
  age:Annotated[Optional[int],Field(gt=0,lt=180,default=None )]
  gender:Annotated[Optional[Literal['male','female','other']],Field(default=None)]
  height:Annotated[Optional[float],Field(gt=0, default=None)]
  weight:Annotated[Optional[float],Field(gt=0,default=None)]
  city:Annotated[Optional[str],Field(default=None)]






@app.get("/")
def hello():
    return {'message':'Patient management system API'}

@app.get("/about")
def about():
    return {'message':'A fully functional API to manage your patient record'}

@app.get("/views")
def view():
  data=load_data()
  return data


@app.get("/views/{patient_id}")
def view_patient(patient_id:str=Path(...,description= 'ID of the patient in DB')):
  data=load_data()
  for patient in data:
   if patient.get("patient_id") == patient_id:
            return patient 
  raise HTTPException(status_code=404,detail='Patient not found')

@app.get("/sort")
def sort_patients(sort_by:str=Query(...,description='sort on the basis of query'),
                  order:str=Query('asc',description='sort by ascending or descending order')):
   
   valid_fields=['height','weight','bmi']

   if sort_by not in valid_fields:
      raise HTTPException(status_code=400,detail='invalid field')
   
   if order not in ['asc','desc']:
      raise HTTPException(status_code=400,detail='invalid order select between scending and descending')
   
   data=load_data()
   
   sort_order=True if order=='desc' else False
   sorted_data=sorted(data.value(),key=lambda x:x.get(sort_by,0),reverse=sort_order)

   return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    # load existing data
    data = load_data()

    # check if this patient exist or not
    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail="Patient already exists"
        )

    # store the patient in db
    data[patient.id] = patient.model_dump(exclude={"id"})

    # save data
    save_data(data)

    return JSONResponse(status_code=200,content='patient is created successfully')

#update route
#in update route I make another model excluding id 
@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:updatePatient):
   data=load_data()

   if patient_id not in data:
      raise HTTPException(status_code=404,detail='patient not found')
   
   existing_patient_info=data[patient_id]

   updated_patient_info=patient_update.model_dump(exclude_unset=True)
     #find which key value pair is updated
   for key,value in updated_patient_info.items():
      existing_patient_info[key]=value
      #add id so that we can convert t into Patient class for updated bmi
   existing_patient_info['id']=patient_id
      #conversion into patient
   patient_pydantic_obj=Patient(**existing_patient_info)
      #convert into disc
   existing_patient_info=patient_pydantic_obj.model_dump(exclude={'id'})
      #add into existing data basically her update
   data[patient_id]=existing_patient_info
      #save the data
   save_data(data)

   return JSONResponse(status_code=200,content='info updated successfully')


       