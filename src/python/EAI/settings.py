import iris

iris.system.Process.SetNamespace('EAI')

from bp import MyBusinessProcess

CLASSES = {
    'Python.EAI.bp.MyBusinessProcess' : MyBusinessProcess
}