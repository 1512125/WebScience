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

class Spider:

    # Class variables (shared among all instances)
    domain_name = ''
    base_url = ''
    deep = 7
    queue = set()
    crawled = set()

    def __init__(self, domain_name, base_url, deep):
        Spider.domain_name = domain_name
        Spider.deep = deep
        for i in range(Spider.deep):
            temp = str("crawled_" + str(i))
            Spider.temp = set()
        Spider.base_url = base_url
        Spider.queue.add(base_url)
        self.crawlPage('First spider', Spider.base_url)

    @staticmethod
    def crawlPage(thread_name, page_url):
        index = getDeep(page_url)
        temp = str("crawled_" + str(index))
        if page_url not in Spider.temp:
            if getDeep(page_url) <= Spider.deep:
                try:
                    start = time.time()
                    print(thread_name + ' now crawling ' + page_url)
                    print('Queue ' + str(len(Spider.queue)) + ' | ' +
                        'Crawled ' + str(len(Spider.temp)))
                    Spider.addLinksToQueue(Spider.gatherLinks(page_url), temp)
                    Spider.queue.remove(page_url)
                    Spider.temp.add(page_url)
                    end = time.time()
                    with open("./static/timeCalculate.csv", 'a') as fp:
                        fp.write(page_url + ", " + str(start) + ", " + str(end) + ", " + str(end-start) + "\n")
                except Exception as e:
                    print("Failed to process the request, Exception:%s"%(e))
            else:
                Spider.queue.remove(page_url)

    @staticmethod
    def gatherLinks(page_url):
        results = set()

        for retries in range(5):
            try:
                s = requests.Session()
                s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
                content = s.get(page_url)
                if content.status_code != 200:
                    raise ValueError("Invalid Response Received From Webserver")
                soup = BeautifulSoup(content.text, 'html.parser')
                with open("./html/" + getStringAfterLastSlash(page_url).replace(' ', '_') + ".html", 'a', encoding="utf-8") as fp:
                    fp.write(soup.prettify())

                with open("./text/" + getStringAfterLastSlash(page_url).replace(' ', '_') + ".txt", 'a', encoding="utf-8") as fp:
                    fp.write(soup.get_text().strip())

                for elem in soup.find_all("a", href=True):
                    link = urljoin(page_url, elem['href'])
                    results.add(link)
                
                return results
            except Exception as e:
                print("Failed to process the request, Exception:%s"%(e))
        return []


    @staticmethod
    def addLinksToQueue(links, temp):
        for url in links:
            if (url in Spider.queue) or (url in Spider.temp) or (goToIdInPage(url)):
                continue
            if Spider.domain_name != getDomainName(url):
                continue
            Spider.queue.add(url)