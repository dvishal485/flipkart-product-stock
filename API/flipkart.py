from pyppeteer import launch
import asyncio


async def getProductDetails(productLink, pincode):
    browser = await launch(args=['--no-sandbox'],
                           headless=True,
                           handleSIGINT=False,
                           handleSIGTERM=False,
                           handleSIGHUP=False)
    page = await browser.newPage()
    await page.setRequestInterception(True)

    async def intercept(request):
        if any(request.resourceType == _ for _ in ('stylesheet', 'image', 'font')):
            await request.abort()
        else:
            await request.continue_()

    page.on('request', lambda req: asyncio.ensure_future(intercept(req)))
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 OPR/68.0.3618.125')
    try:
        await page.goto(productLink, timeout=10000)
    except:
        None
    try:
        productTitleSelector = await page.waitForSelector('h1', timeout=2000)
        productName = await page.evaluate('(el)=>el.textContent', productTitleSelector)
        try:
            priceSelector = await page.waitForSelector('div[class="dyC4hf"]', timeout=1000)
            prices = (await page.evaluate('(el)=>el.textContent', priceSelector)).replace(',', '')
            currentPrice = prices.split('₹')[1].replace(',', '')
            try:
                discountSelector = await page.Jx('//span[contains(text(), "% off")]')
                discountPercentIndicator = await page.evaluate('(el)=>el.textContent', discountSelector[0])
                originalPrice = prices.split('₹')[2].replace(
                    ',', '').split(discountPercentIndicator)[0]
            except:
                originalPrice = currentPrice
        except:
            None
        try:
            await page.waitForSelector('img[class="jMnjzX"]', timeout=500)
            fassured = True
        except:
            fassured = False
        try:
            outOfStock = (await page.Jx('//div[contains(text(), "currently out of stock")]')).length > 0
        except:
            outOfStock = False
        try:
            comingSoon = (await page.Jx('//div[contains(text(), "Coming Soon")]')).length > 0
        except:
            comingSoon = False
        if (comingSoon or outOfStock):
            inStock = False
        else:
            inStock = True
        if (not comingSoon):
            pinCodeField = await page.xpath('//input[@id="pincodeInputId"]')
            await pinCodeField[0].type(str(pincode))
            checkButton = await page.Jx('//span[contains(text(), "Check")]')
            await checkButton[0].click()
            try:
                await page.waitForXPath('//div[contains(text(), "Currently out of stock in this area.")]', timeout=2000)
                pincodeStock = False
            except:
                try:
                    await page.waitForXPath('//div[contains(text(), "Not a valid pincode")]', timeout=500)
                    pincodeStock = False
                except:
                    pincodeStock = True

        stockMessage = {'general_stock': inStock,
                        'pincode': pincode, 'pincode_stock': pincodeStock}
    # await page.screenshot(path='sample.png', type='png')
        result = {'name': productName, 'current_price': currentPrice, 'original_price': originalPrice,
                  'discount': discountPercentIndicator, 'share_url': productLink, 'fassured': fassured, 'stock_details': stockMessage}
        try:
            await page.close()
            await browser.close()

        except:
            None
        return result
    except:
        return {'error': 'Some error occured, we may not support all products right now'}
