from ProspectInstights.InsightTool.scripts.lighthouse import LighthouseRunner as LightRun
import pprint

report = LightRun("https://shop.polymer-project.org/", form_factor="desktop", debug=True).report

print("PASSED:\n")
for item in report.audits["performance"].passed:
    print(item.title, item.display)

print("\n\nFAILED:\n")
for item in report.audits["performance"].failed:
    print(item.title, item.display)
