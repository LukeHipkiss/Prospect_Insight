from ProspectInstights.InsightTool.scripts.lighthouse import LighthouseRunner
import pprint

report = LighthouseRunner("https://shop.polymer-project.org/", form_factor="desktop", debug=True).report

print("OUTPUT:\n")
print(report.metric_keys)
print(report.score())
