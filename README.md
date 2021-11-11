# StatusBarJsonPath
Sublime Text plugin to get the JSONPath (a notation to access the item) under the cursor in a JSON.

The plugin also includes a command _JSONPath: Copy_ to copy the displayed path to the clipboard.

## Example

Given the following JSON object:
```
{
	"name": "Hello World",
	"tags": [
		"example"
	],
	"metadata": {
		"author": "Alex Kirk"
	}
}
```
In this scenario the plugin will display/copy the following JSONPaths:

- Cursor inside "name": `name`
- Cursor inside "Hello World": `name`
- Cursor inside "tags": `tags`
- Cursor inside "example": `tags[0]`
- Cursor inside "metadata": `metadata`
- Cursor inside "author": `metadata.author`

## Demo
![screen recording](statusbarjsonpath.gif)

## Installation

You can install the package manually like this (it has been submitted to https://packagecontrol.io/ but not accepted yet):

1. Click the Preferences > Browse Packages… menu
2. Download https://github.com/akirk/StatusBarJsonPath/archive/refs/heads/main.zip and extract it into that directory (it should then have a subfolde StatusBarJsonPath-main)
3. Restart Sublime Text
