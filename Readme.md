- Create `.env` file under the project dir<br>
- Add `ZYTE_API=<api-key>`


<br>Now spider can run by this command:

`scrapy crawl retailer_spider`

#### Build

<!--- docker rmi mycrawler -->
docker build -t mycrawler .

#### Run

docker run --rm --add-host host.docker.internal:host-gateway mycrawler scrapy crawl retailer