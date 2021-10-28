from pyppeteer import launch
import asyncio
import math


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
        try:
            await page.goto(productLink, timeout=10000)
        except:
            None
        try:
            await page.waitForXPath('//div[contains(text(), "currently out of stock")]', timeout=1000)
            outOfStock = True
        except:
            outOfStock = False
        try:
            await page.waitForXPath('//div[contains(text(), "Coming Soon")]', timeout=800)
            comingSoon = True
        except:
            comingSoon = False
        if (comingSoon or outOfStock):
            inStock = False
        else:
            inStock = True
        if (inStock):
            try:
                pincodeField = await page.xpath('//input[@id="pincodeInputId"]')
                await pincodeField[0].click(clickCount=3)
                await pincodeField[0].type(str(pincode))
            except:
                try:
                    await page.waitForSelector('input[class="cfnctZ"]', timeout=1200)
                except:
                    pincodeDropDownMenu = await page.querySelector('img[src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI5IiBoZWlnaHQ9IjUiPjxwYXRoIGZpbGw9IiMyMTIxMjEiIGZpbGwtcnVsZT0iZXZlbm9kZCIgZD0iTS4yMjcuNzAzQy0uMTY4LjMxNS0uMDMyIDAgLjUxNCAwaDcuOTY1Yy41NTYgMCAuNjg1LjMxNy4yOTguNjk4TDcuNjQgMS44MThsLTIuNDI3IDIuMzlhMS4wMiAxLjAyIDAgMCAxLTEuNDI3LS4wMDNMLjIyNy43MDN6Ii8+PC9zdmc+"]')
                    await pincodeDropDownMenu.click()
                    await page.waitForSelector('input[class="cfnctZ"]', timeout=1100)
                pincodeField = await page.querySelectorAll('input[class="cfnctZ"]')
                await pincodeField[0].click(clickCount=3)
                await pincodeField[0].type(str(pincode))
            checkButton = await page.Jx('//span[contains(text(), "Check")]')
            await checkButton[0].click()
            try:
                await page.waitForXPath('//div[contains(text(), "Currently out of stock in this area.")]', timeout=2100)
                pincodeStock = False
            except:
                try:
                    await page.waitForXPath('//div[contains(text(), "Not a valid pincode")]', timeout=1100)
                    pincodeStock = False
                except:
                    try:
                        await page.waitForXPath('//div[contains(text(), "No seller")]', timeout=1100)
                        pincodeStock = False
                    except:
                        pincodeStock = True
        else:
            pincodeStock = False
        webPage = await page.content()

        # Verification mechanism for TRUE pincode stock
        if pincodeStock:
            if webPage.__contains__('No seller') or webPage.__contains__('Not a valid pincode') or webPage.__contains__('out of stock'):
                pincodeStock = False

        webPage = webPage.replace('&amp;', '&')

        try:
            productTitleSelector = await page.waitForSelector('h1', timeout=1500)
            productName = await page.evaluate('(el)=>el.textContent', productTitleSelector)
        except:
            productName = webPage.split('class="B_NuCI')[1].split(
                '</span>')[0].split('>')[1].replace('<!-- -->', '').replace('&nbsp;', '')
        try:
            priceSelector = await page.waitForSelector('div[class="dyC4hf"]', timeout=1000)
            prices = (await page.evaluate('(el)=>el.textContent', priceSelector)).replace(',', '')
            currentPrice = int(prices.split('₹')[1].replace(',', ''))
            try:
                discountSelector = await page.Jx('//span[contains(text(), "% off")]')
                discountPercentIndicator = await page.evaluate('(el)=>el.textContent', discountSelector[0])
                originalPrice = int(prices.split('₹')[2].replace(
                    ',', '').split(discountPercentIndicator)[0])
            except:
                originalPrice = currentPrice
                discountPercentIndicator = '0% off'
        except:
            currentPrice = int(webPage.split('<h1')[1].split(">₹")[
                1].split("</div>")[0].replace(',', ''))
            originalPriceFinder = webPage.split('<h1')[1].split(
                ">₹")[2].split("</div>")[0].split('<!-- -->')
            if len(originalPriceFinder) > 1:
                try:
                    originalPriceField = originalPriceFinder[1].replace(
                        ',', '')
                    originalPrice = int(originalPriceField)
                except:
                    originalPrice = currentPrice
            else:
                try:
                    originalPrice = int(webPage.split('_3I9_wc _2p6lqe')[1].split(
                        '</div>')[0].split('>')[1].replace('₹', '').replace(',', ''))
                except:
                    originalPrice = currentPrice
            discount = originalPrice-currentPrice
            discountPercent = math.floor(discount/originalPrice * 100)
            discountPercentIndicator = str(discountPercent) + '% off'
        try:
            await page.waitForSelector('img[class="jMnjzX"]', timeout=1000)
            fassured = True
        except:
            fassured = False

        stockMessage = {'general_stock': inStock,
                        'pincode': pincode, 'pincode_stock': pincodeStock}
        result = {'name': productName, 'current_price': currentPrice, 'original_price': originalPrice,
                  'discount': discountPercentIndicator, 'share_url': productLink, 'fassured': fassured, 'stock_details': stockMessage}
    except:
        result = {'error': 'Some error occured while fetching product details'}
    finally:
        try:
            await page.close()
            await browser.close()
        except:
            None
        return result
