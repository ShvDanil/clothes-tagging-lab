# Источники и условия использования

## Таксономия и модели

- [Ximilar Fashion Taxonomy](https://docs.ximilar.com/taxonomy/fashion) и [полный JSON](https://docs.ximilar.com/docs/fashion-taxonomy.json). Включенное сокращение подготовлено из предоставленного снимка; происхождение и checksum — в `data/taxonomy/clothing-v1.json`.
- [TypeSafe: изображения](https://docs.typesafe.ai/images), [Choice](https://docs.typesafe.ai/primitives/choice), [confidence](https://docs.typesafe.ai/confidence). Особенности API проверены по документации 07.11.2026; проверка реального доступа с выданным ключом еще предстоит.
- [Jina CLIP v2](https://jina.ai/models/jina-clip-v2/) и [Embeddings API](https://jina.ai/embeddings/).
- [OpenRouter: документация](https://openrouter.ai/docs) и [модели с изображениями](https://openrouter.ai/models?fmt=cards&input_modalities=image).
- [FastAPI: файлы запросов](https://fastapi.tiangolo.com/tutorial/request-files/), [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/orm/quickstart.html), [готовность зависимостей Compose](https://docs.docker.com/compose/how-tos/startup-order/).

## Данные

Релиз изображений еще готовится; существующего публичного разрешения на перепубликацию фотографий Zara/Massimo Dutti/Uniqlo здесь не заявляется. Доступная веб-страница, отсутствие запрета в robots.txt или паузы между запросами сами по себе не устанавливают условия распространения фотографий. Для каждого выбранного источника в паспорте должны быть основание использования, атрибуция и допустимый способ выдачи.

При подборе альтернатив были рассмотрены:

- [Amazon Berkeley Objects](https://amazon-berkeley-objects.s3.amazonaws.com/index.html): опубликованы условия CC BY 4.0; соответствие требуемым категориям одежды еще нужно проверить.
- [Fashionpedia: лицензии данных](https://fashionpedia.github.io/home/data_license.html): условия аннотаций и изображений необходимо различать.
- [DeepFashion MultiModal](https://github.com/yumingj/DeepFashion-MultiModal#agreement): действуют специальные условия использования и распространения; автоматически включать изображения в публичный репозиторий нельзя.

Выбранный источник фиксируется после проверки. Если данные выдаются отдельно через S3 с ограничениями, их не следует копировать в GitHub. Кодовая MIT-лицензия не распространяется автоматически на изображения, сторонние метаданные, таксономию или веса моделей.

## Примеры оформления задания

Эти репозитории использованы как ориентиры для понятного запуска, критериев, тестирования и сдачи; требования текущего задания изложены в его собственных документах:

- [crm-webhook-sync-lab-v2](https://github.com/H4T3H4K3RS/crm-webhook-sync-lab-v2)
- [recipe-video-extraction-pipeline](https://github.com/VictoriaPugach/recipe-video-extraction-pipeline)
- [redis-cache-lab](https://github.com/rbeketov/redis-cache-lab)

Рабочий notebook организатора не включен: в нем есть проектные результаты и настройки доступа. Его идеи использованы только как исходный контекст, код и выводы ячеек не опубликованы.
