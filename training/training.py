import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import time
from torch.utils.data import TensorDataset, random_split, DataLoader
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt

tfloat = torch.float32
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

class FNN_simp(nn.Module):
    def __init__(self):
        super(FNN_simp,self).__init__()
        self.actF = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        self.lin1 = nn.Linear(10, 100)
        self.lin2 = nn.Linear(100,80)
        self.lin3 = nn.Linear(80,50)
        self.lin4 = nn.Linear(50,30)
        self.lin5 = nn.Linear(30,20)
        self.out = nn.Linear(20, 4)
    def forward(self,t):
        l1 = self.lin1(t)
        h1 = self.actF(l1)
        l2 = self.lin2(h1)
        h2 = self.actF(l2)
        l3 = self.lin3(h2)
        h3 = self.actF(l3)
        l4 = self.lin4(h3)
        h4 = self.actF(l4)
        l5 = self.lin5(h4)
        h5 = self.actF(l5)
        out = self.out(h5)
        out_sigmo = self.sigmoid(out)
        return out_sigmo

def blackbox_function(x):
    y = np.sin(x) + np.cos(2*x)
    return y

#definisikan loss function
def mse_loss(out_pred, out_truth):
    L = ((out_pred-out_truth).pow(2)).mean()
    return L

def mae_loss(out_pred, out_truth):
    L = ((out_pred-out_truth).abs()).mean()
    return L

def mape_metric(out_pred,out_truth):
    L = torch.abs(out_pred-out_truth)/out_truth
    return L

def ground_truth2(validation_split = 0.3, random_seed=41):
    data_input = np.loadtxt('modified_input.csv', delimiter=',')
    data_output = np.loadtxt('modified_output.csv', delimiter=',')

    # Split the dataset first (before normalization)
    train_input, val_input, train_output, val_output = train_test_split(
        data_input, data_output, test_size=validation_split, random_state=random_seed
    )

    # Compute normalization statistics **ONLY from the training set**
    input_min = np.min(train_input, axis=0)
    input_max = np.max(train_input, axis=0)
    output_min = np.min(train_output, axis=0)
    output_max = np.max(train_output, axis=0)

    # Apply min-max normalization using only training set statistics
    train_input_norm = (train_input - input_min) / (input_max - input_min)
    val_input_norm = (val_input - input_min) / (input_max - input_min)

    train_output_norm = 0.1 + (0.8 * (train_output - output_min) / (output_max - output_min))
    val_output_norm = 0.1 + (0.8 * (val_output - output_min) / (output_max - output_min))

    # Convert to PyTorch tensors
    tfloat = torch.float32  # Ensure consistent float dtype
    train_input_tensor = torch.tensor(train_input_norm, dtype=tfloat)
    train_output_tensor = torch.tensor(train_output_norm, dtype=tfloat)
    val_input_tensor = torch.tensor(val_input_norm, dtype=tfloat)
    val_output_tensor = torch.tensor(val_output_norm, dtype=tfloat)

    return train_input_tensor, train_output_tensor, val_input_tensor, val_output_tensor


#untuk scatter plot, kita butuh data yang outputnya bukan tensor
def scatter_data(validation_split = 0.3, random_seed=42):
    data_input = np.loadtxt('file_input.csv',delimiter=',')
    data_output = np.loadtxt('file_output.csv',delimiter=',')
    #selama formantnya masih numpy, mestinya kita bisa split. Kita split dulu di sini
    train_input, val_input, train_output, val_output = train_test_split(
        data_input, data_output, test_size=validation_split, random_state=random_seed
    )
    return train_input, train_output, val_input, val_output

def main(n,lr,epochs, batch_number):
    torch.manual_seed(n)
    np.random.seed(n)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(n)
    waktu0 = time.time()
    #kita mau definisikan beberapa model, tapi kayaknya mending iterasi di main aja
    f_connected = FNN_simp().to(device)
    #loading data, sudah displit
    train_input, train_output, val_input, val_output = ground_truth2()
    betas = [0.9,0.999] #ini nilai pasnya berapa mungkin perlu cari referensi dulu
    loss = 0
    loss1 = 0
    loss2 = 0
    loss3 = 0
    loss4 = 0
    val_loss = 0
    val_loss1 = 0
    val_loss2 = 0
    val_loss3 = 0
    val_loss4 = 0
    optimizer = optim.Adam(f_connected.parameters(), lr=lr, betas=betas)
    batch_size = int(len(train_input)/batch_number)
    for tt in range(epochs):
        idx = np.random.permutation(len(train_input))
        shuf_train_input = train_input[idx]
        shuf_train_output = train_output[idx]
        loss = 0
        loss1 = 0
        loss2 = 0
        loss3 = 0
        loss4 = 0
        train_start, train_end = 0, batch_size
        for i in range(batch_number):
            mb_input = shuf_train_input[train_start:train_end].to(device)
            mb_output = shuf_train_output[train_start: train_end].to(device)
            #print("mb_input_shape:", mb_input.shape)
            #print("mb_output_shape:", mb_output.shape)
            pred = f_connected(mb_input).to(device)
            loss_batch = mse_loss(pred, mb_output)
            loss1batch = mse_loss(pred[:,0], mb_output[:,0])
            loss2batch = mse_loss(pred[:,1], mb_output[:,1])
            loss3batch = mse_loss(pred[:,2], mb_output[:,2])
            loss4batch = mse_loss(pred[:,3], mb_output[:,3])
            loss_batch.backward()
            optimizer.step()
            loss += loss_batch.cpu().data.numpy()
            loss1 += loss1batch.cpu().data.numpy()
            loss2 += loss2batch.cpu().data.numpy()
            loss3 += loss3batch.cpu().data.numpy()
            loss4 += loss4batch.cpu().data.numpy()
            optimizer.zero_grad()
            #update batch
            train_start += batch_size; train_end += batch_size

        with torch.no_grad():
            val_input = val_input.to(device)
            val_output = val_output.to(device)
            val_pred = f_connected(val_input).to(device)
            val_loss = mse_loss(val_pred, val_output).cpu().data.numpy()
            val_loss1 = mse_loss(val_pred[:,0], val_output[:,0]).cpu().data.numpy()
            val_loss2 = mse_loss(val_pred[:,1], val_output[:,1]).cpu().data.numpy()
            val_loss3 = mse_loss(val_pred[:,2], val_output[:,2]).cpu().data.numpy()
            val_loss4 = mse_loss(val_pred[:,3], val_output[:,3]).cpu().data.numpy()
        if tt%100 == 0:
            print('epoch:', tt , ' train_loss: ', loss, ' val_loss: ', val_loss)
            print('train_loss1', loss1, 'val_loss1', val_loss1)
            print('train_loss2', loss2, 'val_loss2', val_loss2)
            print('train_loss3', loss3, 'val_loss3', val_loss3)
            print('train_loss4', loss4, 'val_loss4', val_loss4)
        if tt == 8000:
            new_lr = 2e-4
            for param_group in optimizer.param_groups:
                param_group['lr'] = new_lr
        if tt == 15000:
            new_lr = 1e-4
            for param_group in optimizer.param_groups:
                param_group['lr'] = new_lr

    #save model
    torch.save(f_connected.state_dict(), 'models/sigm-out_relu-hidden_mse_%d.pt' %n)
    waktuf = time.time()
    print(waktuf-waktu0)
    return loss, val_loss, loss1, loss2, loss3, loss4, val_loss1, val_loss2, val_loss3, val_loss4
nomor = []
train_loss_total = []
val_loss_total = []
train_loss_1 = []
val_loss_1 = []
train_loss_2 = []
val_loss_2 = []
train_loss_3 = []
val_loss_3 = []
train_loss_4 = []
val_loss_4 = []

i=0
while i<200:
    loss, val_loss, loss1, loss2, loss3, loss4, val_loss1, val_loss2, val_loss3, val_loss4 = main(i, 5e-4, 20000,1)
    nomor.append(i)
    train_loss_total.append(loss)
    val_loss_total.append(val_loss)
    train_loss_1.append(loss1)
    val_loss_1.append(val_loss1)
    train_loss_2.append(loss2)
    val_loss_2.append(val_loss2)
    train_loss_3.append(loss3)
    val_loss_3.append(val_loss3)
    train_loss_4.append(loss4)
    val_loss_4.append(val_loss4)
    i = i+1

output = np.vstack([nomor, train_loss_total, val_loss_total, train_loss_1, val_loss_1, train_loss_2, val_loss_2, train_loss_3, val_loss_3, train_loss_4, val_loss_4])
output = np.transpose(output)
np.savetxt('output_ensemble_mse.csv', output, delimiter=',')
