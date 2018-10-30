import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;

public class Controller {

	public static void main(String[] args) throws Exception {

		int numberOfCrawlers = 7;
		String crawlStorageFolder = "output";
		int maxDepthOfCrawling = 7;
		
		 CrawlConfig config = new CrawlConfig();
		 config.setCrawlStorageFolder(crawlStorageFolder);
		 config.setMaxDepthOfCrawling(maxDepthOfCrawling);
		 config.setIncludeBinaryContentInCrawling(true);
		 config.setFollowRedirects(true);
		 config.setPolitenessDelay(300);
		 /*
		 * Instantiate the controller for this crawl.
		 */
		 PageFetcher pageFetcher = new PageFetcher(config);
		 RobotstxtConfig robotstxtConfig = new RobotstxtConfig();
		 RobotstxtServer robotstxtServer = new RobotstxtServer(robotstxtConfig, pageFetcher);
		 CrawlController controller = new CrawlController(config, pageFetcher, robotstxtServer);
		 /*
		 * For each crawl, you need to add some seed urls. These are the first
		 * URLs that are fetched and then the crawler starts following links
		 * which are found in these pages
		 */
		 controller.addSeed("https://www.vnexpress.net/");
		 
		 MyCrawler.configure("output/downloads");

        /*
         * Start the crawl.
         */
        controller.start(MyCrawler.class, numberOfCrawlers);
    }
}
