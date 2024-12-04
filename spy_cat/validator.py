import requests
from django.core.exceptions import ValidationError


class RequestError(Exception):
    pass


def get_cat_breed_names():
    try:
        response = requests.get("https://api.thecatapi.com/v1/breeds")
        response.raise_for_status()
        breeds = [breed["name"] for breed in response.json()]
        return breeds
    except requests.exceptions.RequestException as e:
        raise RequestError(f"Failed to fetch cat breeds: {str(e)}")


def validate_cat_breed(user_breed):
    if not user_breed:
        raise ValidationError("Breed cannot be empty.")

    valid_breeds = get_cat_breed_names()
    if user_breed not in valid_breeds:
        raise ValidationError(
            f"Invalid breed: {user_breed}. Valid breeds are: {', '.join(valid_breeds)}"
        )
