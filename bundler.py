#!/usr/bin/env python3

from os.path import basename, getsize
from json import dumps, dump, load
from os import system
from glob import glob

def quote(item):
	item = item.partition('.')
	return "'"+item[0]+"'."+item[2]

def close():
	print("Closing process")
	exit(0)

def select(container, arg):
	print("")
	for i in range(1, len(container)+1):
		print(f"{i})",container[i-1])
	if arg[0]:
		print(f"{len(container)+1})" , arg[1])
	print(f"{len(container)+1+arg[0]}) None")
	option = int(input(f"\nSelect one of the given {[name for name in globals() if globals()[name] is container][0]}: "))
	if option in range(1, len(container)+1):
		return container[option-1]
	elif option == len(container)+arg[0]:
		return arg[1]
	close()

system("clear")
jars =  glob("*.jar")
jsons = [basename(x) for x in glob("config/*.json")]
icons = glob("*.icns")
with open("config/config.conf", 'r') as file:
		data = {}
		if getsize("config/config.conf"):
			data = load(file)			
		for key in data.keys():
			if key not in jars:
				for json in data[key]:
					jsons.remove(json[:-3] + "json")
if not len(jars):
	print("No jar file found.")
	close()
if len(jsons):
	option = input("+ Press Enter for setup process\n+ Type 'L' for loading config file\n")
else:
	option = ""
if option.lower() == 'l':
	option = select(jsons, (0,0))
	file = open("config/" + option, 'r')
	json = load(file)
	file.close()
	app_name = json["app"]
	jar_file = json["jar"]
	icon_file = json["icon"]
	main_class = json["main"]
	app_version = json["version"]
	if icon_file not in icons and icon_file != "default.icns":
		option = input("\n\"{}\" not found.\n\n+ Press Enter to continue with default.icns\n+ Type 'q' to quit program\n".format(icon_file))
		if option == 'q':
			close()
		icon_file = "default.icns"
else:
	app_name = input("Name of the app: ") + ".app"
	app_version = input("Version of the app: ")
	main_class = input("Name of the main class: ")
	jar_file = select(jars, (0,0))
	icon_file = select(icons, (1,"default.icns"))
	j = {
		"jar":jar_file,
		"icon":icon_file,
		"main":main_class,
		"app":app_name,
		"version":app_version
	}
	file = open("config/{}.json".format(app_name[0:-4]), 'w')
	file.write(dumps(j))
	file.close()
	with open("config/config.conf", 'r+') as file:
		data = {}
		if getsize("config/config.conf"):
			data = load(file)
		file.seek(0)
		if jar_file not in data.keys():
			data.update({jar_file:[app_name]})
		else:
			data[jar_file].append(app_name)
		dump(data, file)
dir = "{}/Contents".format(quote(app_name))
system("mkdir {app} {dir} {dir}/Java {dir}/MacOS {dir}/Resources".format(app = quote(app_name), dir = dir))
if icon_file not in icons:
	system("cp resources/default.icns {}/Resources".format(dir))
else:
	system("cp {icon} {dir}/Resources".format(icon = quote(icon_file), dir = dir))
system("cp resources/Info.plist {dir} && cp resources/executable {dir}/MacOS && cp {jar} {dir}/Java".format(dir = dir, jar = jar_file))
system("mv {dir}/MacOS/executable {dir}/MacOS/'{app}'".format(dir = dir, app = app_name[0:-4]))
with open(dir.replace("'", "") + "/Info.plist", 'r+') as file:
	newdata = file.read().replace("executable", app_name[0:-4]).replace("app_name", app_name[0:-4]).replace("icon_file", icon_file[:-5]).replace("version", app_version).replace("main_class", main_class)
	file.seek(0)
	file.write(newdata)
if input("\nDo you want to delete remaining jar and icon file(s)? (Y/N) ") == 'Y':
	system("rm -rf {}".format(jar_file))
	if icon_file in icons:
		system("rm -rf {}".format(quote(icon_file)))
