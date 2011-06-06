##################################################
#
# File: newDiffHelper.py
# Description:
#   Helper function for "newDiffHelper.py", containing function definitions
#   and implementations.
#
##################################################
import re
import sys

## function: covFileProcess("coverage.xml file")
##   Return a dictionary: {pkgname, {classFile, {covType, data}}}
def covFileProcess(covFile):
    lines = covFile.readlines()

    pkgName = None
    className = None
    result = {}
    for item in lines:
        item = item.strip()

        # pkg name: 
        if item.startswith(r'<package name="'):
            # print item
            m = re.match(r'<package name="(.+)" line-rate', item)
            # print m.group(1)
            pkgName = m.group(1)
            if pkgName not in result:
                result[pkgName] = {}
            else:
                print "Error ! Wired, two identical package names in the same file!"
                sys.exit(1)
            
            continue

        elif item.startswith(r'<class name="'):
            className = re.match(r'<class name="(.+)" filename', item).group(1)
            line_rate = float(re.match(r'.+line-rate="(.+)" branch.+', item).group(1))
            br_rate = float(re.match(r'.+branch-rate="(.+)" complexity.+', item).group(1))
            # print "class: ", className, "lineCov:", line_rate, "branchCov:", br_rate
            result[pkgName][className] = {}
            result[pkgName][className]["lineCov"] = line_rate
            result[pkgName][className]["branchCov"] = br_rate

    return result
