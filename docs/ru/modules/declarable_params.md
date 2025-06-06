### Декларированные параметры

Он должен быть статическим (без self) и возвращать словарь с ключами параметров в виде:

`type` _(str)_: тип параметра. Возможные значения:

|Название|Описание|
|--|--|
|`int`|Принимается целое число|
|`float`|Принимается вещественное число|
|`string`|Принимается строка|
|`bool`|Принимается 0 или 1, преобразуется в True или False|
|`array`|Принимается только то значение, что приведено в массиве|
|`object`|Внутренний Python-объект, не может быть задан извне|

<br>

`default` _(any)_: какое значение будет задано, если параметр не передан

`hidden` _(bool)_: параметр скрыт из интерфейса
<br>
`assertion` _(dict)_: словарь, отвечающий за функцию assert:

`not_null` _(bool)_: со значением True будет проверка значение на неравность None.

`assert_link` _(str)_: значение будет привязано к указанному параметру, назовём X. Если текущий параметр равен None, будет проверятся параметр X, если он тоже равен None, будет возвращено AssertionError.

`only_when` _(list)_: массив с проверками на равность других параметров.

<br>

`maxlength` _(int)_: максимальная длина значения, только при `type` = `string`. 

<br>

`docs` _(dict)_: документация к параметру формата:

Ключ `definition` _(localization dict)_: словарь с описанием параметра на разных языках (например, ключи en, ru)

Ключ `examples` _(list)_: массив с примерами значений.

Ключ `values` _(dict)_: только при `type`="array": словарь, объясняющий, что означает тот или иной параметр из `values`. В ключе должно быть название параметра, в значении — _localization dict_.

<br>

`env_property` _(str)_: какое значение из env используется для `default`

`sensitive` _(bool)_: заменять ли значение `default` при показе документации. Рекомендуется ставить на True, если в `default` подставляется информация вроде токена

<br>

#### Имена, которые лучше не использовать

`i`, `display_name`, `description`, `unlisted`, `make_preview`
