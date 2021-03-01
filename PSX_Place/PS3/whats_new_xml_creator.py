# Coded for Python 2.7 but with Python 3 syntax (running on OpenMediaVault 4 for Raspberry Pi). OMV run this every hour.

import requests

import base64
from github import Github
from github import InputGitTreeElement

import urllib2

import os

directory = ""
if os.name == 'nt':
	directory = os.getcwd()
else:
	directory = "/srv/dev-disk-by-label-MP4DADi/24_7/Noticias_de_consolas_em_consolas/PSX-Place/PS3"

print("PS3 What's New updater - DADi590")
print("---")
print()

def update_xml():
	print("--> Updating XML...")
	print()

	URL_RSS_PSX_Place = --->RSS feed XML URL here<---

	response = str(urllib2.urlopen(URL_RSS_PSX_Place))

	#response = htmlSource.decode("utf-8")

	response = ""
	for line in urllib2.urlopen(URL_RSS_PSX_Place):
		response += line

	response_list = response.split("\n")

	#for i in response_list:
	#	print(i)
	#	print("---")

	item_location=[]
	for counter, i in enumerate(response_list):
		if "<item>" in i or "</item>" in i:
			item_location.append(counter)
		counter += 1

	counter1 = 0
	counter2 = 0
	titles = []
	URLs = []
	images_not_ready = []
	images = []
	dates = []
	dadi590_descriptions = []
	dadi590_creators = []

	
	file_list = [
		 directory + "/whats_new.xml"
	]

	file_names = [
		'PSX_Place/PS3/whats_new.xml'
	]

	# If this is not here, each update removes lines from the XML for some reason. The separated line from PSX-Place must be removed, or the script won't work decently. This removes all instances on the list.
	list(filter(lambda a: a != '<br/><br/><span style="font-size:12px; color: gray;">(Feed generated with <a href="http://fetchrss.com" target="_blank">FetchRSS</a>)</span>]]></description>', response_list))

	for counter, i in enumerate(response_list):
		if counter1+1 < len(item_location):
			if counter > item_location[counter1] and counter < item_location[counter1+1]:
				if "<title>" in i and "</title>" in i:
					titles.append(response_list[counter][response_list[counter].index(">")+1:response_list[counter].index("</title>")])
				elif "<link>" in i and "</link>" in i:
					URLs.append("http://webproxy.to/browse.php?u="+response_list[counter][response_list[counter].index(">")+1:response_list[counter].index("</link>")])
				elif '<media:content url="' in i and 'medium="image"' in i:
					media_content_lista=response_list[counter].split()
					images_not_ready.append(media_content_lista[1][media_content_lista[1].index("h"):-1])
				elif "<description>" in i:# and "</description>" in i: --> Don't enable this, since it's not in the same line, and that must be the reason for the list(filter(.....)) line above
					descricao = (response_list[counter][response_list[counter].index(">")+1+9:])+"<br/><br/>"#response_list[counter].index("</description>")])
					#print(find_url_psx_place(descricao, 0))
					#exit()
					dadi590_descriptions.append(descricao);
				elif "<dc:creator>" in i and "</dc:creator>" in i:
					dadi590_creators.append(response_list[counter][response_list[counter].index(">")+1:response_list[counter].index("</dc:creator>")])
				elif '<pubDate>' in i and '</pubDate>' in i:
					dates.append(response_list[counter][response_list[counter].index(">")+1:response_list[counter].index("</pubDate>")])
			if item_location[counter1+1]==counter: # Quando acabar um <item>...
				# This checks if there was an error by the RSS feed maker website and it didn't put an image, title, or anything like that.
				# If there's an element missing in one of the lines (which means if the length of the list is less than the supposed),
				# this will add ERROR in the place of the missing element. In case of the images, the error imagem will be used (image of the website from where the news came from).
				if counter2 > len(titles)-1:
					titles.append("ERROR")
				if counter2 > len(URLs)-1:
					URLs.append("ERROR")
				if counter2 > len(images_not_ready)-1:
					images_not_ready.append("ERROR")
				if counter2 > len(dates)-1:
					dates.append("ERROR")
				if counter2 > len(dadi590_descriptions)-1:
					dadi590_descriptions.append("ERROR")
				if counter2 > len(dadi590_creators)-1:
					dadi590_creators.append("ERROR")
				counter1+=2
				counter2+=1

	print(images_not_ready)

	for i in images_not_ready:
		name_image = "ERROR.png"
		if i != "ERROR":
			response = requests.get(i).content

			name_image = i.replace(":","_").replace("/","_").replace("\\","_").replace("=","_").replace('"',"_").replace("?","_").replace("<","_").replace(">","_").replace("|","_")

			if not os.path.isfile(directory + "/" + name_image):
				with open(directory + "/" + name_image,"wb") as image:
					image.write(response)
				image.close()
		images.append("https://raw.githubusercontent.com/DADi590/Console-news-on-consoles/master/PSX_Place/PS3/" + name_image)
		file_list.append(directory + "/" + name_image)
		file_names.append("PSX_Place/PS3/" + name_image)

	# This is to correct the URLs of the images in the descriptions (they'd point to PSX-Place, now they point to GitHub, since the PS3 accepts the GitHub SSL certificate on https://raw.githubusercontent.com)
	for counter, i in enumerate(dadi590_descriptions):
		dadi590_descriptions[counter] = '<img src="' + images[counter] + i[i[10:].index('"') + 10:]

	#print(file_list)
	#print(file_names)

	print(titles)
	#print(URLs)
	#print(images)
	#print(dates)

	with open(directory + "/whats_new.xml") as whats_new_read:
		lines = whats_new_read.read().splitlines()
	whats_new_read.close()

	lines_new = []

	file_titles = []
	for i in lines:
		if "<desc>" in i:
			file_titles.append(i[i.index(">")+1:i.index("</desc>")])

	#print(file_titles)

	lines_new.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
	lines_new.append('<nsx anno="" lt-id="131" min-sys-ver="1" rev="1093" ver="1.0">')
	lines_new.append('\t<spc anno="csxad=1&amp;adspace=9,10,11,12,13" id="33537" multi="o" rep="t">')

	for i in range(0, len(titles)):
		carry_on = True
		for e in file_titles:
			if e == titles[i]:
				carry_on = False
				break
		if carry_on:
			if dates[i] != "ERROR":
				data_lista = dates[i].split()
				second = data_lista[4].split(":")[2]
				minute = data_lista[4].split(":")[1]
				hour = data_lista[4].split(":")[0]
				day = data_lista[1]
				month_name = data_lista[2]
				name_months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
				month = str(name_months.index(month_name))
				year = data_lista[3]

				date_ps3 = year + "-" + month + "-" + day + "T" + hour + ":" + minute + ":" + second + ".000Z"
			else:
				date_ps3 = "ERROR"

			#print(date_ps3)

			lines_new.append('\t\t<mtrl id="0" lastm="' + date_ps3 + '" until="2100-12-31T23:59:00.000Z">')
			lines_new.append('\t\t\t<desc>' + titles[i] + '</desc>')
			lines_new.append('\t\t\t<url type="2">' + images[i] + '</url>')
			lines_new.append('\t\t\t<target type="u">' + URLs[i] + '</target>')
			lines_new.append('\t\t\t<cntry agelmt="0">all</cntry>')
			lines_new.append('\t\t\t<lang>all</lang>')
			lines_new.append('\t\t\t<dadi590_description>' + dadi590_descriptions[i] + '</dadi590_description>')
			lines_new.append('\t\t\t<dadi590_creators>' + dadi590_creators[i] + '</dadi590_creators>')
			lines_new.append('\t\t</mtrl>')

	for i in lines[3:-2]:
		lines_new.append(i)

	lines_new.append('\t</spc>')
	lines_new.append('</nsx>')

	counter1 = 1
	for counter,i in enumerate(lines_new):
		if "<mtrl" in i:
			if counter1 <= 3:
				if not ' anno="picks=1">' in i:
					lines_new[counter] = lines_new[counter][:-1] + ' anno="picks=1">'
			else:
				break
			counter1 += 1

	#print(lines_new)

	if lines != lines_new:
		with open(directory + "/whats_new.xml","w") as whats_new_write:
			for i in lines_new:
				whats_new_write.write(i+'\n')
		whats_new_write.close()

		upload_to_github("PS3", file_list, file_names)
	else:
		print()
		print("--> No news to add.")

def upload_to_github(console, file_list, file_names):
	user = "DADi590"
	with open(directory+"/codigo_github.txt") as github_code_read:
		lines = github_code_read.read().splitlines()
	github_code_read.close()
	password = lines[0]
	github = Github(user, password)
	repo = github.get_user().get_repo('Console-news-on-consoles')

	commit_message = console + " What's New XML update"
	master_ref = repo.get_git_ref('heads/master')
	master_sha = master_ref.object.sha
	base_tree = repo.get_git_tree(master_sha)
	element_list = list()
	for i, entry in enumerate(file_list):
		if entry.endswith('.png') or entry.endswith('.jpg') or entry.endswith('.bmp') or entry.endswith('.gif'):# Or ZIPs or something like that (think it must have binary content or something)
			data = base64.b64encode(open(entry, "rb").read())
			blob = repo.create_git_blob(data.decode("utf-8"), "base64")
			element = InputGitTreeElement(path=file_names[i], mode='100644', type='blob', sha=blob.sha)
			element_list.append(element)
		else:
			with open(entry) as input_file:
				data = input_file.read()
			input_file.close()
			element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
			element_list.append(element)
	tree = repo.create_git_tree(element_list, base_tree)
	parent = repo.get_git_commit(master_sha)
	commit = repo.create_git_commit(commit_message, tree, [parent])
	master_ref.edit(commit.sha)

	print()
	print("--> " + console + " XML updated!")


update_xml()