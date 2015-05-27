from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

import MySQLdb
import urllib

class Spider_IR(CrawlSpider):
    # MySQL Settings
    db = MySQLdb.connect("localhost", "root", "apmsetup", "CERL_HCD")
    cursor = db.cursor()

    # Scrapy Settings
    name = 'Spider_IE'
    allowed_domains = ['supremecourt.ie']
    start_urls = [
        'http://www.supremecourt.ie/Judgments.nsf/frmSCJudgmentsByYear?OpenForm&Start=1&Count=1000&Expand=1',
        'http://www.supremecourt.ie/Judgments.nsf/frmSCJudgmentsByYear?OpenForm&Start=1&Count=1000&Expand=2',
        'http://www.supremecourt.ie/Judgments.nsf/frmSCJudgmentsByYear?OpenForm&Start=1&Count=1000&Expand=3',
        'http://www.supremecourt.ie/Judgments.nsf/frmSCJudgmentsByYear?OpenForm&Start=1&Count=1000&Expand=4',
        'http://www.supremecourt.ie/Judgments.nsf/frmSCJudgmentsByYear?OpenForm&Start=1&Count=1000&Expand=5',
        'http://www.supremecourt.ie/Judgments.nsf/frmSCJudgmentsByYear?OpenForm&Start=1&Count=1000&Expand=6',
        'http://www.supremecourt.ie/Judgments.nsf/frmSCJudgmentsByYear?OpenForm&Start=1&Count=1000&Expand=7',
        'http://www.supremecourt.ie/Judgments.nsf/frmSCJudgmentsByYear?OpenForm&Start=1&Count=1000&Expand=8',
        'http://www.supremecourt.ie/Judgments.nsf/frmSCJudgmentsByYear?OpenForm&Start=1&Count=1000&Expand=9',
    ]

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('/html/body/form/div[2]/div[2]/table/tbody/tr/td/table//a/@href'))),
        Rule(SgmlLinkExtractor(allow=('http://www.supremecourt.ie/Judgments.nsf/',)), callback='parse_item'),
    )

    # Crawl (by Scrapy) & Restore (by MySQL)
    def parse_item(self, response):
        sel = Selector(response)
        print '====================================='
        case_name = sel.xpath('/html/body/form/div[2]/div[2]/div[4]/table/tr[1]/td[2]/font/text()').extract()
        citation_num = sel.xpath('/html/body/form/div[2]/div[2]/div[4]/table/tr[2]/td[2]/font/text()').extract()
        sct_rec_num = sel.xpath('/html/body/form/div[2]/div[2]/div[4]/table/tr[3]/td[2]/font/text()').extract()
        hct_rec_num = sel.xpath('/html/body/form/div[2]/div[2]/div[4]/table/tr[4]/td[2]/font/text()').extract()
        delivery_date = sel.xpath('/html/body/form/div[2]/div[2]/div[4]/table/tr[5]/td[2]/font/text()').extract()
        court = sel.xpath('/html/body/form/div[2]/div[2]/div[4]/table/tr[6]/td[2]/font/text()').extract()
        justices = sel.xpath('/html/body/form/div[2]/div[2]/div[4]/table/tr[7]/td[2]/font/text()').extract()
        justice_lead = sel.xpath('/html/body/form/div[2]/div[2]/div[4]/table/tr[8]/td[2]/font/text()').extract()
        status = sel.xpath('/html/body/form/div[2]/div[2]/div[4]/table/tr[9]/td[2]/font/text()').extract()

        case_name = str(case_name[0])
        citation_num = str(citation_num[0])
        sct_rec_num = str(sct_rec_num[0])
        hct_rec_num = str(hct_rec_num[0])
        delivery_date = str(delivery_date[0])
        court = str(court[0])
        justices = str(justices[0])
        justice_lead = str(justice_lead[0])
        status = str(status[0])

        file_name = citation_num
        file_name = file_name.lstrip()
        file_name = file_name.rstrip()
        file_name = file_name.replace('[', '')
        file_name = file_name.replace(']', '')
        file_name = file_name.replace(' ', '_')

        urllib.urlretrieve(response.request.url, filename='files/'+file_name+'.html')

        try:
            self.cursor.execute("INSERT INTO ie_cases (hct_rec_num, sct_rec_num, case_name, citation_num, delivery_date, justices, justice_lead, court, status, file_name, timestamp) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', CURRENT_TIMESTAMP)" % (hct_rec_num, sct_rec_num, case_name, citation_num, delivery_date, justices, justice_lead, court, status, file_name+'.html'))
        except:
            print 'Error'