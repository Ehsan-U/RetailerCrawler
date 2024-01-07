- Create `.env` file under the project dir<br>
- Add `ZYTE_API=<api-key>`


<br>Now spider can run by this command:

`scrapy crawl retailer`

#### Build

<!--- docker rmi deelio_crawler -->
docker build -t deelio_crawler .

#### Run

##### Scrapping
docker run --rm --add-host host.docker.internal:host-gateway deelio_crawler scrapy crawl retailer -a RETAILER_ID=1
##### Product check
docker run --rm --add-host host.docker.internal:host-gateway deelio_crawler scrapy crawl retailer -a RETAILER_ID=1 -a SPIDER_TYPE=checker
