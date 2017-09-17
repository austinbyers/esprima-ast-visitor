# Esprima AST Visitor

This provides a simple Python3 module for pre-order traversal of an Esprima AST.

## JavaScript Parsing with Esprima
[Esprima](http://esprima.org/) is a popular state-of-the-art JavaScript parser.
You can use Esprima's [nodejs package](https://www.npmjs.com/package/esprima)
to parse a JavaScript file and output it's Abstract Syntax Tree (AST) as a JSON file:

```javascript
var esprima = require('esprima');
JSON.stringify(esprima.parse(js_string), null, 2);
```

## AST Format
Esprima's AST follows a [standard format](https://github.com/estree/estree/blob/master/es5.md) specified by the [ESTree project](https://github.com/estree/estree).
While there are other nodejs projects that provide Esprima AST traversal
(e.g. [estraverse](https://github.com/estools/estraverse)), I was unable
to find an equivalent Python tool. So I made one myself!

## Usage
```python
import json

import visitor

ast = json.loads(esprima_ast_string)
program = visitor.objectify(ast)

print(program.type)  # 'Program'
print(program.type_digest)  # SHA256 over all node types in order

for node in program.traverse():
	print(node.type)
```

## Testing
The AST traversal has been tested with a dozen of the most complex real-world
JavaScript samples, including popular libraries like JQuery and Sugar and code
served by the Alexa top 10 sites.

`python3 visitor_test.py`