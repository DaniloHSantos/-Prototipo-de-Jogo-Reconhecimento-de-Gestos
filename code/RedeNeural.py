from settings import *

class MyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1,3,3,padding=1)
        self.pool = nn.MaxPool2d(2,2)
        self.conv2 = nn.Conv2d(3,9,3)
        self.fc1 = nn.Linear(9*6*6,25)
        self.fc2 = nn.Linear(25,25)
        self.fc3 = nn.Linear(25,6)
        self.R = nn.ReLU()
    def forward(self,x):
        x = self.pool(self.R(self.conv1(x)))
        x = self.pool(self.R(self.conv2(x)))
        x = x.view(-1,9*6*6)
        x = self.R(self.fc1(x))
        x = self.R(self.fc2(x))
        x = self.fc3(x)
        return x.squeeze()
    
class RedeNeural():
    def __init__(self):
        #Inicia e carrega a Rede Neural
        self.CNN = MyCNN()
        self.CNN.load_state_dict(torch.load(join("NeuralNetwork","CNN8.pth")))
        self.SoftMax = nn.Softmax(dim=0)
    def Prediciton(self,Drawing):
        with torch.no_grad():
            #Faz o palpite 
            prediction = self.CNN((torch.from_numpy(np.asarray(Drawing))/255).view(1,28,28))
            prediction_answer = prediction.argmax()

            prediction_value = prediction[prediction_answer]

        return float(prediction_answer),float(prediction_value)