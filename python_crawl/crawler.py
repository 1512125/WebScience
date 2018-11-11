from util import getDomainName
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from util import initAllowElem
from util import getStringAfterLastSlash
from util import getDeep
from util import goToIdInPage
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from tqdm import tqdm
tqdm.monitor_interval = 0

class Crawler:

    # Class variables (shared among all instances)
    domain_name = ''
    base_url = ''
    depth = 7
    queue = set()
    crawled = []

    def __init__(self, domain_name, base_url, depth):
        Crawler.domain_name = domain_name
        Crawler.depth = depth
        Crawler.crawled = [[] for _ in range(depth)]
        Crawler.base_url = base_url
        Crawler.queue.add(base_url)
        self.crawlPage('First Crawler', Crawler.base_url)

    @staticmethod
    def crawlPage(thread_name, page_url):
        index = getDeep(page_url)
        if index <= Crawler.depth:
            if page_url not in Crawler.crawled[index]:
                try:
                    start = time.time()
                    print(thread_name + ' now crawling ' + page_url)
                    print('Queue ' + str(len(Crawler.queue)) + ' | ' +
                        'Crawled ' + str(len(Crawler.crawled[index])))
                    Crawler.addLinksToQueue(Crawler.gatherLinks(page_url), index)
                    Crawler.queue.remove(page_url)
                    Crawler.crawled[index].append(page_url)
                    end = time.time()
                    with open("./static/timeCalculate.csv", 'a') as fp:
                        fp.write(page_url + ", " + str(start) + ", " + str(end) + ", " + str(end-start) + "\n")
                except Exception as e:
                    print("Failed to process the request, Exception:%s"%(e))
            else:
                Crawler.queue.remove(page_url)

    @staticmethod
    def gatherLinks(page_url):
        results = set()

        for retries in range(5):
            try:
                s = requests.Session()
                s.headers['User-Agent'] = 'nguyenhuudatduc HCMUS'
                content = s.get(page_url)
                if content.status_code != 200:
                    raise ValueError("Invalid Response Received From Webserver")
                soup = BeautifulSoup(content.text, 'html.parser')
                with open("./static/pageLength.csv", 'a') as fp:
                    fp.write(page_url + ", " + str(len(content.text)) + "\n")
                with open("./html/" + getStringAfterLastSlash(page_url).replace(' ', '_') + ".html", 'a', encoding="utf-8") as fp:
                    fp.write(soup.prettify())

                with open("./text/" + getStringAfterLastSlash(page_url).replace(' ', '_') + ".txt", 'a', encoding="utf-8") as fp:
                    fp.write(soup.get_text())

                for elem in soup.find_all("a", href=True):
                    link = urljoin(page_url, elem['href'])

                    results.add(link)
                
                return results
            except Exception as e:
                print("Failed to process the request, Exception:%s"%(e))
        return []


    @staticmethod
    def addLinksToQueue(links, index):
        for url in links:
            with open("./static/urls.csv", 'a') as fp:
                fp.write(url + "\n")
            if (url in Crawler.queue) or (url in Crawler.crawled[index]) or (goToIdInPage(url)):
                continue
            if Crawler.domain_name != getDomainName(url):
                continue
            Crawler.queue.add(url)