from time import sleep
from Verifyscanner.comparison import comparison
from Verifyscanner.connect_to_database import connect_to_database, close_database_connection
from datetime import date
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse            
from django.urls import reverse
from django.http import request  # Import the request object from Django




# display = DisplayOnLCD()

def get_data_from_database():
    connection = connect_to_database()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, first_name, fingerprint_xtics FROM public.freedom_voters")
                voters = cursor.fetchall()
                return voters
        except Exception as e:
            print(f"Error fetching data from the database: {str(e)}")
        finally:
            close_database_connection(connection)

    return None



# if __name__ == "__main__":
#     main()