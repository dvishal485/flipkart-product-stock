import API.flipkart as flipkart
import asyncio


async def main(link, pincode):
    result = await flipkart.getProductDetails(link, pincode)
    try:
        print('Product Name : '+result["name"])
        print('Current Price : '+str(result["current_price"]))
        print('Original Price : '+str(result["original_price"]))
        print('Discount : '+result["discount"])
        print('Share URL : '+result["share_url"])
        print('F-Assure Product : '+str(result["fassured"]))
        print('In Stock (general) : ' +
              str(result["stock_details"]["general_stock"]))
        print('In Stock (for pincode '+str(result["stock_details"]["pincode"])+') : ' +
              str(result["stock_details"]["pincode_stock"]))
    except:
        print('Error : Some error occurred while fetching product details')
    finally:
        print(br)
        check = input('Check out other product? (Y/N)')
        if check == 'y' or check == 'Y':
            inputData = askInput()
            await main(inputData[0], inputData[1])
        else:
            exit()


br = '___________________________________________________________'

print('=> flipkart-product-stock <=')
print('=> Flipkart Product Stock Details in a specific pincode <=')


def askInput():
    print(br)
    link = input("Input link of product : ")
    pincode = input("Your pincode : ")
    print(br)
    print('Please wait while we check your product on Flipkart...')
    print(br)
    return [link, pincode]


inputData = askInput()
asyncio.run(main(inputData[0], inputData[1]))
