# Arquitetura de Software e Diagnóstico de Ambiente — JIT-Smart & JIT-Fine (Pesquisa 6)

## 1. Diagrama da Arquitetura Multi-Task Co-Learning (`JITSmart/concat/model.py`)

```
+---------------------------------------------------------------------------------------------------+
| ENTRADAS DO BATCH (TextDataset em JITSmart/my_util.py)                                            |
|  1. inputs_ids, attn_masks: [bs, 512] (Msg max 64 + Code [ADD]/[DEL] tokens)                      |
|  2. manual_features: [bs, 14] (14 Expert Features de Kamei normalizadas via MinMaxScaler)         |
|  3. line_ids: [bs, 256, 64] (Matriz 2D por commit: max 256 linhas x max 64 tokens por linha)      |
|  4. labels: [bs] (Rótulo binário do commit) & line_label: [bs, 256] (Rótulo binário de cada linha)|
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                  +-------------------------------+-------------------------------+
                  |                                                               |
                  v                                                               v
+---------------------------------------------------+   +-------------------------------------------+
| RAMO 1: JIT-DP (Commit-Level)                     |   | RAMO 2: JIT-DL (Line-Level DLN/HAN_MODEL) |
|  - encoder: RobertaModel (microsoft/codebert-base)|   |  - Embedding compartilhado com CodeBERT   |
|    Extrai token <s>: x = outputs[0][:, 0, :] (768)|   |  - lstm1 (BiLSTM 768->512) + att1         |
|  - classifier: RobertaClassificationHead          |   |    (need_aggregation=True -> [bs*256,512])|
|    y = tanh(Linear_14->768(manual_features))      |   |  - lstm2 (BiLSTM 512->512) + att2         |
|    logits_dp = Linear_1536->2(Dropout(cat(x, y))) |   |    (need_aggregation=False ->[bs,256,512])|
|    Shape: [bs, 2]                                 |   |  - fc1(512->128) + Tanh + fc2(128->2)     |
|                                                   |   |    han_logits Shape: [bs, 256, 2]         |
+-------------------------+-------------------------+   +---------------------+---------------------+
                          |                                                   |
                          +-------------------------+-------------------------+
                                                    |
                                                    v
+---------------------------------------------------------------------------------------------------+
| FUSÃO CO-SUPERVISIONADA & OTIMIZAÇÃO MULTI-TAREFA                                                 |
|  - Fusão de Logits: logits = (logits_dp + han_logits.mean(dim=1)) / 2                             |
|  - Perda Commit: loss1 = MultiFocalLoss(alpha=0.25, gamma=2)(logits, labels)                      |
|  - Perda Linha:  loss2 = MultiFocalLoss(alpha=0.25, gamma=2)(han_logits.reshape(-1,2), line_label)|
|  - Perda Global: loss  = 0.3 * loss1 + 0.7 * loss2                                                |
+---------------------------------------------------------------------------------------------------+
```

## 2. Mapeamento dos Arquivos de Dados (`data/`)

Ao descompactar `repos/06-jit-smart/jit-smart/data/data.zip` na raiz `jit-smart/`, são populados:
- `data/jitfine/`: `changes_train.pkl`, `changes_valid.pkl`, `changes_test.pkl`, `features_train.pkl`, `features_valid.pkl`, `features_test.pkl`, `changes_complete_buggy_line_level.pkl`.
- `data/cc2vec/`, `data/deepjit/`, `data/deeper/`, `data/la/`, `data/ngram/`: Pickles e TXTs para execução imediata de todos os baselines.
- `data/jitsmart/`: Recebe os arquivos `train_buggy_commit_lines_df.pkl`, `valid_buggy_commit_lines_df.pkl` e `test_buggy_commit_lines_df.pkl` originados de `JITSmart/process and label defect code lines/`.
