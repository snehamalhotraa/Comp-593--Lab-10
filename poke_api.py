'''
Authors: Mahenur Master, Nisharg Patel, Sneha Malhotra, Siddharth Patel 
Library for interacting with the PokeAPI.
https://pokeapi.co/
'''
import requests
import os
import image_lib

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Initial test of the get_pokemon_info() function
    # You can inspect the returned dictionary with breakpoints
    pokemon_details = get_pokemon_info("Rockruff")
    fetch_pokemon_names()
    return

def get_pokemon_info(pokemon):
    """Retrieves data about a specific Pokemon from the PokeAPI.

    Args:
        pokemon (str): Name or Pokedex number of the Pokemon

    Returns:
        dict: A dictionary with the Pokemon's information, if successful. Otherwise, None.
    """
    # Prepare the Pokemon name by:
    # - Ensuring it's a string,
    # - Stripping whitespace at the start/end, and
    # - Converting it to lowercase
    pokemon = str(pokemon).strip().lower()

    # Verify that the Pokemon name isn't empty
    if not pokemon:
        print('Error: Pokemon name is missing.')
        return

    # Make a GET request to fetch the Pokemon info
    print(f'Retrieving data for {pokemon.capitalize()}...', end='')
    url = f"{POKE_API_URL}{pokemon}"
    response = requests.get(url)

    # Verify if the request was successful
    if response.status_code == requests.codes.ok:
        print('Success')
        # Return the Pokemon info as a dictionary
        return response.json()
    else:
        print('Failed')
        print(f'Status code: {response.status_code} ({response.reason})')

    # TODO: Implement a function to retrieve a list of all Pokemon names from the PokeAPI

def fetch_pokemon_names(limit=100000, offset=0):
    print(f'Retrieving Pokemon names list....', end='')
    params = {
        'limit': limit,
        'offset': offset
    }
    response = requests.get(POKE_API_URL, params=params)
    if response.status_code == requests.codes.ok:
        print('Success')
        response_data = response.json()
        return [pokemon['name'] for pokemon in response_data['results']]
    else:
        print('Failed')
        print(f'Status code: {response.status_code} ({response.reason})')
        return []

    # TODO: Implement a function that downloads and saves Pokemon artwork
def download_pokemon_artwork(pokemon_name, folder_path='.'):
    pokemon_details = get_pokemon_info(pokemon_name)
    if pokemon_details is None:
        return

    # Get the artwork URL from the Pokemon's details
    artwork_url = pokemon_details['sprites']['other']['official-artwork']['front_default']
    if artwork_url is None:
        print(f"No artwork available for {pokemon_name.capitalize()}.")
        return

    # Create the file path for the image
    file_extension = artwork_url.split('.')[-1]
    image_path = os.path.join(folder_path, f'{pokemon_name}.{file_extension}')

    # Skip downloading if the artwork already exists
    if os.path.exists(image_path):
        print(f'Artwork already exists for {pokemon_name.capitalize()}.')
        return

    print(f'Downloading artwork for {pokemon_name.capitalize()}...', end='')
    image_content = image_lib.download_image(artwork_url)
    if image_content is None:
        return

    # Save the image file
    if image_lib.save_image_file(image_content, image_path):
        print(f'Artwork successfully saved to {image_path}.')
        return image_path

if __name__ == '__main__':
    main()
