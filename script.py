import flipkart
import asyncio


async def main(link, pincode):
    result = await flipkart.getProductDetails(link, pincode)
    print('Product Name : '+result["name"])
    print('Current Price : '+result["current_price"])
    print('Original Price : '+result["original_price"])
    print('Discount : '+result["discount"])
    print('Share URL : '+result["share_url"])
    print('F-Assure Product : '+str(result["fassured"]))
    print('In Stock (general) : ' +
          str(result["stock_details"]["general_stock"]))
    print('In Stock (for pincode '+str(result["stock_details"]["pincode"])+') : ' +
          str(result["stock_details"]["pincode_stock"]))

br = '__________________________________________________'

print('=> flipkart-product-stock')
print('=> Flipkart Product Stock Details in a specific pincode')
print(br)
link = input("Input link of product : ")
pincode = input("Your pincode : ")
print(br)
print('Please wait while we check in marketplace...')
asyncio.run(main(link, pincode))
