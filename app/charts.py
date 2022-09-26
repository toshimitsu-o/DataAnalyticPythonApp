import matplotlib.pyplot as plt    

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

#generates bar chart
def generate_bar_chart(xAxis, yAxis):
    plt.bar(xAxis,yAxis)
    plt.title('title name')
    plt.xlabel('xAxis name')
    plt.ylabel('yAxis name')
    plt.show()

