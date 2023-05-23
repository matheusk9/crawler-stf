import sys

from src.modules.crawler import Crawler

data = sys.argv[1]
Crawler(data).run()
