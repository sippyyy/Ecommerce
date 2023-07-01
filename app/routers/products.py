from fastapi import APIRouter,HTTPException,Depends,status,Form,UploadFile,File
from sqlalchemy.orm import Session
from app import models,database,oauth2
from app.Schema.product import Product
from secrets import token_hex
routers =  APIRouter(
    prefix='/products',
    tags=['products']
)


@routers.get('/',status_code=status.HTTP_200_OK)
def get_products(db:Session = Depends(database.get_db)):
    return {"message": "Hello World"}


@routers.post('/',status_code=status.HTTP_201_CREATED)
async def create_product(product_name: str = Form(...),
                   price: float = Form(...),
                   product_type: str  = Form(...),
                   detail: str = Form(...),
                   quantity: int = Form(...),
                   image: UploadFile | None = None,
                   db:Session=Depends(database.get_db),
                   current_user=Depends(oauth2.get_current_user)):
    image_ext = image.filename.split(".").pop()
    image_name = token_hex(10)
    image_path = f"{image_name}.{image_ext}"
    with open(image_path,"wb") as f:
        content = await image.read()
        f.write(content)
    new_product = models.Products(
        product_name=product_name,
        price=price,
        product_type=product_type,
        detail=detail,
        quantity=quantity,
        image=image_path
    )
    db.add(new_product)
    db.commit()
    return {"message": "Create product successfully"}
