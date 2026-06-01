class Project:
     def __int__(self,name,list_task):
         self.name = name
         self.list_task = list_task

class Task:
    def __init__(self,name,status,team):
        self.nameTask=name
        self.status=status
        self.team=team

class TeamMember :
    def __init__(self,member,listTask):
        self.member=member
        self.listTask=listTask

Task1=Task("clear","true","shira")
Task2=Task("hw","false","rut")
project1=Project("do task",[Task1,Task2])
name1 = TeamMember("ruti"[])


