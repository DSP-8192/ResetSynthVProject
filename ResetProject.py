import json
from tkinter import Tk, Button, messagebox, filedialog
import ctypes



#手绘参数名称
parameterNames = ["pitchDelta", "vibratoEnv", "loudness", "tension", "breathiness",
				"voicing", "gender", "toneShift"]




#还原音符组默认设置
def restoreGroupDefaults(group):	
	#遍历所有手绘参数
	for paraName in parameterNames:
		#清空参数点
		group["parameters"][paraName]["points"] = []
	
	#遍历所有音符
	for noteIndex in range(0, len(group["notes"])):
		#读取
		note = group["notes"][noteIndex]
		#清除音符属性
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



#还原轨道默认设置
def restoreTrackDefaults(track):
	#清空主音轨参数
	restoreGroupDefaults(track["mainGroup"])
	#重置主音轨全局参数
	track["mainRef"]["voice"] = {
        "vocalModeInherited": True,
       	"vocalModePreset": "",
       	"vocalModeParams": {}
    }
	#重置音符组全局参数
	for groupIndex in range(0, len(track["groups"])):
		track["groups"][groupIndex]["voice"] = {
			"vocalModeInherited": True,
			"vocalModePreset": "",
			"vocalModeParams": {}
		}



#重置工程
def resetProject(projectDir):
	#打开工程
	inFile = open(projectDir, "r", encoding="utf8")
	svProject = json.loads(inFile.read().rstrip("\x00"))
	inFile.close()

	#遍历音符组库中的每个音符组
	for libIndex in range(0, len(svProject["library"])):
		#重置音符组参数
		restoreGroupDefaults(svProject["library"][libIndex])

	#遍历每个轨道
	for trackIndex in range(0, len(svProject["tracks"])):
		#如果是伴奏轨，不改动
		if(svProject["tracks"][trackIndex]["mainRef"]["isInstrumental"]):
			continue
		#重置轨道参数
		restoreTrackDefaults(svProject["tracks"][trackIndex])

	return svProject



#按钮按下时
def onButtonClick():
	#选择读取工程路径
	inFileDir = filedialog.askopenfilename(title="选择读取的工程文件",
										filetypes=(("Synthesizer V R2工程文件", "*.svp*"),))
	#重置SV工程
	svProjectReset = resetProject(inFileDir)
	#选择保存工程路径
	outFileDir = filedialog.asksaveasfilename(title="选择工程保存路径",
										filetypes=(("Synthesizer V R2工程文件", "*.svp*"),))
	#保存
	if (outFileDir != ""):
		#检查文件路径
		if not outFileDir.endswith(".svp"):
			outFileDir += ".svp"
		#写入
		outFile = open(outFileDir, "w", encoding="utf8")
		json.dump(svProjectReset, outFile)
		outFile.close()
		messagebox.showinfo("处理完成", "已保存重置的工程到" + outFileDir)

	


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