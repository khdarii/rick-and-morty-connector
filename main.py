import requests
import json
from uuid import uuid4
from urllib.parse import urljoin
from datetime import datetime


class Fetcher:
    @staticmethod
    def fetch_data(url):
        response = requests.get(url)
        return response.json()


class DataProcessor:
    @staticmethod
    def process_and_write(data, filename_prefix):
        for item in data:
            processed_data = {
                'Id': str(uuid4()),
                'Metadata': item['name'],
                'RawData': item
            }
            write_to_json(f"{filename_prefix}_{item['id']}.json", processed_data)


class DateConverter:
    @staticmethod
    def convert_api_date(api_date):
        try:
            return datetime.strptime(api_date, "%B %d, %Y")
        except ValueError:
            try:
                return datetime.strptime(api_date, "%Y-%m-%d")
            except ValueError:
                print(f"Unable to parse date: {api_date}")
                return None


class Logger:
    @staticmethod
    def filter_episodes_by_date(episodes, start_date, end_date):
        filtered_episodes = [episode for episode in episodes
                             if start_date <= DateConverter.convert_api_date(episode['air_date']) <= end_date
                             and len(episode['characters']) > 3]
        return filtered_episodes

    @staticmethod
    def log_episodes(episodes, start_year=2017, end_year=2021):
        try:
            start_date = datetime(start_year, 1, 1)
            end_date = datetime(end_year, 12, 31)
            if start_date >= end_date:
                raise ValueError("Start year should be before the end year.")
        except ValueError as e:
            print(f"Error: {e}")
            return

        filtered_episodes = Logger.filter_episodes_by_date(episodes, start_date, end_date)

        print("Episodes meeting the criteria:")
        print([episode['name'] for episode in filtered_episodes])

    @staticmethod
    def log_odd_locations(locations):
        log_locations = [location['name'] for i, location in enumerate(locations, start=1) if i % 2 != 0]
        print("\nLocations that appear only on odd episode numbers:")
        print(log_locations)


def write_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)


class RickAndMortyConnector:
    def __init__(self):
        self.api_base_url = 'https://rickandmortyapi.com/api/'

        # Joining URLs using urljoin
        self.characters_url = urljoin(self.api_base_url, 'character')
        self.locations_url = urljoin(self.api_base_url, 'location')
        self.episodes_url = urljoin(self.api_base_url, 'episode')

    def run(self):
        fetcher = Fetcher()

        # Fetch data for characters, locations, and episodes
        characters = fetcher.fetch_data(self.characters_url)['results']
        locations = fetcher.fetch_data(self.locations_url)['results']
        episodes = fetcher.fetch_data(self.episodes_url)['results']

        # Process and write data to JSON files
        DataProcessor.process_and_write(characters, 'character')
        DataProcessor.process_and_write(locations, 'location')
        DataProcessor.process_and_write(episodes, 'episode')

        # Log information with default year values
        Logger.log_episodes(episodes)
        Logger.log_odd_locations(locations)


if __name__ == "__main__":
    connector = RickAndMortyConnector()
    connector.run()
