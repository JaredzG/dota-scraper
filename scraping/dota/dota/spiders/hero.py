import scrapy
from dota.items import HeroItem

class HeroSpider(scrapy.Spider):
  name = "hero"
  allowed_domains = ["https://dota2.fandom.com", "dota2.fandom.com"]
  
  def start_requests(self):
    url = "https://dota2.fandom.com/wiki/Heroes"
    yield scrapy.Request(url)

  def parse(self, response):
    for hero in response.xpath('//table/tbody/tr/td/div/div/a'):
      hero_item = HeroItem()
      hero_item['name'] = hero.xpath('./@title').get()
      yield response.follow(f'{self.allowed_domains[0]}{hero.xpath("./@href").get()}', callback=self.get_hero_data, meta={'hero_item': hero_item})
      
  def get_hero_data(self, response):
    hero_item = response.meta['hero_item']
    hero_item['abilities'] = []
    for ability in response.xpath('//div[@class="ability-background"]/div/div/span'):
        hero_item['abilities'].append(ability.xpath('./text()').get())
    descriptor = response.xpath('//table[@class="infobox"]/following-sibling::table/tbody/tr[2]/td[1]/text()').get()
    hero_item['descriptor'] = descriptor.strip()
    yield hero_item
