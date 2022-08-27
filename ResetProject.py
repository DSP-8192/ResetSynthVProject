import json
import os



#参数名称
parameterNames = ["pitchDelta", "vibratoEnv", "loudness", "tension", "breathiness",
				"voicing", "gender", "toneShift"]




#还原音符组默认设置
def restoreGroupDefaults(group):	
	#遍历所有参数
	for paraName in parameterNames:
		#清空参数
		group["parameters"][paraName]["points"] = []
	
	#遍历所有音符
	for noteIndex in range(0, len(group["notes"])):
		#读取
		note = group["notes"][noteIndex]
		#恢复默认
		note["phonemes"] = ""
		note["detune"] = 0
		note["attributes"] = {}
		note["systemAttributes"] = {}
		note["pitchTakes"] = {
			"activeTakeId": 0,
			"takes": [
				{
					"id": 0,
					"expr": 1.0,
					"liked": False
				}
			]
		}
		note["timbreTakes"] = {
			"activeTakeId": 0,
			"takes": [
				{
					"id": 0,
					"expr": 1.0,
					"liked": False
				}
			]
		}
		#写入
		group["notes"][noteIndex] = note
	
	#返回
	return group




#文件路径
print("清理SV工程中的所有参数和音符属性")
projectDir = input("请输入完整的工程路径（不要包括引号）：")


#打开工程
inFile = open(projectDir, "r", encoding="utf8")
svProject = json.loads(inFile.read().rstrip("\x00"))
inFile.close()


#遍历音符组库中的每个音符组
for libIndex in range(0, len(svProject["library"])):
	#还原默认
	noteGroup = svProject["library"][libIndex]
	noteGroup = restoreGroupDefaults(noteGroup)
	svProject["library"][libIndex] = noteGroup


#遍历每个轨道中的主音符组
for trackIndex in range(0, len(svProject["tracks"])):
	#如果是伴奏轨，不改动
	if(svProject["tracks"][trackIndex]["mainRef"]["isInstrumental"]):
		continue
	#还原默认
	noteGroup = svProject["tracks"][trackIndex]["mainGroup"]
	noteGroup = restoreGroupDefaults(noteGroup)
	svProject["tracks"][trackIndex]["mainGroup"] = noteGroup


outFile = open(projectDir, "w", encoding="utf8")
json.dump(svProject, outFile)
outFile.close()
print("完成")
os.system("pause")