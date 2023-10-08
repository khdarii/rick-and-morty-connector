import requests
import json
from uuid import uuid4
from urllib.parse import urljoin
from datetime import datetime


class Fetcher:
    @staticmethod
    def fetch_data(url):
        """Fetches data from the specified URL and returns the JSON response."""
        response = requests.get(url)
        return response.json()


class DataProcessor:
    @staticmethod
    def process_and_write(data, filename_prefix):
        """Processes data and writes it to JSON files."""
        for item in data:
            processed_data = {
                'Id': str(uuid4()),
                'Metadata': item['name'],
                'RawData': item
            }
            write_to_json(f"{filename_prefix}_{item['id']}.json", processed_data)


class Logger:
    @staticmethod
    def filter_episodes_by_date(episodes, start_date, end_date):
        """Filters episodes based on air date, characters, and a date range."""
        filtered_episodes = [episode for episode in episodes
                             if start_date <= DateConverter.convert_api_date(episode['air_date']) <= end_date
                             and 'characters' in episode and len(episode['characters']) > 3]
        return filtered_episodes

    @staticmethod
    def log_episodes(episodes, start_year=2017, end_year=2021):
        """Logs episodes meeting specified criteria."""
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
        """Logs locations that appear only on odd episode numbers."""
        log_locations = [location['name'] for i, location in enumerate(locations, start=1) if i % 2 != 0]
        print("\nLocations that appear only on odd episode numbers:")
        print(log_locations)


class DateConverter:
    @staticmethod
    def convert_api_date(api_date):
        """Converts API date to a datetime object."""
        date_formats = ["%B %d, %Y", "%Y-%m-%d"]

        for date_format in date_formats:
            try:
                return datetime.strptime(api_date, date_format)
            except ValueError:
                pass

        print(f"Unable to parse date: {api_date}")
        return None


def write_to_json(filename, data):
    """Writes data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)


class RickAndMortyConnector:
    def __init__(self):
        self.api_base_url = 'https://rickandmortyapi.com/api/'
        self.characters_url = urljoin(self.api_base_url, 'character')
        self.locations_url = urljoin(self.api_base_url, 'location')
        self.episodes_url = urljoin(self.api_base_url, 'episode')

    @staticmethod
    def fetch_all_data(base_url):
        """Fetches all data from a paginated API endpoint."""
        all_data = []
        next_page = base_url

        while next_page:
            data_page = Fetcher.fetch_data(next_page)
            all_data.extend(data_page['results'])
            next_page = data_page['info']['next']

        return all_data

    def run(self):
        # Fetch all characters
        all_characters = self.fetch_all_data(self.characters_url)
        DataProcessor.process_and_write(all_characters, 'character')
        Logger.log_odd_locations(all_characters)

        # Fetch all locations
        all_locations = self.fetch_all_data(self.locations_url)
        DataProcessor.process_and_write(all_locations, 'location')
        # You can log or process locations as needed

        # Fetch all episodes
        all_episodes = self.fetch_all_data(self.episodes_url)
        DataProcessor.process_and_write(all_episodes, 'episode')
        Logger.log_episodes(all_episodes)


if __name__ == "__main__":
    connector = RickAndMortyConnector()
    connector.run()
