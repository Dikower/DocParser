import torch
import torch.nn as nn

def get_inferense(test_text, path='saved_weights.pt'):
  model.load_state_dict(torch.load(path))
  tokenizer = BertTokenizerFast.from_pretrained('DeepPavlov/rubert-base-cased-conversational')

  tokens_test = tokenizer.batch_encode_plus(
    test_text.tolist(),
    max_length = max_seq_len,
    pad_to_max_length=True,
    truncation=True,
    return_token_type_ids=False
  )

  test_seq = torch.tensor(tokens_test['input_ids'])
  test_mask = torch.tensor(tokens_test['attention_mask'])

  with torch.no_grad():
    preds = model(test_seq.to(device), test_mask.to(device))
    preds = preds.detach().cpu().numpy()
  preds = np.argmax(preds, axis = 1)
  return preds