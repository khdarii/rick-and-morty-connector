# Rick and Morty API Connector

This Python script fetches data from the [Rick and Morty API](https://rickandmortyapi.com/) and performs the following tasks:

1. Fetches data for Characters, Locations, and Episodes.
2. Writes the data to separate JSON files with unique IDs.
3. Prints a log of episodes aired between 2017 and 2021 with more than three characters.
4. Prints a list of locations that appear only on odd episode numbers.

## Prerequisites

- Python 3.x
- Install dependencies using `pip install -r requirements.txt`

## Usage

1. Clone the repository:

   ```bash
   git clone git@github.com:khdarii/rick-and-morty-connector.git
   cd rick-and-morty-connector
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:

   ```bash
   python main.py
   ```

## Configuration

You can customize the script by modifying the script itself, such as changing the default start and end years for episode filtering.
