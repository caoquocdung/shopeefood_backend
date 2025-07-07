from fastapi import FastAPI

from routers import order, user, address, restaurant, category, menu_item, voucher, order_item, cart_item
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user.router)
app.include_router(address.router)
app.include_router(restaurant.router)
app.include_router(category.router)
app.include_router(menu_item.router)
app.include_router(voucher.router)
app.include_router(order.router)
app.include_router(order_item.router)
app.include_router(cart_item.router)