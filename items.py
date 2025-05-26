2025-05-26 16:14:40 [twisted] CRITICAL:
Traceback (most recent call last):
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\twisted\internet\defer.py", line 2017, in _inlineCallbacks
    result = context.run(gen.send, result)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\scrapy\crawler.py", line 156, in crawl
    self.engine = self._create_engine()
                  ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\scrapy\crawler.py", line 169, in _create_engine
    return ExecutionEngine(self, lambda _: self.stop())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\scrapy\core\engine.py", line 111, in __init__
    self.scraper: Scraper = Scraper(crawler)
                            ^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\scrapy\core\scraper.py", line 107, in __init__
    self.itemproc: ItemPipelineManager = itemproc_cls.from_crawler(crawler)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\scrapy\middleware.py", line 77, in from_crawler
    return cls._from_settings(crawler.settings, crawler)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\scrapy\middleware.py", line 86, in _from_settings
    mwcls = load_object(clspath)
            ^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\.venv\Lib\site-packages\scrapy\utils\misc.py", line 71, in load_object
    mod = import_module(module)
          ^^^^^^^^^^^^^^^^^^^^^
  File "C:\ProgramData\anaconda3\Lib\importlib\__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\urd_scraper\pipelines.py", line 11, in <module>
    from urd_scraper.models import Udr, Base
  File "C:\Users\Hammadhussain\PycharmProjects\Module5\urd_scraper\models.py", line 18, in <module>
    class Udr(Base):
TypeError: function() argument 'code' must be code, not str
