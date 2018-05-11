# Overview

A full-featured e-commerce website based on Django, Mezzanine and Cartridge. Bitcoin payments are accepted here. Uses a modern HTML theme available [here](https://bootstrapious.com/p/obaju-e-commerce-template). 

# Features
Supports almost all e-ecommerce features available in Cartridge. Namely you can expect to have:

* Customizable Admin Interface
* Shopping Cart
* Sales
* Discount Codes
* Product Categories
* Product Ordering
* Search
* Related Products
* Upsell products

Plus...

* A Sleek UI
* Bitcoin Payments
* Product Filtering
* Recently Viewed Products
* and more…

# Local Installation

1. Clone this repo
2. Install `virtualenv` if haven’t installed it
3. Create a new environment - `mkvirtualenv ecommerce`
4. `cd` to cloned repo
5. `pip install -r requirements.py` - installs the required modules
6. `python manage.py migrate` - applies the migrations
7. `python manage.py createsuperuser` - create an admin user
8. Navigate to http://localhost:8000/admin and enter the credentials from the previous step
9. From left panel click on Pages then choose “Home page” from “Add…” dropdown
10. Fill in the fields, scroll down to “Meta data” tab and type “/” without quotes in URL field
11. Click Save and navigate to http”//localhost:8000

To add sliders first create Gallery pages add as many images as you like than drag those Gallery instances under Homepage like in picture below
![alt text](https://bitcoineria.com/static/media/uploads/blog/post_images/.thumbnails/sliders_under_homepage.png/sliders_under_homepage-760x156.png "Sliders under homepage")


# Bitcoin Payments 
Website leverages blockchain.info's [Receive Payments API V2](https://blockchain.info/api/api_receive) for accepting bitcoin payments. Follow the instructions on the linked page to sign up for a wallet, request an API key and find out your XPUB. You then need to copy over those values into your “local_settings.py” file. More delails in [this blog post](https://bitcoineria.com/blog/recently-viewed-product-filtering-and-bitcoin-payments/)

# Deployment 
Deployment is rather easy because Mezzanine is already configured with a deployment tool like Fabric. For specific deployment instructions visit [this blog post](https://bitcoineria.com/blog/deployment/)

# How to...
### Set up links for social icons in the footer
* Log in to admin UI
* From left panel click "Settings"
* Scroll down to "Social" tab
* Fill in the links to social platforms
* Leave blank those you don't want to be displayed

### Use product filtering
* Log in to admin UI
* From left panel choose "Pages"
* Choose a Category or create a new one
* Scroll down to Product filters
* Choose an option shared among all the products in that category
* Click Save
* Navigate to any product or category page on main site
* Select an option and click Apply to see filtred products

### Add upsell/related products
* Log in to admin UI
* Click on a product in "Products" menu
* Scroll down to "Other products" expandable tab
* Choose Related and/or Upsell products as you like
* (Related products appear on a given product's page, upsell products - on cart page

### Use in-line editing
* On admin UI choose "Site" before logging in
* If a page has in-line editable content it will dislay small "Edit" links
* Click those links and edit the content on-the-fly

# Tests
Several tests have been created in main/tests.py and btc_payment/tests.py. To run the tests issue the commands:
`./manage.py test main.test`
`./manage.py test btc_payment.tests`

# Credits
All the credits for the utilized packages and dependencies go to their respective owners. All I’ve done is a little remix.)

# Donation
If this code adds any value to you and you'd like to reciprocate, here's a bitcoin address for donations:)
19w9wSmtL2PaLwSsQktd6TzGKYnMerq6Fs ![alt text](https://bitcoineria.com/static/media/uploads/galleries/.thumbnails/donation.png/donation-200x200.png "Donation QR code")
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=9PWESEARPH2QU)
