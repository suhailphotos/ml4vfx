import hou

class NodeUtils:
    def __init__(self):
        pass

    def printTest(self):
        print("Helloooooo")

    def getNetworkAsLinkedList(self, root_node):
        current = root_node

        res = [root_node.type().name()]

        while current.outputs():
            current = current.outputs()[0]
            res.append(current.type().name())
            print(current.type().name())

        return res

    def save_to_file(self, file_path, nodes):
        with open(file_path, 'a') as f:
            for sublist in nodes:
                f.write(' '.join(sublist) + '\n')
