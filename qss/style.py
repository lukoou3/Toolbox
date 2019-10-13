def setScrollBarStyle(widget):
    """先不用chardet.detect推测编码了，会输出日志
    import chardet
    with open("qss/ScrollBar.qss", "rb") as fp:
        content = fp.read()
        encoding = chardet.detect(content) or {}
        content = content.decode(encoding.get("encoding") or "utf-8")
    """
    with open("qss/ScrollBar.qss", "r", encoding="utf-8") as fp:
        content = fp.read()
    
    # 设置样式
    widget.setStyleSheet(content)