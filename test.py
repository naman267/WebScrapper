from Scraper import Scraper

sc = Scraper("https://www.monster.com/jobs/search/?q=Software-Developer&where=NY")

q = sc.find(_tag="div", _id="SearchResults")
tree = sc.parse(sc.getSubstring(q[0]))

for section in tree.children.tags:
    if(section.props["class"] == 'card-content'):
        title = section.find(_tag = "h2", _class='title').children.getString()[0]
        company = section.find(_tag = "div", _class='company').find(_tag = "span").getString()[0]
        location = section.find(_tag = "div", _class='location').find(_tag = "span").getString()[0]
        print("Title: ", title)
        print("Company: ",company)
        print("Location: ", location)

tree.children.tags[0].display()