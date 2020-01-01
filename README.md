## Пример работы с XML-Json-конвертерами

Функция create_test_xml создает тестовый xml (в виде объекта Document).

Функция parse_test_xml парсит переданную строку с xml-кодом (но только тем,
 который создан функцией create_test_xml). Эта функция приведена просто как пример
 использования инструментов стандартного пакета xml в Python.

Функция convert_to_json конвертирует переданный в виде строки xml в словарь Python.

Функция convert_to_xml конвертирует переданный словарь Python в объект Document, 
из которого потом могут быть получены как отформатированный xml (для вывода на экран),
так и "чистый" xml-текст для передачи по сети.

XML-тег конвертируется в следующий словарь (json):

```python
{
    'title':'<название тега>',
    'attrs':{
        'атрибут 1':'<значение>',
        'атрибут 2':'<значение>',
        'атрибут ...':'<значение>',
        'атрибут n':'<значение>',
    },
    'content':[
        # Список вложенных тегов
    ]
    
}
```

Пример вывода скрипта:

```
Сгенерирован XML:
 <?xml version="1.0" ?>
<glade>
	<grass_array>
		<grass>Травинка 1</grass>
		<grass>Травинка 2</grass>
		<grass>Травинка 3</grass>
		<grass>Травинка 4</grass>
		<grass>Травинка 5</grass>
	</grass_array>
	<tree>
		<leaf color="green">Маленький листочек на деревце</leaf>
		<leaf age="Молодой" color="Зеленый" size="Большой" state="Целый">
			Маленький листочек на деревце
			<bug color="Черный" description="Маленький жучок на листочке"/>
			<!--Комментарий внутри документа-->
<![CDATA[<ПРОИЗВОЛЬНЫЕ ДАННЫЕ CDATA/>]]>		</leaf>
	</tree>
</glade>


XML конвертирован в Json:
 {
  "title": "glade",
  "attrs": {},
  "content": [
    {
      "title": "grass_array",
      "attrs": {},
      "content": [
        {
          "title": "grass",
          "attrs": {},
          "content": [
            "Травинка 1"
          ]
        },
        {
          "title": "grass",
          "attrs": {},
          "content": [
            "Травинка 2"
          ]
        },
        {
          "title": "grass",
          "attrs": {},
          "content": [
            "Травинка 3"
          ]
        },
        {
          "title": "grass",
          "attrs": {},
          "content": [
            "Травинка 4"
          ]
        },
        {
          "title": "grass",
          "attrs": {},
          "content": [
            "Травинка 5"
          ]
        }
      ]
    },
    {
      "title": "tree",
      "attrs": {},
      "content": [
        {
          "title": "leaf",
          "attrs": {
            "color": "green"
          },
          "content": [
            "Маленький листочек на деревце"
          ]
        },
        {
          "title": "leaf",
          "attrs": {
            "age": "Молодой",
            "color": "Зеленый",
            "size": "Большой",
            "state": "Целый"
          },
          "content": [
            "Маленький листочек на деревце",
            {
              "title": "bug",
              "attrs": {
                "color": "Черный",
                "description": "Маленький жучок на листочке"
              },
              "content": []
            },
            "<ПРОИЗВОЛЬНЫЕ ДАННЫЕ CDATA/>"
          ]
        }
      ]
    }
  ]
}

Json конвертирован в XML:
 <?xml version="1.0" ?>
<glade>
	<grass_array>
		<grass>Травинка 1</grass>
		<grass>Травинка 2</grass>
		<grass>Травинка 3</grass>
		<grass>Травинка 4</grass>
		<grass>Травинка 5</grass>
	</grass_array>
	<tree>
		<leaf color="green">Маленький листочек на деревце</leaf>
		<leaf age="Молодой" color="Зеленый" size="Большой" state="Целый">
			Маленький листочек на деревце
			<bug color="Черный" description="Маленький жучок на листочке"/>
<![CDATA[<ПРОИЗВОЛЬНЫЕ ДАННЫЕ CDATA/>]]>		</leaf>
	</tree>
</glade>
```