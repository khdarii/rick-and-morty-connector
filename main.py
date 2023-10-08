import asyncio
import json
from datetime import datetime
from urllib.parse import urljoin
from uuid import uuid4

import requests


class Fetcher:
    @staticmethod
    async def fetch_data(url):
        """Fetches data from the specified URL and returns the JSON response."""
        response = requests.get(url)
        return response.json()


class DataProcessor:
    @staticmethod
    async def process_and_write(data, filename_prefix):
        """Processes data and writes it to JSON files."""
        for item in data:
            processed_data = {
                'Id': str(uuid4()),
                'Metadata': item['name'],
                'RawData': item
            }
            await write_to_json(f"{filename_prefix}_{item['id']}.json", processed_data)


class Logger:
    @staticmethod
    async def filter_episodes_by_date(episodes, start_date, end_date):
        """Filters episodes based on air date, characters, and a date range."""
        filtered_episodes = [episode for episode in episodes
                             if start_date <= await DateConverter.convert_api_date(episode['air_date']) <= end_date
                             and 'characters' in episode and len(episode['characters']) > 3]
        return filtered_episodes

    @staticmethod
    async def log_episodes(episodes, start_year=2017, end_year=2021):
        """Logs episodes meeting specified criteria."""
        try:
            start_date = datetime(start_year, 1, 1)
            end_date = datetime(end_year, 12, 31)
            if start_date >= end_date:
                raise ValueError("Start year should be before the end year.")
        except ValueError as e:
            print(f"Error: {e}")
            return

        filtered_episodes = await Logger.filter_episodes_by_date(episodes, start_date, end_date)

        print("Episodes meeting the criteria:")
        print([episode['name'] for episode in filtered_episodes])

    @staticmethod
    async def log_odd_locations(locations):
        """Logs locations that appear only on odd episode numbers."""
        log_locations = [location['name'] for i, location in enumerate(locations, start=1) if i % 2 != 0]
        print("\nLocations that appear only on odd episode numbers:")
        print(log_locations)


class DateConverter:
    @staticmethod
    async def convert_api_date(api_date):
        """Converts API date to a datetime object."""
        date_formats = ["%B %d, %Y", "%Y-%m-%d"]

        for date_format in date_formats:
            try:
                return datetime.strptime(api_date, date_format)
            except ValueError:
                pass

        print(f"Unable to parse date: {api_date}")
        return None


async def write_to_json(filename, data):
    """Writes data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)


class RickAndMortyConnector:
    def __init__(self):
        self.api_base_url = 'https://rickandmortyapi.com/api/'
        self.characters_url = urljoin(self.api_base_url, 'character')
        self.locations_url = urljoin(self.api_base_url, 'location')
        self.episodes_url = urljoin(self.api_base_url, 'episode')

    async def fetch_and_process_characters(self):
        all_characters = await self.fetch_all_data(self.characters_url)
        await DataProcessor.process_and_write(all_characters, 'character')

    async def fetch_and_process_locations(self):
        all_locations = await self.fetch_all_data(self.locations_url)
        await DataProcessor.process_and_write(all_locations, 'location')
        await Logger.log_odd_locations(all_locations)
        # You can log or process locations as needed

    async def fetch_and_process_episodes(self):
        all_episodes = await self.fetch_all_data(self.episodes_url)
        await DataProcessor.process_and_write(all_episodes, 'episode')
        await Logger.log_episodes(all_episodes)

    @staticmethod
    async def fetch_all_data(base_url):
        all_data = []
        next_page = base_url

        while next_page:
            data_page = await Fetcher.fetch_data(next_page)
            all_data.extend(data_page['results'])
            next_page = data_page['info']['next']

        return all_data

    async def run(self):
        await asyncio.gather(
            self.fetch_and_process_locations(),
            self.fetch_and_process_characters(),
            self.fetch_and_process_episodes(),
        )


if __name__ == "__main__":
    connector = RickAndMortyConnector()
    asyncio.run(connector.run())
