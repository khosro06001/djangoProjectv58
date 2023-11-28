from django.shortcuts import render, redirect
# Make sure to install requests using 'pip install requests' on your terminal, otherwise 'requests' will not work
import requests
from datetime import datetime
from django.contrib import messages


def index_old(request):
    # if the request method is a post
    if request.method == 'POST':
        # get the search term and location
        number_of_users = request.POST['number-of-users']
        gender = request.POST['gender']

        # Check if either number_of_users or gender is empty
        if not number_of_users or not gender:
            # Set up an error message using Django's message utility to inform the user
            messages.info(request, 'Both number of users and gender are required fields.')
            # redirect user to the index page
            return redirect('randomuser-index')
            # Add code to handle or display the error_message as needed.

        # call get_random_users function() to get the data from the API
        random_female_users = get_random_users(number_of_users, gender, nationality='us')

        # If the request to fetch data from randomuser was unsuccessful or returned None
        if random_female_users is None:
            # Set up an error message using Django's message utility to inform the user
            messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
            # redirect user to the index page
            return redirect('randomuser-index')

        else:
            # print the response for testing purpose (open "Run" at the bottom to see what is printed)
            print(random_female_users)
            # Store each user's information in a variable
            users = random_female_users['results']

            # Initialize an empty list to store user data
            user_list = []

            # Iterate through each user in the 'users' list coming from the api
            # Rather than directly passing the "users" array to the template,
            # the following approach allows server-side processing and formatting of specific data (e.g., date).
            # So, the template only needs to plug in the preprocessed information.
            for user in users:
                # Extract relevant information from the user dictionary
                first_name = user['name']['first']
                last_name = user['name']['last']
                email = user['email']
                phone = user['phone']
                picture = user['picture']['large']
                registration_date = user['registered']['date']

                # Format the registration date from "2004-03-12T17:05:44.193Z" to "2004"
                # Extract the first 10 characters to get the date portion, then convert to a datetime object
                date_object = datetime.strptime(registration_date[:10], "%Y-%m-%d")

                # Format the date object to a more readable format, e.g., "Sat Nov 03 2023"
                registration_date = date_object.strftime("%a %b %d %Y")

                # Create a new dictionary to store user details
                user_details = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                    'picture': picture,
                    'registration_date': registration_date
                }

                # Append the user details dictionary to the user_list
                user_list.append(user_details)

            # Create a context dictionary with the user_list and render the 'index2.html' template
            context = {'users': user_list}
            return render(request, 'randomuser/index2.html', context)

    # all other cases, just render the page without sending/passing any context to the template
    return render(request, 'randomuser/index2.html')


def get_random_users(number_of_users, gender, nationality):
    try:
        # Construct the URL with parameters
        url = "https://randomuser.me/api/"

        # The query parameters will be appended to the url such as https://randomuser.me/api/?results=5&gender=female&nat=us
        params = {
            "results": number_of_users,
            "gender": gender,
            "nat": nationality
        }

        # Send a GET request to the specified URL with parameters
        response = requests.get(url, params=params)

        # Raise an exception for 4xx and 5xx status codes
        response.raise_for_status()

        # Parse the JSON data from the response
        data = response.json()

        # Return the parsed data
        return data
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, timeouts)
        print(f"Request failed: {e}")

        # Return None to indicate failure
        return None



def index(request):
    # if the request method is a post
    if request.method == 'POST':
        # get the search term and location
        # number_of_users = request.POST['number-of-users']
        # gender = request.POST['gender']

        # later change the form and the words used here for the query request...
        events = request.POST['events']
        city = request.POST['city']

        # Check if either number_of_users or gender is empty
        # if not number_of_users or not gender:
        #     # Set up an error message using Django's message utility to inform the user
        #     messages.info(request, 'Both number of users and gender are required fields.')
        #     # redirect user to the index page
        #     return redirect('randomuser-index')
        #     # Add code to handle or display the error_message as needed.

        # Construct the URL with parameters
        # url = "https://randomuser.me/api/"

        # The query parameters will be appended to the url such as https://randomuser.me/api/?results=5&gender=female&nat=us
        # params = {
        #     "results": number_of_users,
        #     "gender": gender,
        #     "nat": nationality
        # }

        # params = {
        #     "results": number_of_users,
        #     "gender": gender,
        #     "nat": nationality
        # }

        # url = "https://app.ticketmaster.com/discovery/v2/events.json"
        # # apikey = 'BSQwvGEqBVyuq8qtKajfgDTwfuufWVUX'
        # apikey = 'BSQwvGEqBVyuq8qtKajfgDTwfuufWVUX'
        #
        # params = {
        #     "apikey": apikey,
        #     "city" : city,
        #     "classificationName": events
        # }
        #
        # # Send a GET request to the specified URL with parameters
        # response = requests.get(url, params=params)
        #
        #
        # # Parse the JSON data from the response
        # total_events = response.json()


        apikey = 'OFYGvXGLUFanaijTT1jpItQsJ5Ayf3c8'
        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            "apikey": apikey,
            "classificationName": events,
            "city": city,
            "sort": "date,asc",
        }
        ### response = requests.get(url, params=params)
        ### response = requests.post(url, params=params)
        ### response = requests.get('https://app.ticketmaster.com/discovery/v2/events.json?apikey=OFYGvXGLUFanaijTT1jpItQsJ5Ayf3c8')
        ### response = requests.get('https://app.ticketmaster.com/discovery/v2/events.json?apikey=OFYGvXGLUFanaijTT1jpItQsJ5Ayf3c8' , params=params)

        # print(request)
        # return JsonResponse({"value": request })

        ### response = requests.get(url, params=params) ############# get or post???
        response = requests.get(url, params=params)
        ### response = requests.get(url, params=params)

        total_events = response.json()


        ### now PARSE IT!!!
        event_list = []

        for event in total_events['_embedded']['events']:
            event_name = event['name']
            ticket_link = event['url']
            event_id = event['id']
            image_url = event['images'[0]['url']]
            venue_name = event['_embedded']['venues'][0]['name']
            venue_address = event['_embedded']['venues'][0]['address']['line1']
            venue_city = event['_embedded']['venues'][0]['city']['name']
            venue_state = event['_embedded']['venues'][0]['state']['name']
            event_datetime = event['dates']['start']['dateTime']
            event_item = {
                'eventName': event_name,
                'ticketLink': ticket_link,
                'eventID': event_id,
                'imageUrl': image_url,
                'venueName': venue_name,
                'venueAddress': venue_address,
                'venueCity': venue_city,
                'venueState': venue_state,
                'eventDate': event_datetime,
                'eventTime': event_datetime,
            }
            event_list.append(event_item)

        context = {'events': event_list}
        # return render(request, 'ticketmaster.html', context)
        return render(request, 'index.html', context)

        # call get_random_users function() to get the data from the API
        # random_female_users = get_random_users(number_of_users, gender, nationality='us')
        #
        # # If the request to fetch data from randomuser was unsuccessful or returned None
        # if random_female_users is None:
        #     # Set up an error message using Django's message utility to inform the user
        #     messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
        #     # redirect user to the index page
        #     return redirect('events-index')
        #
        # else:
        #     # print the response for testing purpose (open "Run" at the bottom to see what is printed)
        #     print(random_female_users)
        #     # Store each user's information in a variable
        #     users = random_female_users['results']



    # if the request method is not post
    # all other cases, just render the page without sending/passing any context to the template
    return render(request, 'randomuser/index.html')

# def get_events(number_of_users, gender, nationality):
#     try:
#         # Construct the URL with parameters
#         def get_random_users(number_of_users, gender, nationality):
#             try:
#                 # Construct the URL with parameters
#                 url = "https://randomuser.me/api/"
#
#                 # The query parameters will be appended to the url such as https://randomuser.me/api/?results=5&gender=female&nat=us
#                 params = {
#                     "results": number_of_users,
#                     "gender": gender,
#                     "nat": nationality
#                 }
#
#                 # Send a GET request to the specified URL with parameters
#                 response = requests.get(url, params=params)
#
#                 # Raise an exception for 4xx and 5xx status codes
#                 response.raise_for_status()
#
#                 # Parse the JSON data from the response
#                 data = response.json()
#
#                 # Return the parsed data
#                 return data
#             except requests.exceptions.RequestException as e:
#                 # Handle request exceptions (e.g., network issues, timeouts)
#                 print(f"Request failed: {e}")
#
#                 # Return None to indicate failure
#                 return None
#
#         # Return the parsed data
#         return data
#     except requests.exceptions.RequestException as e:
#         # Handle request exceptions (e.g., network issues, timeouts)
#         print(f"Request failed: {e}")
#
#         # Return None to indicate failure
#         return None
#

