import requests
from lxml import etree

def html_tables_to_markdown(url_or_html):
    """
    url or html，转换页面上所有table到markdown table
    :param url_or_html:
    :return:
    """
    if url_or_html.startswith('http') or url_or_html.startswith('https'):
        response = requests.get(url_or_html)
        html = etree.HTML(response.text)
    else:
        html = etree.HTML(url_or_html)

    texts = []
    tables = html.xpath("//table")
    for table in tables:
        trs = table.xpath(".//tr")
        for tr in trs:
            trstr = " | ".join([ "".join([text.strip() for text in td.xpath(".//text()")]).replace("|","&#124;")
                for td in tr.xpath("./td | ./th")]).replace("â¦","...")
            texts.append("| "+trstr+" |")
        texts.append("#"*20)

    return "\n".join(texts)

def text_to_markdown_ul(text):
    """把文本转换成markdown形式的无序列表"""
    texts = [ "* " + line.strip()  for line in text.split("\n") if line.strip() != "" ]
    text = "    \n".join(texts)
    return text


def text_addnum(text,addEmptyLine=False):
    """
    在文本前面加上序号
    :param text:
    :param addEmptyLine:
    :return:
    """
    texts = [ "{}、{}".format(str(i),line) + line.strip()
              for i,line in enumerate( filter(lambda x: x.strip() != "",text.split("\n")) , start=1 ) ]
    text = "    \n".join(texts) if not addEmptyLine else "    \n\n".join(texts)
    return text


def html_ul_to_markdown(text):
    """把html ul 转换成markdown形式的无序列表"""
    html = etree.HTML(text)
    text = "    \n".join(["* " + text.strip() for text in html.xpath("//li//text()")] )
    return text