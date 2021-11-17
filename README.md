# Flipkart Pincode Specific Product Stock

API to scrapes product details and pincode specific stock from Flipkart.

The [Flipkart Scrapper API](https://github.com/dvishal485/flipkart-scraper-api) could give the stock avalibility of a product in general and not in any specific reigion. This project is created to fill the gap in hole of specificity of product avalibility.

You can also deploy the API yourself on Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

(API will be disabled at night, host your own to get access of API at those hours) : [See Important Note](#important-note)

---

## Features

You can fetch following product details from Flipkart :

- Product Name

- Current Price (specific to given pincode)

- Original Price / MRP

- Discount offered

- Shareable URL (without unnecessary arguments)

- Flipkart Assured or not (f-assured status)

- Stock details

- General Stock detail (without entering pincode)

- Specific Stock detail (specific to given pincode)

---

## Usage

1. Using API

    API requires two arguments :

    - Flipkart Product URL

    - Pincode (defaults to `110051`)

    Syntax URL : `https://flipkart-product-stock.herokuapp.com/product?link={product_link}&pincode={pincode}`

2. Using Terminal Script

    One can also use the [terminal-script.py provided in the root folder](terminal-script.py)

    1. Clone the repository to your system.

    2. Install the python modules (one-time measure):

        `pip install -r requirements.txt`

    3. Run the script in the root directory :

        `python terminal-script.py`

    4. You will be asked for the product link and then the pincode of your location and will be reverted back with product and stock details

---

## Important Note

As the API is hosted on Heroku's free limited dyno, the API hosted by [developer](https://github.com/dvishal485) will be unavalible during night ( `02:00 AM` to `10:00 AM` IST ). If you want to use the API at those hours, kindly host your own.


---

## Sample

The API is easy to use and understand, but in case of any problem do check out the sample API usage and it's response.

<details>
	<summary>Check out an example</summary>
	
- Example URL : https://flipkart-product-stock.herokuapp.com/product?link=https://dl.flipkart.com/s/WaqrsvNNNN&pincode=712702

- Response :

```json
{
  "name": "42 Years Chapterwise Topicwise Solved Papers (2020-1979) Iit Jee Chemistry  (English, Paperback, Shahi Ranjeet)",
  "current_price": 236,
  "original_price": 430,
  "discount": "45% off",
  "share_url": "https://dl.flipkart.com/s/WaqrsvNNNN",
  "fassured": true,
  "stock_details": {
    "general_stock": true,
    "pincode": "712702",
    "pincode_stock": false
  }
}
```
</details>

---

## ToDo

- [x] Make an API usage guide
- [x] Add Deploy to Heroku button
- [x] Add Support for more Products
- [x] Get Product Price specific to the pincode
- [x] Improve accuracy (worked for all Flipkart links which were tested)

---

## License & Copyright

  - This Project is [Apache-2.0](./LICENSE) Licensed
  - Copyright 2021 [Vishal Das](https://github.com/dvishal485)