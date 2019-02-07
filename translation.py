# Create Phalcon translation file from content($t array variables) view, controller and current language file using python file.

import re
import sys


s = {}
path = '/var/www/html/ocex/apps/'

try:
    # Get variables from console
    site = sys.argv[1]
    controller = sys.argv[2]
    action = sys.argv[3]
    language = sys.argv[4]
except:
    print 'You need write in console "site" "controller" "action" "language"'

def findTranslation(data):
    return re.findall('t\[\'(.*?)\'\]', data)

def viewFile(file):
     # Open view file
    with open(file, 'r') as myfile:
        data = myfile.read()
    # Search $t array keys
    result = findTranslation(data);

    partials = re.findall('partial\(\'(.*?)\'\)\?>', data)
    p_result_array = {};

    for partial in partials:
        file=path+site+'/views/partials/'+partial+'.phtml'
        p_result=viewFile(file)
        result=result+p_result


    return result

try:

    file=path+site+'/views/'+controller.lower()+'/'+action+'.phtml'
    result=viewFile(file)

    for i in result:
        if i not in s:
            s[i] = i
except:
    print 'No view file'

try:
    # Open controller file
    with open(path+site+'/controllers/'+controller+'Controller.php', 'r') as myfile:
        data = myfile.read()

    # Search function in controller file
    result = re.findall(action+'Action(.*?)public', data, re.DOTALL)

    # Search $t array keys
    result = findTranslation(result[0]);

    # Add keys to dictionary
    for i in result:
        if i not in s:
            s[i] = i
except:
    print 'No controller file'


try:
    #    Open language file
    file = path+site+'/language/'+language+'/'+controller.lower()+'/' + \
        action+'.php'

    with open(file, 'r') as myfile:
        data = myfile.read()

#   Search text between ""
    result = re.findall('\"(.*?)\"', data)

    i = 0
    key = ''
    for text in result:
        i += 1

#       Check that variables is key or value and add in appropriate place
        if i % 2 == 0:
            s[key] = text
        else:
            s[text] = ''
            key = text

except:
    print 'No language file'

# Print language file content with variables alphabetically sorted
print '<?php \n\n$messages = ['

for t in sorted(s.iterkeys()):
    print ' "' + t + '" => "' + s[t] + '",'

print '];'
