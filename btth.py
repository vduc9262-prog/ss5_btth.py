# from fastapi import FastAPI
# from pydantic import BaseModel,Field

# app = FastAPI()

# products = [

#     {"id": 1, "name": "Keyboard", "price": 500000},

#     {"id": 2, "name": "Mouse", "price": 300000}

# ]

# class CreateProduct(BaseModel):
#     id: int
#     name: str = Field(min_length=2)
#     price: float = Field(gt=0,lt=9000000)

# class UpdateProduct(BaseModel):
#     name : str
#     price: float


# @app.get('/')
# def get_root():
#     return{"message": "hiển thị danh sách"}

# @app.get('/products')
# def products():
#     return{
#         "data": products
#     }

# # Api lấy 1 sản phẩm theo id 
# @app.get('/product/{product_id}')
# def ID_product(product_id: int):
#     return{
#         "data":next((p for p in products if p["id"] == product_id),None)
#     }

# @app.get('/product')
# def get_product_by_price(start:float, end:float):
#     filter = []
#     for i in products:
#         if start < i["price"] < end:
#             filter.append(i)
#     if filter:
#         return{
#             "message":"tìm thấy",
#             "data" : filter
#         }
#     return{
#          "message":"ko  thấy",
#             "data" : None
#     }

# @app.post('/product')
# def post_product(new_product:CreateProduct):
#     products.append({
#         "id": new_product.id,
#         "name":new_product.name,
#         "price":new_product.price
#     })
#     return{
#         "message":"thêm sản phẩm thành công",
#         "data":new_product
#     }

# @app.put('/product/{product_id}')
# def update_products(product_id: int , update: UpdateProduct):
#     for pro in products:
#         if pro["id"] == product_id:
#             pro["name"] = update.name
#             pro["price"] = update.price
#             return{
#                 "message":"cập nhật thành công",
#                 "data":{
#                     "id":product_id,
#                     "name":update.name,
#                     "price":update.price
#                 }
#             }
#     return{
#         "message":"Sản phẩm ko tìm thấy để cập nhật",
#         "data":None
#     }


# @app.delete('/product/{product_id}')
# def delete_product(product_id:int):
#     for pro in products:
#         if pro["id"] == product_id:
#             products.remove(pro)
#             return{
#                 "message":"xóa thành công",
#                 "data":pro
#             }
#     return{
#         "message":"xóa ko thành công",
#         "data":None
#     }





from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products = [
    {"id": 1, "name": "Keyboard", "price": 500000},
    {"id": 2, "name": "Mouse", "price": 300000}
]


class ProductCreate(BaseModel):
    name: str
    price: float


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):

    if product.name.strip() == "":
        raise HTTPException(status_code=400,detail="Name cannot be empty")

    if product.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")

    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "price": product.price
    }

    products.append(new_product)

    return {"message": "tạo sản phẩm thành công ","data": new_product }


@app.get("/products")
def get_products():
    return products


@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            products.remove(product)

            return {
                "message": "xóa sản phẩm thành công"
            }

    return{ "message": "ko tìm thấy sản phẩm để xóa"}