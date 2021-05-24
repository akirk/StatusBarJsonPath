import re

import sublime
import sublime_plugin

class CopyJsonPathCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		json_paths = get_json_path(self.view)
		print(json_paths)
		if len(json_paths):
			sublime.set_clipboard( ", ".join(json_paths))

class StatusBarJsonPath(sublime_plugin.EventListener):
	KEY_SIZE = "JSONPath"

	def update_json_path(self, view):
		json_paths = get_json_path(view)
		if len(json_paths):
			view.set_status(self.KEY_SIZE, "JSONPath: " + ", ".join(json_paths))
		else:
			view.erase_status(self.KEY_SIZE)

	on_selection_modified_async = update_json_path

def get_json_path(view):
	json_paths = []
	tag = view.change_count()

	for region in view.sel():
		if view.change_count() != tag:
			# Buffer was changed, we abort our mission.
			return None, None
		start = region.begin()
		end = region.end()
		if view.scope_name(start) != view.scope_name(end):
			break
		if 'source.json' not in view.scope_name(start) or 'source.json' not in view.scope_name(end):
			break

		for scope in view.find_by_selector('source.json'):
			if scope.begin() < start and scope.end() > start:
				break

		if scope is None:
			return None, None

		text = view.substr(scope)
		jsonpath = json_path_to(text, end)

		if jsonpath: json_paths.append(jsonpath)
	return json_paths

# ported from https://github.com/nidu/vscode-copy-json-path/blob/master/src/jsPathTo.ts
def json_path_to(text,offset):
	pos = 0
	stack = []
	is_in_key = False

	while pos < offset:
		# print('json_path_to:step', pos, stack, is_in_key)
		start_pos = pos
		if text[pos] == '"':
			s, new_pos = read_string(text, pos)
			if len(stack):
				frame = stack[-1]
				if frame['col_type'] == 'object' and is_in_key:
					frame['key'] = s
					is_in_key = False
			pos = new_pos
		elif text[pos] == '{':
			stack.append(dict(col_type='object'))
			is_in_key = True
		elif text[pos] == '[':
			stack.append(dict(col_type='array',index=0))
		elif text[pos] == '}' or text[pos] == ']':
			stack.pop()
		elif text[pos] == ',':
			if len(stack):
				frame = stack[-1]
				if frame['col_type'] == 'object':
					is_in_key = True
				elif frame['col_type'] == 'array':
					frame['index'] += 1

		if pos == start_pos: pos += 1
	return path_to_string(stack)

def path_to_string(path):
	s = '';
	for frame in path:
		if frame['col_type'] == 'object':
			if 'key' in frame:
				if re.match(r"^[a-zA-Z0-9_][a-zA-Z0-9_]*$", frame['key']):
					if s: s += '.'
					s += frame['key']
				else:
					key = frame['key'].replace('"', '\\"')
					s += '["' + frame['key'] + '"]'
		else:
			s += '[' + str(frame['index']) + ']'
	return s


def read_string(text, pos):
	p = pos + 1
	i = find_end_quote(text, p)
	# print('read_string: text:', text[p:i], i + 1 )
	return text[p:i], i + 1

# Find the next end quote
def find_end_quote(text, i):
	while i < len(text):
		# print( 'find_end_quote: ' + str(i) + ' : ' + text[i])
		if text[i] == '"':
			bt = i;
			# Handle backtracking to find if this quote is escaped (or, if the escape is escaping a slash)
			while 0 <= bt and text[bt] == '\\': bt -= 1
			if (i - bt) % 2 == 0: break
		i += 1

	return i;
