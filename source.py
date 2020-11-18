from app import appObj

# when using function category.runApp(), visit http://127.0.0.1:8050/ in your web browser.
# for an offline check, run category.offlinePlot

root = 'D:/Files/OneDrive - McGill University/Classes/MUMT 609 - Project/ScriptAnimation/data/installationsList.csv'

AI = 'Artistic Intention'
ID = 'Interaction'
SD = 'System Design'



SyD = appObj(root, SD)
SyD.initiateArray()
SyD.draw(4)
SyD.runApp()
SyD.run()
#SyD.offlinePlot()

df = SyD.df

