# Arquitetura de Software e Diagnóstico de Ambiente — CC2Vec (Pesquisa 5)

## 1. Mapeamento dos 28 Módulos Python (`repos/05-cc2vec/`)

```
+-----------------------------------------------------------------------------------+
| PIPELINE 1: LOG MESSAGE GENERATION (lmg_*)                                        |
|  - lmg_padding.py & lmg_utils.py -> Tensorização 4D (Batch x Hunk x Line x Word)  |
|  - lmg_cc2ftr_model.py -> WordRNN, SentRNN, HunkRNN, HierachicalRNN               |
|  - lmg_cc2ftr.py / lmg_cc2ftr_train.py / lmg_cc2ftr_extracted.py                  |
|  - lmg_eval.py -> k-NN Cosine Similarity sobre cc2ftr + BLEU-4                    |
+-----------------------------------------------------------------------------------+
| PIPELINE 2: BUG-FIXING PATCH IDENTIFICATION (bfp_*)                               |
|  - bfp_preprocessing.py, bfp_reformating.py, bfp_extracting.py, bfp_padding.py    |
|  - bfp_cc2ftr_model.py, bfp_cc2ftr.py, bfp_cc2ftr_train.py, bfp_cc2ftr_extracted.py|
|  - bfp_PNExtended_model.py -> PatchNetExtended (CNN 3D + Concatenação cc2ftr)     |
|  - bfp_PNExtended.py, bfp_PNExtended_train.py, bfp_PNExtended_eval.py             |
+-----------------------------------------------------------------------------------+
| PIPELINE 3: JUST-IN-TIME DEFECT PREDICTION (jit_*)                                |
|  - jit_padding.py, jit_DExtended_padding.py, jit_utils.py                         |
|  - jit_cc2ftr_model.py, jit_cc2ftr.py, jit_cc2ftr_train.py, jit_cc2ftr_extracted.py|
|  - jit_DExtended_model.py -> DeepJITExtended (CNN 2D Msg + Code + cc2ftr)         |
|  - jit_DExtended.py, jit_DExtended_train.py, jit_DExtended_eval.py                |
+-----------------------------------------------------------------------------------+
```

## 2. Guia de Portabilidade CPU-First (`torch.cuda.LongTensor` -> CPU)

Nos arquivos `*_cc2ftr_model.py` (ex.: `jit_cc2ftr_model.py` linha 136) e `*_train.py`, o código original de 2020 contém chamadas `torch.cuda.LongTensor(words)` quando `args.cuda` está ativo ou em laços internos.
- **Para execução 100% em CPU local (Intel i7-1255U sem GPU NVIDIA)**:
  1. Passe a flag `-device -1` na linha de comando.
  2. Em `HierachicalRNN.forward_code()`, substitua `torch.cuda.LongTensor(words)` por `torch.LongTensor(words).to(hid_state_word.device)`.
- **Dataset Pré-Empacotado Localmente**: Além dos repositórios do Zenodo (`record/3965149`), o pacote `repos/06-jit-smart/jit-smart/data/data.zip` contém a pasta `data/cc2vec/` (`dataset_dict.pkl`, `features_train.pkl`, `features_test.pkl`, `projects_train.pkl`, `projects_test.pkl`) e o módulo `baselines/CC2Vec/cc2vec.py` pronto para execução cruzada.
