# Product In-Stock Notifier

This project's was built to monitor websites for product stock updates.
Encapsulating the code within a Docker container allow easy dispatching to remote Synology NAS servers.

## Development Build:
Stand up development build for local testing
```
docker compose up
docker compose down # To clean up
````

## Build Production Image
```
docker build -t in-stock-notifier-arm .
```

## Build x86-64 Production Image Building on Apple Silicon (Cross-platform building)
```
docker buildx ls # First, list all available Cross-Build Platforms
docker buildx build --platform linux/amd64 -t in-stock-notifier-amd64 . # Build the image
```

## Save the image for exporting to a NAS
```
docker images # List Images
```
```
docker save in-stock-notifier-arm:latest -o in-stock-notifier-arm
docker save in-stock-notifier-amd64:latest -o in-stock-notifier-amd64
```
or
```
docker save in-stock-notifier-arm:latest | gzip > in-stock-notifier-arm.tar.gz
docker save in-stock-notifier-amd64:latest | gzip > in-stock-notifier-amd64.tar.gz
```
Loading the Image into Docker:
```
docker load -i <path to image tar file>
```

## Docker Container Environmental Variables:

| Variable      | Data Type     | Description  |
| ------------- | ------------- | ------------ |
| PAGE      | Product URL | String |
| DIV     | DIV ID that contains the Keyword | String |
| KEYWORD | The "Out of Stock" string | String |
| EMAIL_SUBJECT | Notification Email Subject | String |
| ADDRESS | Recipient Email Address | String |
| PASSWORD | Email Password | String | 
| SMS_NUMBER | [7 Digit Phone Number] + [@Gateway] | String |
| RUN_HOURS | Number of hours to Run  | Int |
| POLL_FREQUENCY | Time in seconds between polling | Int |

### SMS Gateways by Provider
| Provider | Gateway |
| -------- | ------- |
| AT&T | @txt.att.net |
| Sprint | @messaging.sprintpcs.com or @pm .sprint.com |
| T-Mobile | @tmomail.net |
| Verizon | @vtext.com |
| Boost Mobile | @myboostmobile.com |
| Cricket | @sms.mycricket.com |
| Metro PCS | @mymetropcs.com |
| Tracfone | @mmst5.tracfone.com |
| U.S. Cellular | @email.uscc.net |
| Virgin Mobile | @vmobl.com |

## Run the Container
### Example 1:
```
docker run -d -it --name fuji-in-stock-notifier \
-e PAGE='https://fujifilm-x.registria.com/products/0-74101-20713-2' \
-e DIV='pdp-buy-now-txt' \
-e KEYWORD='Notify Me' -e EMAIL_SUBJECT='!! Fujifilm Stock Update !!' \
-e ADDRESS='' -e PASSWORD='' -e SMS_NUMBER='' \
-e RUN_HOURS='2190' -e POLL_FREQUENCY='10'  \
in-stock-notifier-arm
```

### Example 2:
```
docker run -d -it --name fieldsheer-in-stock-notifier \
-e PAGE='https://fieldsheer.com/products/7-4v-glove-2in1-battery?variant=30238111826035' \
-e DIV='add-cart-wrapper' \
-e KEYWORD='Coming Soon' -e EMAIL_SUBJECT='!! Fieldsheer Stock Update !!' \
-e ADDRESS='' -e PASSWORD='' -e SMS_NUMBER='' \
-e RUN_HOURS='2190' -e POLL_FREQUENCY='10'  \
in-stock-notifier-arm
```