---
name: skill-env-cc2vec
description: >-
  Use this skill to configure the isolated PyTorch environment (.venv-cc2vec),
  inspect the 3-level Hierarchical Attention Network (WordRNN, SentRNN, HunkRNN) and Neural Tensor Network comparison layers,
  adapt CUDA calls for CPU-first execution, and execute or replicate the 3 CC2Vec downstream tasks
  (Log Message Generation, Bug-Fixing Patch Identification, and JIT Defect Prediction)
  in /home/artur-carvalho/mestrado/repos/05-cc2vec.
---

# Skill: Arquitetura de Software e Execução Isolada do Ambiente CC2Vec (Pesquisa 5)

Este runbook habilita o agente (`expert-cc2vec` ou `professor-orientador`) a provisionar o ambiente virtual PyTorch `.venv-cc2vec`, adaptar chamadas legadas `.cuda()` para execução determinística em CPU local (`DEC-002`) e executar tanto os 3 pipelines nativos em `/home/artur-carvalho/mestrado/repos/05-cc2vec` quanto o baseline `CC2Vec` sobre o dataset pré-extraído em `/home/artur-carvalho/mestrado/repos/06-jit-smart/jit-smart/data/cc2vec/`.

## 1. Referência de Arquitetura Interna

Para o diagrama completo dos 28 módulos Python (`lmg_*`, `bfp_*`, `jit_*`), dimensões exatas dos tensores 4D ($\mathcal{X} \in \mathbb{Z}^{N \times H \times L \times W}$) e guia de portabilidade PyTorch CPU, consulte:
- [Arquitetura de Software e Diagnóstico de Ambiente](./references/architecture_and_env.md)

## 2. Provisionamento e Verificação do Ambiente Isolado

1. Execute o script de configuração e auditoria arquitetural:
   [setup_and_verify.sh](./scripts/setup_and_verify.sh)
   ```bash
   bash /home/artur-carvalho/mestrado/.agents/skills/skill-env-cc2vec/scripts/setup_and_verify.sh
   ```
2. O script cria `/home/artur-carvalho/mestrado/repos/05-cc2vec/.venv-cc2vec` (ou reutiliza pacotes PyTorch do sistema via `--system-site-packages` para economizar gigabytes de disco), verifica `torch`, `nltk`, `scikit-learn`, `numpy`, `tqdm` e valida a instanciação das classes `WordRNN`, `SentRNN`, `HunkRNN`, `HierachicalRNN`, `PatchNetExtended` e `DeepJITExtended`.

## 3. Comandos de Execução Individual dos 3 Pipelines Downstream

Com o ambiente `.venv-cc2vec` ativado em `/home/artur-carvalho/mestrado/repos/05-cc2vec`:

```bash
source /home/artur-carvalho/mestrado/repos/05-cc2vec/.venv-cc2vec/bin/activate
cd /home/artur-carvalho/mestrado/repos/05-cc2vec

# 1. Tarefa 1 — Log Message Generation (LMG):
python3 lmg_cc2ftr.py -train -train_data <train.pkl> -dictionary_data <dict.pkl>
python3 lmg_cc2ftr.py -predict -pred_data <data.pkl> -dictionary_data <dict.pkl> -load_model <snapshot.pt> -name <out_cc2ftr.pkl>
python3 lmg_eval.py -train_data <train.pkl> -test_data <test.pkl> -train_cc2ftr_data <train_ftr.pkl> -test_cc2ftr_data <test_ftr.pkl>

# 2. Tarefa 2 — Bug-Fixing Patch Identification (BFP + PatchNetExtended):
python3 bfp_cc2ftr.py -train -train_data <train.pkl> -test_data <test.pkl> -dictionary_data <dict.pkl>
python3 bfp_cc2ftr.py -predict -predict_data <data.pkl> -dictionary_data <dict.pkl> -load_model <snapshot.pt> -name <out_cc2ftr.pkl>
python3 bfp_PNExtended.py -train -train_data <train.pkl> -train_data_cc2ftr <train_ftr.pkl> -dictionary_data <dict.pkl>
python3 bfp_PNExtended.py -predict -pred_data <test.pkl> -pred_data_cc2ftr <test_ftr.pkl> -dictionary_data <dict.pkl> -load_model <model.pt>

# 3. Tarefa 3 — Just-In-Time Defect Prediction (JIT + DeepJITExtended):
python3 jit_cc2ftr.py -train -train_data <train.pkl> -test_data <test.pkl> -dictionary_data <dict.pkl>
python3 jit_cc2ftr.py -predict -predict_data <data.pkl> -dictionary_data <dict.pkl> -load_model <snapshot.pt> -name <out_cc2ftr.pkl>
python3 jit_DExtended.py -train -train_data <train_dextend.pkl> -train_data_cc2ftr <train_ftr.pkl> -dictionary_data <dict.pkl>
python3 jit_DExtended.py -predict -pred_data <test_dextend.pkl> -pred_data_cc2ftr <test_ftr.pkl> -dictionary_data <dict.pkl> -load_model <model.pt>
```
