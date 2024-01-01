- Create `.env` file under the project dir<br>
- Add `ZYTE_API=<api-key>`


<br>Now spider can run by this command:

`scrapy crawl retailer_spider`

#### Build

<!--- docker rmi deelio_crawler -->
docker build -t deelio_crawler .

#### Run

##### Scrapping
docker run --rm --add-host host.docker.internal:host-gateway deelio_crawler scrapy crawl retailer
##### Product check
docker run --rm --add-host host.docker.internal:host-gateway deelio_crawler scrapy crawl retailer -a SPIDER_TYPE=checker
