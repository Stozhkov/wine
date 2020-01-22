import multiprocessing
from parserwinestyle import ParserWineStyle
import pandas
from selenium import webdriver


def generate_urls(url):
    parser = ParserWineStyle(browser)
    page_count = int(parser.get_page_count(url)) + 1
    urls_list = []
    for i in range(1, page_count):
        urls_list.append(url + '?page=' + str(i))
    return urls_list


def run_parser(url):
    parser = ParserWineStyle(browser)
    parser.parse(url)
    parser.get_data()
    df = pandas.DataFrame(parser.data)
    return df


url = 'https://winestyle.ru/wine/1000-1500rub/1500-3000rub/500-1000rub/wines/available/limited_ll/'
data_frames = []

if __name__ == '__main__':
    browser = webdriver.Chrome()
    count_of_processes = 1
    pool = multiprocessing.Pool(count_of_processes)

    for res in pool.imap(run_parser, generate_urls(url), 1):
        data_frames.append(res)

    result = pandas.concat(data_frames, sort=True).drop_duplicates().reset_index(drop=True)

    result.to_csv('result.txt', header=True, index=False, sep=';')
    browser.close()
