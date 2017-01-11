import scrapy
import collections
from itertools import dropwhile
from stop_words import get_stop_words
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# STARTING_URL = 'https://en.wikipedia.org/wiki/Baseball'
# STARTING_URL = 'https://marc-lj-401.herokuapp.com/'
# STARTING_URL = ''
STARTING_URL = 'http://www.espn.com/'
NUM_OF_OCCURANCES = 3


class HarvestSpider(scrapy.Spider):
    """Spider for harvesting words from a URL."""

    name = "harvester"


    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'harvester.pipelines.HarvesterPipeline': 300,
    #     }
    # }

    def __init__(self, url=None, *args, **kwargs):
        """Initialize a harvest spider."""
        self.url = url

    def start_requests(self):
        """Starting place for request."""
        print('helo helo helo helo')
        print(self.url)
        yield scrapy.Request(url=STARTING_URL, callback=self.parse)

    def parse(self, response):
        """Get words from site."""
        words = []
        headers = []
        title = []
        words_in_title = []
        words_in_headers = []
        stop_words = get_stop_words('english')
        h1_res = response.css('h1::text').extract()
        h2_res = response.css('h2::text').extract()
        h3_res = response.css('h3::text').extract()
        h4_res = response.css('h4::text').extract()
        h5_res = response.css('h5::text').extract()
        h6_res = response.css('h6::text').extract()
        title_res = response.css('title::text').extract()
        p_res = response.css('p::text').extract()

        for each in p_res:
            words.extend(each.split())
        for each in h1_res:
            headers.extend(each.split())
        for each in h2_res:
            headers.extend(each.split())
        for each in h3_res:
            headers.extend(each.split())
        for each in h4_res:
            headers.extend(each.split())
        for each in h5_res:
            headers.extend(each.split())
        for each in h6_res:
            headers.extend(each.split())
        for each in title_res:
            title.extend(each.split())
        words = lower_list(words)
        headers = lower_list(headers)
        title = lower_list(title)
        for word in words:
            if word in headers and word not in stop_words:
                words_in_headers.append(word)
            if word in title and word not in stop_words:
                words_in_title.append(word)
        word_count = collections.Counter(words)
        head_count = collections.Counter(headers)
        title_count = collections.Counter(title)
        for key, count in dropwhile(lambda key_count: key_count[1] >= NUM_OF_OCCURANCES, word_count.most_common()):
            del word_count[key]
        for key in list(word_count.keys()):
            if key in stop_words:
                del word_count[key]
        return word_count


def harvest(url):
    settings = get_project_settings()
    settings.url = url
    process = CrawlerProcess(settings)
    print('in harvest ' + url)
    process.crawl(HarvestSpider)
    process.start()


def lower_list(list_in):
    """Return a list with all words lowercase."""
    list_out = []
    for each in list_in:
        list_out.append(each.lower())
    return list_out


if __name__ == '__main__':
    import sys
    # process = CrawlerProcess(get_project_settings())
    # process.crawl(HarvestSpider)
    # process.start()
    print('in name == main ' + sys.argv[1])
    harvest(sys.argv[1])





# import scrapy
# import collections
# from itertools import dropwhile
# from stop_words import get_stop_words
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings

# # STARTING_URL = 'https://en.wikipedia.org/wiki/Baseball'
# # STARTING_URL = 'https://marc-lj-401.herokuapp.com/'
# # STARTING_URL = ''
# # STARTING_URL = 'http://www.dmoz.org/'
# NUM_OF_OCCURANCES = 3


# def harvest(url):

#     class HarvestSpider(scrapy.Spider):
#         """Spider for harvesting words from a URL."""

#         name = "harvester"

#         print('helo helo helo helo')

#         # custom_settings = {
#         #     'ITEM_PIPELINES': {
#         #         'harvester.pipelines.HarvesterPipeline': 300,
#         #     }
#         # }


#         def start_requests(self):
#             """Starting place for request."""
#             yield scrapy.Request(url=url, callback=self.parse)

#         def parse(self, response):
#             """Get words from site."""
#             words = []
#             headers = []
#             title = []
#             words_in_title = []
#             words_in_headers = []
#             stop_words = get_stop_words('english')
#             h1_res = response.css('h1::text').extract()
#             h2_res = response.css('h2::text').extract()
#             h3_res = response.css('h3::text').extract()
#             h4_res = response.css('h4::text').extract()
#             h5_res = response.css('h5::text').extract()
#             h6_res = response.css('h6::text').extract()
#             title_res = response.css('title::text').extract()
#             p_res = response.css('p::text').extract()

#             for each in p_res:
#                 words.extend(each.split())
#             for each in h1_res:
#                 headers.extend(each.split())
#             for each in h2_res:
#                 headers.extend(each.split())
#             for each in h3_res:
#                 headers.extend(each.split())
#             for each in h4_res:
#                 headers.extend(each.split())
#             for each in h5_res:
#                 headers.extend(each.split())
#             for each in h6_res:
#                 headers.extend(each.split())
#             for each in title_res:
#                 title.extend(each.split())
#             words = lower_list(words)
#             headers = lower_list(headers)
#             title = lower_list(title)
#             for word in words:
#                 if word in headers and word not in stop_words:
#                     words_in_headers.append(word)
#                 if word in title and word not in stop_words:
#                     words_in_title.append(word)
#             word_count = collections.Counter(words)
#             head_count = collections.Counter(headers)
#             title_count = collections.Counter(title)
#             for key, count in dropwhile(lambda key_count: key_count[1] >= NUM_OF_OCCURANCES, word_count.most_common()):
#                 del word_count[key]
#             for key in list(word_count.keys()):
#                 if key in stop_words:
#                     del word_count[key]
#             # with open('log.txt', 'w') as f:
#             #     f.write('keyword: {0}, keyhead: {1}\n'.format(word_count.keys(), word_count.values()))
#             # import pdb; pdb.set_trace()
#             # print(word_count)
#             # print(head_count)
#             # print(title_count)
#             return word_count

#     process = CrawlerProcess(get_project_settings())
#     process.crawl(HarvestSpider)
#     process.start()


# def lower_list(list_in):
#     """Return a list with all words lowercase."""
#     list_out = []
#     for each in list_in:
#         list_out.append(each.lower())
#     return list_out



# if __name__ == '__main__':
#     # process = CrawlerProcess(get_project_settings())
#     # process.crawl(HarvestSpider)
#     # process.start()
#     import sys
#     harvest(sys.argv[1])


# class HarvestSpider(scrapy.Spider):
#     """Spider for harvesting words from a URL."""

#     name = "harvester"

#     custom_settings = {
#         'ITEM_PIPELINES': {
#             'harvester.pipelines.HarvesterPipeline': 300,
#         }
#     }

#     def __init__(self, url=None, *args, **kwargs):
#         """Initialize a harvest spider."""
#         # self.url = url
#         pass

#     def start_requests(self):
#         """Starting place for request."""
#         # yield scrapy.Request(url=self.url, callback=self.parse)
#         yield scrapy.Request(url=STARTING_URL, callback=self.parse)

#     def parse(self, response):
#         """Get words from site."""
#         print('HEEEEEEEEEEEEEEEEEEEEEEEERRRRREEEE')
#         words = []
#         headers = []
#         title = []
#         words_in_title = []
#         words_in_headers = []
#         stop_words = get_stop_words('english')
#         h1_res = response.css('h1::text').extract()
#         h2_res = response.css('h2::text').extract()
#         h3_res = response.css('h3::text').extract()
#         h4_res = response.css('h4::text').extract()
#         h5_res = response.css('h5::text').extract()
#         h6_res = response.css('h6::text').extract()
#         title_res = response.css('title::text').extract()
#         p_res = response.css('p::text').extract()

#         for each in p_res:
#             words.extend(each.split())
#         for each in h1_res:
#             headers.extend(each.split())
#         for each in h2_res:
#             headers.extend(each.split())
#         for each in h3_res:
#             headers.extend(each.split())
#         for each in h4_res:
#             headers.extend(each.split())
#         for each in h5_res:
#             headers.extend(each.split())
#         for each in h6_res:
#             headers.extend(each.split())
#         for each in title_res:
#             title.extend(each.split())
#         words = lower_list(words)
#         headers = lower_list(headers)
#         title = lower_list(title)
#         for word in words:
#             if word in headers and word not in stop_words:
#                 words_in_headers.append(word)
#             if word in title and word not in stop_words:
#                 words_in_title.append(word)
#         word_count = collections.Counter(words)
#         head_count = collections.Counter(headers)
#         title_count = collections.Counter(title)
#         for key, count in dropwhile(lambda key_count: key_count[1] >= NUM_OF_OCCURANCES, word_count.most_common()):
#             del word_count[key]
#         for key in list(word_count.keys()):
#             if key in stop_words:
#                 del word_count[key]
#         return word_count



# def harvest(url):
#     print('++++++++++++++++++++++++++++++++++++++++++++++')
#     print('url inside of harvest ' + url)
#     # import pdb; pdb.set_trace()
#     settings = get_project_settings()
#     # settings.url = url
#     # print('settings.url ' + settings.url)
#     # print('url ' + url)
#     process = CrawlerProcess(settings)
#     process.crawl(HarvestSpider)
#     process.start()


# def lower_list(list_in):
#     """Return a list with all words lowercase."""
#     list_out = []
#     for each in list_in:
#         list_out.append(each.lower())
#     return list_out


# if __name__ == '__main__':
#     process = CrawlerProcess(get_project_settings())
#     process.crawl(HarvestSpider)
#     process.start()
