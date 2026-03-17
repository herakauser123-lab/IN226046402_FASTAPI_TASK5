from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"}
]

orders = [
    {"order_id": 1, "customer_name": "Rahul Sharma"},
    {"order_id": 2, "customer_name": "Amit Patel"},
    {"order_id": 3, "customer_name": "Rahul Kumar"}
]

# ------------------- SEARCH -------------------
@app.get("/products/search")
def search_products(keyword: str):
    result = [p for p in products if keyword.lower() in p["name"].lower()]

    if not result:
        return {"message": f"No products found for: {keyword}"}

    return {"total_found": len(result), "products": result}


# ------------------- SORT -------------------
@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name"]:
        raise HTTPException(status_code=400, detail="sort_by must be 'price' or 'name'")

    result = sorted(products, key=lambda p: p[sort_by], reverse=(order == "desc"))

    return {"sort_by": sort_by, "order": order, "products": result}


# ------------------- PAGINATION -------------------
@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    total = len(products)

    return {
        "page": page,
        "limit": limit,
        "total_pages": -(-total // limit),
        "products": products[start:start + limit]
    }


# ------------------- Q4 -------------------
@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    result = [o for o in orders if customer_name.lower() in o["customer_name"].lower()]

    if not result:
        return {"message": f"No orders found for: {customer_name}"}

    return {"total_found": len(result), "orders": result}


# ------------------- Q5 -------------------
@app.get("/products/sort-by-category")
def sort_by_category():
    result = sorted(products, key=lambda p: (p["category"], p["price"]))

    return {"products": result}


# ------------------- Q6 -------------------
@app.get("/products/browse")
def browse(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = products

    if keyword:
        result = [p for p in result if keyword.lower() in p["name"].lower()]

    result = sorted(result, key=lambda p: p[sort_by], reverse=(order == "desc"))

    total = len(result)
    start = (page - 1) * limit

    return {
        "total_found": total,
        "total_pages": -(-total // limit),
        "products": result[start:start + limit]
    }


# ------------------- BONUS -------------------
@app.get("/orders/page")
def orders_page(page: int = 1, limit: int = 3):
    start = (page - 1) * limit

    return {
        "total": len(orders),
        "total_pages": -(-len(orders) // limit),
        "orders": orders[start:start + limit]
    }
