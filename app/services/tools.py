
def calculate_total(price: float, quantity: int) -> dict:
    """Calculate the total price for a given quantity."""
    if price < 0:
        raise ValueError("Price cannot be negative")

    if quantity < 0:
        raise ValueError("Quantity cannot be negative")

    total = price * quantity

    return {
        "price": price,
        "quantity": quantity,
        "total": round(total, 2),
    }


def get_server_status(service_name: str) -> dict:
    """Return sample status information for a service."""
    return {
        "service": service_name,
        "status": "healthy",
        "message": f"{service_name} is running",
    }
