import json
from tkinter import Tk, Button, messagebox, filedialog
import ctypes



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



#重置工程
def resetProject(projectDir):
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

	outFile = open(projectDir[0:len(projectDir)-4]+"_reset.svp", "w", encoding="utf8")
	json.dump(svProject, outFile)
	outFile.close()



#按钮按下时
def onButtonClick():
	fileDir = filedialog.askopenfilename(title="选择工程文件",
										filetypes=(("Synthesizer V R2工程文件", "*.svp*"),))
	resetProject(fileDir)
	messagebox.showinfo("处理完成", "已重置工程为"+fileDir[0:len(fileDir)-4]+"_reset.svp")

	


#GUI
mainWindow = Tk()
mainWindow.geometry("240x160")
mainWindow.title("一键重置SV工程")

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
mainWindow.tk.call('tk', 'scaling', ScaleFactor/75)

loadProjectButton = Button(mainWindow, text="选择工程文件", command=onButtonClick,
							height=1, width=10)
loadProjectButton.place(x=70, y=60)

mainWindow.mainloop()