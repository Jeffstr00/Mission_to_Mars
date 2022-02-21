# Mission_to_Mars

## Overview

Robin is a data scientist who is obsessed with space, particularly Mars, so she spends a lot of her time keeping up with the latest news on the topic.  While it is currently her hobby, she ultimately dreams of working for NASA someday.  In an attempt to impress her prospective employer, she decides to put together a webpage.  However, rather than just creating a static webpage, she wants it to be a dynamic page which features the latest and greatest news and images.  In order to do this, she has asked us to help her set up a system that will automatically scrape the latest headlines, pictures, and information on the Red Planet from different websites and then display them on a webpage of her own.

## Information Gathering/Scraping

### Latest News

Once we navigated our browser to [https://redplanetscience.com](https://redplanetscience.com), finding the latest news title and text was easy enough thanks to the class titles.  `slide_elem.find('div', class_='content_title')` `news_title = slide_elem.find('div', class_='content_title').get_text()` returned the title, while `news_p = slide_elem.find('div', class_='article_teaser_body').get_text()` provided us with the paragraph text.

### Featured Image

We extracted the latest Mars image from [https://spaceimages-mars.com/](https://spaceimages-mars.com/).  We first clicked on the button using `full_image_elem = browser.find_by_tag('button')[1]` `full_image_elem.click()`, which brought us to the full-size image.  We then found the relative image using `img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')` and combined it with the base image to give us the full location using an f-string: `img_url = f'https://spaceimages-mars.com/{img_url_rel}'`.

### Facts Table

For our facts table, we used [https://galaxyfacts-mars.com](https://galaxyfacts-mars.com).  We read the table into a pandas dataframe using `df = pd.read_html('https://galaxyfacts-mars.com')[0]`, with the "[0]" telling pandas to pull the first table it comes across.  We then assigned the table columns using `df.columns=['description', 'Mars', 'Earth']` and set the index to the description column.

### Hemisphere Images

Finally, we went to [https://marshemispheres.com/](https://marshemispheres.com/) to obtain our beautiful images of each of Mars's four hemispheres.  Using a For loop (`for i in range(4):`) so that we could perform this for each hemisphere, we clicked on the link to take us to the full-size image using `    browser.find_by_css('a.product-item h3')[i].click()`.  We then found the url object using `sample_elem = browser.links.find_by_text('Sample').first`, and extracted its url using `image_url = sample_elem['href']`.  We then searched out the title using `title = browser.find_by_css('h2.title').text`.  Once we had both the image's url and title saved to their dictionary, we appended the list to add the current hemisphere's info using `    hemisphere_image_urls.append(hemispheres)`.  

## Customizing Webpage

While we started off with a standard webpage, we customized it in an attempt to hopefully make it stand out and look more appealing:

* Various headline texts were centered using, for instance, `<h2 style="text-align:center">Featured Mars Image</h2>`.
* The "Scrape New Data" button was changed to red by adding `class="btn btn-danger btn-lg"` to the button code.
* We highlight the fact that the Latest Mars News paragraph is a quote by putting `<p>{{ mars.news_paragraph }}</p>` inside of a `<blockquote>`.
* To go with the Mars theme, we made the background into a maroon/black gradient using `<body style="background-image: linear-gradient(to bottom right, #530909, black); color:rgb(245, 222, 222);">` (which subsequently had us change the font color to white so that it would be readable).
* For the main Mission to Mars title, we highlighted it by putting it (and the scrape button) inside of a black/gray/maroon radial gradient: `      <div class="jumbotron text-center" style="background-image: radial-gradient(black, rgb(32, 24, 24), #530909); color:rgb(245, 222, 222);">`.

![Mission to Mars webpage](https://github.com/Jeffstr00/Mission_to_Mars/blob/main/Resources/webpage.png)