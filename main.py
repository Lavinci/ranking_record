from sites import *

if __name__ == '__main__':
    site_names = [weibo(), zhihu(), bilibili()]
    for site in site_names:
        site.run()
