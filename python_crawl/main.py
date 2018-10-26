import threading
from queue import Queue
from util import getDomainName
from util import initFolder
from crawler import Spider

NUM_SPIDERS = 12
DEEP = 7
HOMEPAGE = 'https://vnexpress.net/'
DOMAIN_NAME = getDomainName(HOMEPAGE)
initFolder(".")
Spider(DOMAIN_NAME, HOMEPAGE, DEEP)
q = Queue()


# crawl the next url
def work():
    while True:
        url = q.get()
        Spider.crawlPage(threading.currentThread().name, url)
        q.task_done()


# Create spider threads (will be terminated when main exits)
def createSpiders():
    for spider in range(NUM_SPIDERS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Each queued link is a new job
def createJobs():
    for link in Spider.queue:
        q.put(link)
    q.join()
    crawl()


# Check if there are items in queue, if so crawl it
def crawl():
    if len(Spider.queue) > 0:
        print(str(len(Spider.queue)) + " links in the queue")
        createJobs()

createSpiders()
crawl()






