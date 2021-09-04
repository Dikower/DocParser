import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from transformers import AutoModel, BertTokenizerFast
from transformers import AdamW
from sklearn.utils.class_weight import compute_class_weight

class BERT_classifier(nn.Module):

    def __init__(self, bert):
      super(BERT_Arch, self).__init__()

      self.bert = bert 

      self.dropout = nn.Dropout(0.1)
      self.relu =  nn.ReLU()
      self.fc1 = nn.Linear(768,512)
      self.fc2 = nn.Linear(512,2)

      self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, sent_id, mask):
      _, cls_hs = self.bert(sent_id, attention_mask=mask)     
      x = self.fc1(cls_hs)
      x = self.relu(x)
      x = self.dropout(x)
      x = self.fc2(x)
      x = self.softmax(x)

      return x

class RuBert:
  def __init__(self, model_path='saved_weights.pt', gpu=True, max_seq_len=512):
    self.bert = AutoModel.from_pretrained('DeepPavlov/rubert-base-cased-conversational')
    for param in self.bert.parameters():
      param.requires_grad = False

    self.tokenizer = BertTokenizerFast.from_pretrained('DeepPavlov/rubert-base-cased-conversational')
    self.model = BERT_classifier(self.bert)
    self.max_seq_len = max_seq_len
    self.gpu = gpu
    if gpu:
      device = torch.device("cuda")
      self.model = self.model.to(device)

  def pred(self, text_batch):
    tokens = tokenizer.batch_encode_plus(
      text_batch.tolist(),
      max_length = self.max_seq_len,
      pad_to_max_length=True,
      truncation=True,
      return_token_type_ids=False
    )

    seq = torch.tensor(tokens['input_ids'])
    mask = torch.tensor(tokens['attention_mask'])
    with torch.no_grad():
      if self.gpu:
        preds = model(seq.to(device), mask.to(device))
        preds = preds.detach().cpu().numpy()
      else:
        preds = model(seq, mask)
        preds = preds.detach().numpy()
    preds = np.argmax(preds, axis = 1)
    return preds

  def fit(train_texts, train_labels, epochs=10, batch_size=32):
    self.model.train()

    tokens_train = self.tokenizer.batch_encode_plus(
      train_texts.tolist(),
      max_length = self.max_seq_len,
      pad_to_max_length=True,
      truncation=True,
      return_token_type_ids=False
    ) 

    train_seq = torch.tensor(tokens_train['input_ids'])
    train_mask = torch.tensor(tokens_train['attention_mask'])
    train_y = torch.tensor(train_labels.tolist())

    train_data = TensorDataset(train_seq, train_mask, train_y)
    train_sampler = RandomSampler(train_data)
    train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)

    class_wts = compute_class_weight('balanced', np.unique(train_labels), train_labels)
    weights= torch.tensor(class_wts,dtype=torch.float)
    if self.gpu:
      weights = weights.to(device)

    cross_entropy  = nn.NLLLoss(weight=weights) 
    total_loss, total_accuracy = 0, 0
    total_preds=[]
    optimizer = AdamW(self.model.parameters(), lr = 1e-3)

    for step,batch in enumerate(train_dataloader):
      if step % 50 == 0 and not step == 0:
        print('  Batch {:>5,}  of  {:>5,}.'.format(step, len(train_dataloader)))

      if self.gpu:
        batch = [r.to(device) for r in batch]
      else:
        batch = [r for r in batch]
      sent_id, mask, labels = batch

      self.model.zero_grad()        
      preds = self.model(sent_id, mask)

      loss = cross_entropy(preds, labels)
      total_loss = total_loss + loss.item()
      loss.backward()

      torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
      optimizer.step()

      preds=preds.detach().cpu().numpy()
      total_preds.append(preds)

    avg_loss = total_loss / len(train_dataloader)
    total_preds  = np.concatenate(total_preds, axis=0)

    return avg_loss, total_preds
