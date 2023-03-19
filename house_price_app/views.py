import os

from django.conf import settings
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import redirect, render
from google.oauth2 import service_account
from googleapiclient.discovery import build

from .models import House


def input_form_view(request):
    return render(request, "input_form.html")


def get_google_sheets_service():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, "credentials.json")

    credentials = service_account.from_service_account_file(
        SERVICE_ACCOUNT_FILE, SCOPES
    )
    service = build("sheets", "v4", credentials=credentials)
    return service


def calculate_estimate(request):
    if request.method == "POST":
        # Extract form data
        city = request.POST["city"]
        neighborhood = request.POST["neighborhood"]
        square_meters = float(request.POST["square_meters"])
        bedrooms = int(request.POST["bedrooms"])
        bathrooms = int(request.POST["bathrooms"])
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        name = request.POST["name"]
        last_name = request.POST["last_name"]

        # Add a filter for square_meters (you can adjust the range as needed)
        min_square_meters = square_meters * 0.9
        max_square_meters = square_meters * 1.1

        houses = House.objects.filter(
            city=city,
            neighborhood=neighborhood,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            square_meters__range=(min_square_meters, max_square_meters),
        )
        mean_rent_price = houses.aggregate(Avg("price"))["price__avg"]
        estimated_cost = mean_rent_price * 220

        # Save the user's contact information to the Google Sheet
        sheet_id = "1xyN5TMmobavFU80tmGfB-2IRb3C5ZaKvp4EbfMZDgog"
        sheet_range = "Sheet1!A1"
        service = get_google_sheets_service()

        values = [
            [
                name,
                last_name,
                email,
                phone_number,
                city,
                neighborhood,
                square_meters,
                bedrooms,
                bathrooms,
                estimated_cost,
            ]
        ]
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=sheet_id,
                range=sheet_range,
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body=body,
            )
            .execute()
        )

        # Render the result in a new template
        context = {"estimated_cost": estimated_cost}
        return render(request, "result.html", context)

    return redirect("input_form")
