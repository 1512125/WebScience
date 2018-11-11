import threading
from queue import Queue
from util import getDomainName
from util import initFolder
from crawler import Crawler

NUM_SPIDERS = 12
DEPTH = 7
HOMEPAGE = 'https://vnexpress.net/'
DOMAIN_NAME = getDomainName(HOMEPAGE)
initFolder(".")
Crawler(DOMAIN_NAME, HOMEPAGE, DEPTH)
q = Queue()

def work():
    while True:
        url = q.get()
        Crawler.crawlPage(threading.currentThread().name, url)
        q.task_done()

# Create spider threads (will be terminated when main exits)
def createCrawlers():
    for spider in range(NUM_SPIDERS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Each queued link is a new job
def createJobs():
    for link in Crawler.queue:
        q.put(link)
    q.join()
    crawl()


# Check if there are items in queue, if so crawl it
def crawl():
    if len(Crawler.queue) > 0:
        print(str(len(Crawler.queue)) + " links in the queue")
        createJobs()

createCrawlers()
crawl()


