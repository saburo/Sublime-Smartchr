import re
import sublime
import sublime_plugin


class SmartchrCommand(sublime_plugin.TextCommand):
    def run(self, edit, chrs):
        v = self.view
        listIndex = len(chrs) - 1
        for (i, curChr) in enumerate(chrs):
            # remove snippet related characters ($0)
            realChr = re.sub(r"\\", '', re.sub(r"\$\d+", '', curChr))
            realChrLen = len(realChr)
            tmpCur = re.sub(r"\\", '', curChr).find('$0')
            curOffset = realChrLen if tmpCur == -1 else tmpCur
            curStart = v.sel()[0].a - curOffset  # current position
            region = sublime.Region(curStart, curStart + realChrLen)
            if v.substr(region) == realChr:
                v.erase(edit, region)
                break
        next = 0 if listIndex == i else i + 1

        v.run_command('insert_snippet', {"contents": chrs[next]})
