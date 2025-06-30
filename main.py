from fastapi import FastAPI

from routers import user, address, restaurant, category, menu_item 

app = FastAPI()

app.include_router(user.router)
app.include_router(address.router)
app.include_router(restaurant.router)
app.include_router(category.router)
app.include_router(menu_item.router)