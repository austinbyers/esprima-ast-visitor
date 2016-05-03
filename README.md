# Esprima AST Visitor

This provides a simple Python3 module for pre-order traversal of the JSON represetnation
of an Esprima AST.

## JavaScript Parsing with Esprima
[Esprima](http://esprima.org/) is a popular state-of-the-art JavaScript parser.
You can use Esprima's [nodejs package](https://www.npmjs.com/package/esprima)
to parse a JavaScript file and output it's Abstract Syntax Tree (AST) as a JSON file:

```javascript
var esprima = require('esprima');
JSON.stringify(esprima.parse(js_string), null, 2);
```

## AST Format
Esprima's AST follows a [format](https://github.com/estree/estree/blob/master/spec.md) standardized by the [ESTree project](https://github.com/estree/estree).
While there are other nodejs projects that provide Esprima AST traversal
(e.g. [estraverse](https://github.com/estools/estraverse)), I was unable
to find convenient scripts for traversing the tree in Python.

## Usage
```python
import json
import visitor

for node in visitor.traverse(json.loads(esprima_ast_string)):
    print(node['type'])
    # Do other work with node...
```

## Testing
`python3 visitor_test.py`