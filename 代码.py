import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

# Set fonts to prevent Chinese garbled characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # Set Chinese font to SimHei
plt.rcParams['axes.unicode_minus'] = False  # Fix issue with negative sign not showing up

class TideDataVisualizer:
    def __init__(self, base_url, year):
        self.base_url = base_url
        self.year = year
        self.dates = []
        self.heights = []

    def fetch_page(self, url):
        """Fetches the page content from a given URL."""
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return None

    def find_tide_data_link(self, soup):
        """Finds the tide data link for the specified year."""
        table = soup.find('table')
        link_tag = table.find('a', href=True, text=str(self.year)) if table else None
        if link_tag:
            return self.base_url + link_tag['href']
        else:
            print(f"Could not find the link for the {self.year} tide data.")
            return None

    def parse_tide_data(self, soup):
        """Parses tide data from the HTML content."""
        pre_tag = soup.find('table')
        if pre_tag:
            data_lines = pre_tag.text.splitlines()
            print("Tide data preview:")
            for line in data_lines[:10]:  # Show the first 10 lines as a preview
                print(line)
            return data_lines
        else:
            print("Could not find <table> tag containing tide data.")
            return None

    def process_tide_data(self, data_lines):
        """Processes tide data into dates and heights."""
        for line in data_lines[3:]:  # Skip the first few descriptive lines
            parts = line.split()
            if len(parts) >= 3:
                date = parts[0]
                height = round(float(parts[1]), 2)  # Tide height
                self.dates.append(date)
                self.heights.append(height)

    def plot_tide_data(self):
        """Plots tide data using a bar chart and line plot."""
        date_range = np.arange(len(self.dates))

        # Visualize the tide height changes as a bar chart and line plot
        plt.figure(figsize=(10, 6))

        # Plot the bar chart (histogram)
        plt.bar(date_range, self.heights, color='b', alpha=0.6, label='Tide Heights')

        # Plot the line chart on the same axis
        plt.plot(date_range, self.heights, color='r', marker='o', label='Line Plot')

        # Customizations
        plt.xticks(date_range, self.dates, rotation=90)
        plt.xlabel('Date')
        plt.ylabel('Tide Height (m)')
        plt.title(f'Tide Height Changes ({self.year}): Bar and Line Plot Combined')
        plt.grid(True, axis='y')
        plt.legend()

        plt.tight_layout()
        plt.show()

    def run(self):
        """Orchestrates the entire flow."""
        # Fetch the main tide page content
        main_page_content = self.fetch_page(self.base_url + '/en/tide/ttext.htm')
        if not main_page_content:
            return

        soup = BeautifulSoup(main_page_content, 'html.parser')

        # Find the link to the specified year's tide data
        tide_data_link = self.find_tide_data_link(soup)
        if not tide_data_link:
            return

        # Fetch the tide data page content
        tide_page_content = self.fetch_page(tide_data_link)
        if not tide_page_content:
            return

        tide_soup = BeautifulSoup(tide_page_content, 'html.parser')

        # Parse and process the tide data
        tide_data_lines = self.parse_tide_data(tide_soup)
        if tide_data_lines:
            self.process_tide_data(tide_data_lines)

            # Plot the tide data
            self.plot_tide_data()


# Create an instance of the TideDataVisualizer class for the year 2026
visualizer = TideDataVisualizer(base_url='https://www.hko.gov.hk', year=2026)

# Run the visualization
visualizer.run()
