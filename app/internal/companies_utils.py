from fastapi import APIRouter, File, UploadFile
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from starlette.responses import HTMLResponse, JSONResponse
import csv, os, re
from ..dependencies import get_db
from ..models import Address, Company


router = APIRouter(prefix='/api')

@router.post("/import-from-csv/")
async def import_from_csv(db: Session = Depends(get_db), file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        return JSONResponse({'error': 'File type not supported'}, status_code=400)
    try:
        os.mkdir("uploads")
    except:
        print('folder already exists')
    file_name = os.getcwd()+"/uploads/"+file.filename.replace(" ", "-")
    with open(file_name,'wb+') as f:
        f.write(await file.read())
        f.close()
    customers = []
    with open(file_name, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if not row["Bill to 4"]:
                pattern_1 = re.compile(r"\d{5}")
                zip_code = pattern_1.findall(row["Bill to 3"])
                if len(zip_code) == 0:
                    zip_code = ''
                else:
                    zip_code = zip_code[0]
                pattern_2 = re.compile(r'^(.+?),')
                city = pattern_2.findall(row["Bill to 3"])
                if len(city) == 0:
                    city = None
                else:
                    city = city[0]
                pattern_3 = re.compile(r'[A-Z]{2}')
                state = pattern_3.findall(row["Bill to 3"])
                if len(state) == 0:
                    state = None
                else:
                    state = state[0]
                customers.append({
                    "name": row["Customer"],
                    "phone_number": "1" + row["Main Phone"].replace('-', ''),
                    "contact_email": row["Main Email"],
                    "address": {
                        "to_from": row["Bill to 1"],
                        "street": row["Bill to 2"],
                        "zip": zip_code,
                        "city": city,
                        "state": state
                    }
                })
    for customer in customers:
        company = Company(name=customer['name'], phone_number=customer['phone_number'], contact_email=customer['contact_email'])
        company.address = Address(**customer['address'])
        db.add(company)
        db.commit()
        db.refresh(company)
    return {'customers': customers}

@router.get("/upload-html/")
async def main():
    content = """
        <body>
        <form action="/api/import-from-csv/" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
        </form>
        </body>
    """
    return HTMLResponse(content=content)

