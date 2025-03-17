import torch
import torch.nn as nn
import numpy as np

class LSTMEventDetector(nn.Module):
    def __init__(self, input_size=1024, hidden_size=512, num_classes=5):
        super(LSTMEventDetector, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
        
    def forward(self, x):
        h_lstm, _ = self.lstm(x)
        out = self.fc(h_lstm[:, -1, :])
        return out

class EventDetector:
    def __init__(self, model_path):
        self.model = LSTMEventDetector()
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
        
    def detect_events(self, sequence):
        with torch.no_grad():
            predictions = self.model(sequence)
        return torch.argmax(predictions, dim=1).cpu().numpy() 