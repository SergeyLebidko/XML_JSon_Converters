from xml.dom import minidom
import json


# Создаем тестовый xml
def create_test_xml():
    doc = minidom.Document()

    # Создаем поляну
    glade = doc.createElement('glade')
    doc.appendChild(glade)

    # Создаем траву на поляне
    grass_array = doc.createElement('grass_array')
    grass_list = [doc.createElement('grass') for i in range(5)]
    for index, grass in enumerate(grass_list, start=1):
        grass.appendChild(doc.createTextNode('Травинка '+str(index)))
        grass_array.appendChild(grass)

    # Добавляем траву на поляну
    glade.appendChild(grass_array)

    # Создаем дерево
    tree = doc.createElement('tree')

    # Создаем листья и добавляем их на дерево
    leaf_1 = doc.createElement('leaf')
    leaf_1.setAttribute('color', 'green')
    text_1 = doc.createTextNode('Маленький листочек на деревце')
    leaf_1.appendChild(text_1)

    leaf_2 = doc.createElement('leaf')
    leaf_2.setAttribute('color', 'Зеленый')
    leaf_2.setAttribute('state', 'Целый')
    leaf_2.setAttribute('size', 'Большой')
    leaf_2.setAttribute('age', 'Молодой')

    # Создаем текстовый тег
    text_2 = doc.createTextNode('Маленький листочек на деревце')
    leaf_2.appendChild(text_2)

    # Создаем жука и добавляем его на один из листов
    bug = doc.createElement('bug')
    bug.setAttribute('description', 'Маленький жучок на листочке')
    bug.setAttribute('color', 'Черный')
    leaf_2.appendChild(bug)

    # Добавляем листья на дерево
    tree.appendChild(leaf_1)
    tree.appendChild(leaf_2)

    # Добавляем дерево на поляну
    glade.appendChild(tree)

    # Добавояем комментарий и произвольные данные
    leaf_2.appendChild(doc.createComment('Комментарий внутри документа'))
    leaf_2.appendChild(doc.createCDATASection('<ПРОИЗВОЛЬНЫЕ ДАННЫЕ CDATA/>'))

    # Возвращаем результат в виде екземпляра Document()
    return doc


# Функция парсит xml и выводит его теги, их значения и их параметры. Приведена как пример использования функций minidom
def parse_test_xml(xml_str):
    print('Результаты парсинга:')

    dom = minidom.parseString(xml_str)
    dom.normalize()

    # Получаем список элементов с заданным именем тега.
    # Если тег один, то можно просто обратиться к первому элементу списка
    glade = dom.getElementsByTagName('glade')[0]
    print('Корневой узел: ', glade.nodeName)

    print('Результаты разбора корневого узла:')
    for element in glade.childNodes:

        # Выводим все элементы массива
        if element.nodeName == 'grass_array':
            for grass in element.childNodes:
                print('\t\t', grass.nodeName, ' = ', grass.childNodes[0].nodeValue)

        if element.nodeName == 'tree':
            # Получаем второй листочек с дерева
            leaf_2 = element.childNodes[1]

            # Перебираем его атрибуты
            print('Атрибуты второго листочка:')
            attrs = leaf_2.attributes
            for index in range(len(attrs)):
                print(attrs.item(index).name + ' = '+attrs.item(index).value)

            # Получаем его содержимое
            for leaf_element in leaf_2.childNodes:

                # У элементов есть тип (TEXT_NODE, ELEMENT_NODE, DOCUMENT_NODE), который можно проверить
                if leaf_element.nodeType == leaf_element.TEXT_NODE:
                    print(leaf_element.nodeValue)

                # Пример получения значений атрибутов по их именам
                if leaf_element.nodeType == leaf_element.ELEMENT_NODE:
                    print(
                        leaf_element.nodeName, ' >> ',
                        leaf_element.getAttribute('color'), ' >> ',
                        leaf_element.getAttribute('description')
                    )


# Конвертируем xml в json (на вход функции передается строка с xml)
def convert_to_json(xml_str):
    def _to_json(xml, result=None):
        # Если на вход поступила строка с xml
        if isinstance(xml, str):

            # Преобразовываем строку в документ
            xml = minidom.parseString(xml)
            xml.normalize()

            if result is None:
                result = []

            # Так как на вход поступила текстовая строка с исходным xml, то дочерний узел будет только один - корневой
            _to_json(xml.childNodes[0], result)

            # Возвращаем результат - в данном случае dict с корневым элементом
            return result[0]

        # Если на вход поступил элемент xml, то читаем его название, атрибуты и список дочерних узлов
        if isinstance(xml, minidom.Element):
            result_element = {}

            # Читаем название тега
            title = xml.nodeName
            result_element['title'] = title

            # Читаем атрибуты тега
            attrs = {}
            for index in range(len(xml.attributes)):
                attrs[xml.attributes.item(index).name] = xml.attributes.item(index).value
            result_element['attrs'] = attrs

            # Читаем содержимое тега и рекурсивно записываем его в список content
            content = []
            for node in xml.childNodes:
                _to_json(node, content)
            result_element['content'] = content

            result.append(result_element)

        # Если на вход поступил текстовый узел, то просто добавляем в результат текст из узла
        if isinstance(xml, minidom.Text):
            result.append(xml.nodeValue)
            return

    return _to_json(xml_str)


# Конвертируем json в xml (на вход функции передается словарь json)
def convert_to_xml(json_dict):
    def _to_xml(json_element, parent=None):
        if parent is None:
            parent = minidom.Document()

        # Если добавляем просто текст
        if isinstance(json_element, str):
            # Проверяем, содержит ли текст недопустмые в XML символы
            if set(json_element) & set('<>&"\'/'):
                # Если содержит, то он добавляется как элемент CDATA
                parent.appendChild(minidom.Document().createCDATASection(json_element))
            else:
                # Если не содержит, то он добавляется как простой текстовый узел
                parent.appendChild(minidom.Document().createTextNode(json_element))

            return parent

        # Получаем имя тега
        tag_name = json_element['title']

        # Создаем тег
        tag = minidom.Document().createElement(tag_name)

        # Добавляем атрибуты тегу
        attrs = json_element['attrs']
        for attr in attrs:
            tag.setAttribute(attr, attrs[attr])

        # Перебираем вложенные теги
        content_elements = json_element['content']
        for content_element in content_elements:
            _to_xml(content_element, tag)

        # Добавляем тег к документу
        parent.appendChild(tag)

        return parent

    return _to_xml(json_dict)


def main():
    # Генерируем xml для тестирования.
    # Получаем его от функции в виде экземпляра minidom.Document, чтобы было уобно вывести его в отформатированном виде
    xml_doc = create_test_xml()

    # Выводим сгенерированный xml
    print('\nСгенерирован XML:\n', xml_doc.toprettyxml())

    # Получаем строку с xml, которую будем конвертировать
    xml_str = xml_doc.toxml()

    # Конвертируем xml в json
    json_obj = convert_to_json(xml_str)
    print('\nXML конвертирован в Json:\n', json.dumps(json_obj, indent=2, sort_keys=False, ensure_ascii=False))

    # Конвертируем json в xml
    xml_obj = convert_to_xml(json_obj)
    print('\nJson конвертирован в XML:\n', xml_obj.toprettyxml())


if __name__ == '__main__':
    main()
