
# Synfig plugin: IK Angle rig v1.0
# Copyright (c) 2024/2025/2026 by ZAINAL AB
#
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import uuid
import xml.etree.ElementTree as ET
import copy
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import pkgutil

gtk_ready = False
try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
    gtk_ready = True
except ModuleNotFoundError:
    print("GTK modul not found. please install GTK.")

if gtk_ready:
	settings = Gtk.Settings.get_default()
	settings.set_property("gtk-application-prefer-dark-theme", True) 

parent_list = None
layer_skeleton = None
guid_data ={}
pilihan = 0

def menu_ik(pilihan_list):
	Gtk.pilihan = -1
	class RadioListBoxWindow(Gtk.Window):
		def __init__(self):
			Gtk.Window.__init__(self, title="IK angle Rig Plugin")
			self.set_border_width(10)
			self.set_default_size(500, 150)

			main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
			self.add(main_vbox)

			main_bbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
			#self.add(main_bbox)

			# List untuk menyimpan RadioButton
			page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
			page1.set_border_width(10)
			page1.pack_start(Gtk.Label(label="Select IK"), False, False, 0)

			self.radio_buttons = []	

			scrolled_window = Gtk.ScrolledWindow()
			scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
			scrolled_window.set_min_content_height(200)
			# Buat ListBox
			self.listbox = Gtk.ListBox()
			self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
			#
			scrolled_window.add(self.listbox)
			page1.pack_start(scrolled_window, False, False, 0)
			main_vbox.pack_start(page1, False, False, 0)

			# Daftar pilihan radio
			choices = ["Pilihan 1", "Pilihan 2", "Pilihan 3", "Pilihan 4", "Pilihan 4", "Pilihan 4", "Pilihan 4"]
			radio_group = None
			idx=0
			for choice in pilihan_list:
				row = Gtk.ListBoxRow()
				hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
				row.add(hbox)

				if radio_group is None:
				    radio_button = Gtk.RadioButton.new_with_label_from_widget(None, choice)
				    radio_group = radio_button
				else:
				    radio_button = Gtk.RadioButton.new_with_label_from_widget(radio_group, choice)

				radio_button.connect("toggled", self.on_radio_toggled)
				radio_button.idx = idx

				self.radio_buttons.append(radio_button)

				hbox.pack_start(radio_button, True, True, 0)
				self.listbox.add(row)

				idx +=1

			self.button = Gtk.Button(label="select IK")
			self.button.info = 1
			self.listbox.add(Gtk.ListBoxRow())
			self.button.connect("clicked", self.on_button_plih)
			main_bbox.pack_start(self.button , True, True, 2)
			
			self.buttonc = Gtk.Button(label="Cancel")
			
			self.buttonc.connect("clicked", self.on_button_cancel)
			main_bbox.pack_end(self.buttonc , False, False, 0)

			main_vbox.pack_start(main_bbox , False, False, 0)
			self.show_all()

		def on_button_cancel(self, button):
			Gtk.pilihan = -1
			Gtk.main_quit()

		def on_button_plih(self, button):
			#global pilihan
			#ilihan = button.info
			Gtk.pilihan = button.info
			Gtk.main_quit()

		def on_radio_toggled(self, radio_button):
			if radio_button.get_active():
				label = radio_button.get_label()
				self.button.set_label(f"CREATE {label}")
				self.button.info = radio_button.idx

	win = RadioListBoxWindow()
	win.connect("destroy", Gtk.main_quit)
	Gtk.main()

	return Gtk.pilihan

def del_meta(root_file):
	for meta in root_file.findall(".//*[@name]"):
		if "ik_" in meta.get('name'):
			root_file.remove(meta)

def add_ikcustom(root_custom_entry,nama):
	el_entry = ET.Element('ik_entry')
	el_entry.attrib['name']=nama
	root_custom_entry.insert(0,el_entry)

def insert_meta(nama,isi,root_file):
	metaadd = ET.Element('meta')
	metaadd.attrib['name']=nama
	metaadd.attrib['content']=isi
	root_file.insert(1,metaadd)

def add_metamenu(root_file,root_custom,pilihan_aktif):
	
	del_meta(root_file)

	list_custom = root_custom.findall(".//ik_entry")

	list_ik = []
	
	ik_basik = ['human rig','single_ik','dino_leg','dinosaurus_rig']
	for ik in ik_basik:
		list_ik.append(ik)

	custom_IKname =[]

	if len(list_custom) >0:
		
		for el_this in list_custom:
			#print(el_this.attrib['name'])
			custom_IKname.append(el_this.attrib['name'])
			list_ik.append(el_this.attrib['name'])
	
		idx_newcustom = 4
		for n in custom_IKname:
			nm = 'ik_menu '+str(idx_newcustom)+' (custom)'
			insert_meta(nm,n,root_file)
			idx_newcustom +=1

	insert_meta('ik_menu ?',str(pilihan_aktif),root_file)
	insert_meta('ik_menu 0','human rig',root_file)
	insert_meta('ik_menu 1','single_ik',root_file)
	insert_meta('ik_menu 2','single leg ik 3 joint',root_file)
	insert_meta('ik_menu 3','dinosaurus_rig',root_file)

	return custom_IKname,list_ik

def replace(parent, el_new):
	parent.remove(parent[0])
	parent.append(el_new)

def ganti_guid(root_file,el_st,el_bones):
	
	# for el_bone in root_file.findall(".//*bone[@type='bone_object']"):
	#  	guid_this = el_bone.get('guid')
	#  	guid_data[guid_this]=guid_this

	# def ganti_id(el_gs):
	# 	for el_g in el_gs:
	# 		new_id =  str(uuid.uuid4())
	# 		guid_data[el_g.get('guid')]=new_id
	# 		el_g.set('guid',new_id)

	def ganti(el_gs):
		for el_g in el_gs:
			if el_g.get('guid') in guid_data:
				id_here = guid_data[el_g.get('guid')]
				el_g.set('guid',id_here)

			else:
				new_id =  str(uuid.uuid4())
				guid_data[el_g.get('guid')]=new_id
				el_g.set('guid',new_id)

	el_bone = root_file.find(".//bone_root")
	
	if el_bone == None: #jika tidak ada bones
		id_root =  str(uuid.uuid4())
		guid_data["root_bone"] = id_root
	else:                         # jika ada bones
		guid_data["root_bone"]=el_bone.attrib['guid']

	el_gs = el_bones.findall(".//*[@guid]")
	ganti(el_gs)
	
	el_gs2 = el_st.findall(".//*[@guid]")
	ganti(el_gs2)
	
def count_ikskeleton(root_file):
	count = 1
	bones = root_file.findall(".//*[@type='skeleton']")		
	
	for el_bone in bones:
		if 'desc' in el_bone.attrib:
			if '_Skeleton' in el_bone.get('desc'):
				count +=1 # jika ada skeleton

	return count

def get_ik_menu(root_file):
	pilihan_ik = '5'
	temp = root_file.find(".//*[@name='ik_menu ?']")
	
	if not temp== None:
		pilihan_ik = temp.get('content')
		
	return pilihan_ik

def masukan_ikcustom(root_custom,XML_ikcustom):
	
	tree_copy = ET.ElementTree(root_custom)
	tree_copy.write(XML_ikcustom)

def find_newikcustem(root,root_custom,path):

	layer_sk = root.find(".//*[@group='new_ik']")
	if not layer_sk == None:

		layer_sk.attrib.pop('group')
		bones_els = []
		#parent_guid = ''
		name_iknew = layer_sk.attrib['desc']
		bone_el = root.find(".//bones")
		bone_root = copy.deepcopy(bone_el.find(".//bone_root"))
		parent_guid = bone_root.attrib['guid']
		bone_root.attrib['guid']="root_bone"
		bones_els.append(bone_root)

		parent_custom_entry =  root_custom.find(".//custom_entry")
		add_ikcustom(parent_custom_entry,name_iknew)

		for el_guid in layer_sk.findall(".//bone"):
			
			guid_id = el_guid.attrib['guid']
		
			for el in bone_el.findall(".//bone"):
				guid_now = el.get('guid')



				if guid_id == guid_now:
					el_c = copy.deepcopy(el)
					for els_guid in el_c.findall(".//*[@guid]"):
						if els_guid.get('guid')==parent_guid:
							els_guid.attrib['guid']="root_bone"

					bones_els.append(el_c)

			
		el_ikbaru = ET.Element(name_iknew)
		for el in bones_els:
			el_ikbaru.insert(0,el)
		
		el_entrybone = copy.deepcopy(layer_sk.find(".//*[@name='bones']"))
		el_entrybone.set('name',name_iknew)

		root_custom.insert(0,el_entrybone)
		root_custom.insert(0,el_ikbaru)

		ET.indent(root_custom)

		masukan_ikcustom(root_custom,path)

		print("+>>   new IK Added")
		return True
	else:
		return False

def cari_parent(root_file):

	global parent_list
	global layer_skeleton
	
	for cari_el in root_file.findall(".//*[@type='skeleton']"):
		if 'desc' in cari_el.attrib:
			
			if ">PARENT" in cari_el.get('desc').upper():
				parent_list = cari_el.find(".//static_list")
				layer_skeleton = cari_el

def masukan_entry(parent_list,el_st,el_newst):

	if parent_list == None:
		replace(el_st, el_newst[0])

	else:
		for el_entry in el_newst.findall(".//entry"):
			
			el_st[0].append(el_entry)

def ik_skeleton(root_file):
	
	#LOAD TEMPLATE
	template_filename = os.path.join(os.path.dirname(sys.argv[0]), 'ik_data_2025.xml')
	tree = ET.parse(template_filename)
	root = tree.getroot()
	
	#LOAD IK_CUSTOM
	XML_ikcustom = os.path.join(os.path.dirname(sys.argv[0]), 'ik_custom.xml')
	tree_custom = ET.parse(XML_ikcustom)
	root_custom = tree_custom.getroot()

	new_ik = find_newikcustem(root_file,root_custom,XML_ikcustom)

	pilihan_ik = int(get_ik_menu(root_file))
	list_iknew,list_ik = add_metamenu(root_file,root_custom,pilihan_ik)
	pilihan_ik = menu_ik(list_ik)

	if pilihan_ik == -1:
		print(" cancel add ik angle rig!")
		return

	insert_meta('ik_menu ?',str(pilihan_ik),root_file)
	print(" Ik no :",str(pilihan_ik))
	#	ADD META MENU

	global guid_data
	
	if not new_ik:
		#el_sk = None
		cari_parent(root_file)
		el_st = None
		el_sk = None
		if parent_list == None:

			el_sk = root.find(".//*[@type='rangkautama']")
			el_st = el_sk.find(".//*[@name='bones']")

		else:
			el_sk = layer_skeleton
			el_st = layer_skeleton.find(".//*[@name='bones']")
			for el_entry in el_st.findall(".//*[@guid]"):
				guid_this = el_entry.get('guid')
				guid_data[guid_this]=guid_this


		el_bones = None
		el_bone_parent = root_file.find(".//bones")
		nama='human'
		
		if pilihan_ik==0:
			
			el_bones = root.find(".//bones")

			if not parent_list == None:
				el_sk = root.find(".//*[@type='rangkautama']")
				el_newst = el_sk.find(".//*[@name='bones']")
				
				masukan_entry(parent_list,el_st,el_newst)

		if pilihan_ik==1:
			nama='single_ik'
			el_bones = root.find(".//singlebones")
			el_newst = root.find(".//*[@name='singlebones']")
			
			masukan_entry(parent_list,el_st,el_newst)
			
		if pilihan_ik==2:
			nama='3 joint bones'
			el_bones = root.find(".//dinobones")
			el_newst = root.find(".//*[@name='dinobones']")
			
			masukan_entry(parent_list,el_st,el_newst)

		if pilihan_ik==3:
			nama='dinosaurus'
			el_bones = root.find(".//dinoindonesia")
			el_newst = root.find(".//*[@name='dinorig']")
			masukan_entry(parent_list,el_st,el_newst)

		if pilihan_ik >3:
			nama = list_iknew[pilihan_ik-4]
			el_bones = root_custom.find(".//{id}".format(id = nama))
			el_newst = root_custom.find(".//*[@name='{id}']".format(id = nama))
			
			masukan_entry(parent_list,el_st,el_newst)

		ganti_guid(root_file,el_st,el_bones)

		if el_bone_parent  == None:
			el = ET.SubElement(root_file, "bones")
			for bone in el_bones:
				el.append(bone)	
			
		else:
			
			for bone in el_bones:
				if not bone.tag == 'bone_root':
					
					el_bone_parent.append(bone)	

		#SET NAME SKELETON
		count = count_ikskeleton(root_file)
		#el_sk = root.find(".//*[@type='rangkautama']") #15 april 2025 del

		if parent_list == None:
			el_sk.attrib['type']='skeleton'
			el_sk.attrib['desc']='('+nama+')_'+str(count)+'_Skeleton'

			root_file.append(el_sk)
		else:
			#pass
			text = layer_skeleton.get('desc')
			pos = text.find(">")
			layer_skeleton.set('desc',text[:pos])

	
	#ET.indent(root_file)
	#tree_copy = ET.ElementTree(root_file)
	#tree_copy.write('/home/mint/Documents/'+'cek_output2025.sif')
	
	print("done...")
	
def inti():
	
	root_file = ET.parse(sys.argv[1]).getroot()
	ik_skeleton(root_file)
	writeTo = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]

	with open(writeTo, "wb") as files:
		files.write(ET.tostring(root_file, encoding="utf-8", xml_declaration=True))

if __name__ == "__main__":
	inti()