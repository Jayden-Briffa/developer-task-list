"""Session 8 Faulty Parcel Delivery Calculator.

Version: 1.0
Purpose: Use this deliberately faulty program for testing and debugging.
Do not correct the code until instructed by the worksheet or recording.
"""

from outputs import outputError

STANDARD_PRICE = 3.50
HEAVY_PRICE = 5.50

def get_parcel_weight():
    """Ask the user for a parcel weight."""

    while True:
        parcel_weight = float(input("Enter the parcel weight in kg: "))

        if parcel_weight <= 0:
            outputError("Parcel weight be greater than 0")

        break

    return parcel_weight


def calculate_delivery_price(parcel_weight):
    """Select a delivery price from the parcel weight."""
    if parcel_weight < 2:
        return STANDARD_PRICE
    return HEAVY_PRICE


def display_summary(parcel_weight, delivery_price):
    """Display the delivery result."""
    print("Delivery Summary")
    print("Weight:", parcel_weight)
    print("Price:", delivery_price)


def main():
    print("Parcel Delivery Calculator - Test Version")
    parcel_weight = get_parcel_weight()
    delivery_price = calculate_delivery_price(parcel_weight)
    display_summary(parcel_weight, delivery_price)


if __name__ == "__main__":
    main()
