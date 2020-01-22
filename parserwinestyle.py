from bs4 import BeautifulSoup
from parser import Parser


class ParserWineStyle(Parser):
    def __init__(self, browser):
        self.browser = browser
        self.page = None
        self.data = []

    def parse(self, url):
        try:
            self.browser.get(url)
        except:
            print('Page ' + url + ' not respond.')
        self.page = BeautifulSoup(self.browser.page_source, 'html.parser')

    def get_page_count(self, url):
        self.parse(url)
        soup = self.page
        all_li = soup.find('div', {'id': 'CatalogPagingBottom'}).find_all('li')
        page_count = BeautifulSoup(str(all_li[len(all_li) - 1:]), 'html.parser').find('a').text
        return page_count

    def get_data(self):
        content = self.page.find('div', {'class': 'center-content'})
        items = content.find_all('form', {'class': 'item-block'})

        for item in items:
            wine = {}
            wine['title'] = self.clear_string(item.find('p', {'class': 'title'}).find('a').text)
            wine['price'] = self.clear_string(str(item.find('div', {'class': 'price'}).text[:-5]).replace(' ', ''))
            wine['volume'] = self.clear_string(item.find('label').text[5:-2])
            regions = item.find('ul', {'class': 'list-description'}).find('li').find_all('a')
            try:
                wine['rating'] = self.clear_string(item.find('div', {'class': 'info-block rating-text'}).find('span', {'class': 'text'}).text)
            except AttributeError:
                wine['rating'] = None
            ratings_div = item.find_all('div', {'class': 'rating-item'})
            for rat in ratings_div:
                wine['rating_' + rat.find('div').find_all('span')[0].text] = self.clear_string(rat.find('div').find_all('span')[1].text)

            count_regions = len(regions)

            for i in range(0, count_regions):
                wine['region_' + str(i + 1)] = self.clear_string(regions[i].text)
            self.data.append(wine)
