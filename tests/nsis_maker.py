from string import Template


class MyTemplate(Template):
    delimiter = '&'

# Change parameters
appname = "InfoVision"
compname = "Conscienciology"
descript = "Application for training remote viewing"
vmajor = 1
vminor = 1
vbuild = 2
helpurl = ""
updateurl = ""
abouturl = ""
installsize = 16692
iconpath = "src/images/tapa_olho.ico"
builder = "py"

# ---------------------------------------------------------------#


outfile = f'{appname.replace(" ", "")}-installer-{vmajor}{vminor}{vbuild}-{builder}.exe'
iconpathrev = iconpath.replace("/", '\\')
iconpathrev = f"\\{iconpathrev}"


d = {
    'appname': appname,
    'compname': compname,
    "descript": descript,
    "vmajor": vmajor,
    "vminor": vminor,
    "vbuild": vbuild,
    "helpurl": helpurl,
    "updateurl": updateurl,
    "abouturl": abouturl,
    "installsize": installsize,
    "iconpath": iconpath,
    "outfile": outfile,
    "iconpathrev": iconpathrev,
}

with open('nsis_template.txt', 'r') as f:
    src = MyTemplate(f.read())
    result = src.substitute(d)

with open(f'{appname}-installer-{vmajor}{vminor}{vbuild}.txt', 'w') as g:
    g.write(result)