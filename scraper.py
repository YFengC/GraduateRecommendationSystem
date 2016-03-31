import requests;
from bs4 import BeautifulSoup
import re;

html_parser = "html.parser";

data_map = [];
link_id_rx = "^normalthread_";
thread_link_rx = "^http://www.1point3acres.com/bbs/thread-\d*-\d-\d.html";

english_rx = r'[\x00-\x7f]+'

links_table_class = "threadlisttableid";
footer_id = "fd_page_bottom";

url = "http://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=82&sortid=164&%1=&sortid=164&page=";
page_no = 1;
r = requests.get(url + str(page_no));
tree = BeautifulSoup(r.text, html_parser);

#Total number of pages are in the footer. Should return something ~886
footer = tree.find(id=footer_id).find("div", class_="pg").find("label").find("span");
page_no_limit = int(re.findall(r'\d+', footer.text)[0]);

links = 0;
while page_no <= page_no_limit:
    links = tree.find_all("tbody", id=re.compile(link_id_rx));
    for link in links:
        link_obj = {};
        link_body = link.find("tr").find("th");

        #link of thread must be of a specific format, but there are many links in each table, so get the right one.
        thread_link = list(filter(lambda x: re.compile(thread_link_rx).match(x["href"]) != None, link_body.find_all("a")))[0]["href"];
        link_obj["url"] = thread_link;

        thread_tree = BeautifulSoup(requests.get(thread_link).text, html_parser);

        #it seems that the header is alawys the first 'u' element on the page. haven't found a case otherwise yet.
        thread_header = thread_tree.find("u");
        thread_content = thread_header.find_parent("div");
        thread_items = thread_content.find_all("li");

        thread_header_items = re.compile('\]').split(thread_header.text);
        offer_details = thread_header_items[0][1:];
        univ_details = thread_header_items[1][1:];

        offer_details = re.compile(english_rx).match(offer_details).group(0);
        univ_details = re.compile(english_rx).match(offer_details).group(0);

        offer_details_items = re.compile('\.').split(offer_details);
        year = offer_details_items[0];
        degree = offer_details_items[1];
        acceptance = offer_details_items[2];

        
    break;
    page_no = page_no + 1;
    r = requests.get(url + str(page_no));
    tree = BeautifulSoup(r.text, html_parser);