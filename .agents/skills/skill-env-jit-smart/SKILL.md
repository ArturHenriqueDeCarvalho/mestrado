---
name: skill-env-jit-smart
description: >-
  Use this skill to configure the isolated Python/PyTorch/Transformers environment (.venv-jit-smart),
  unpack and wire the JIT-Defect4J pickle datasets (data/jitfine/ and data/jitsmart/),
  inspect the Multi-Task Co-Learning architecture (CodeBERT + RobertaClassificationHead + DLN HAN_MODEL + MultiFocalLoss),
  and execute or replicate RQ1-RQ4 and all 6 baselines (LApredict, Deeper, DeepJIT, CC2Vec, JITLine, JIT-Fine)
  in /home/artur-carvalho/mestrado/repos/06-jit-smart.
---

# Skill: Arquitetura de Software e Execução Isolada do Ambiente JIT-Smart & JIT-Fine (Pesquisa 6)

Este runbook habilita o agente (`expert-jit-smart` ou `professor-orientador`) a configurar o ambiente virtual `.venv-jit-smart`, organizar o mapeamento de diretórios de dados (`data/jitfine/` e `data/jitsmart/`) e executar os treinamentos, inferências e baselines das RQs 1 a 4 sobre os 21 projetos Java do **JIT-Defect4J**.

## 1. Referência de Arquitetura Interna

Para o diagrama detalhado de `JITSmart/concat/model.py` (`MultiFocalLoss`, `Attention`, `HAN_MODEL`, `RobertaClassificationHead`, `Model`), `JITSmart/my_util.py` e esquemas dos pickles de linha e commit, consulte:
- [Arquitetura de Software e Diagnóstico de Ambiente](./references/architecture_and_env.md)

## 2. Provisionamento e Verificação do Ambiente Isolado

1. Execute o script de configuração, descompactação e amarração dos pickles (`data/jitfine/` e `data/jitsmart/`):
   [setup_and_verify.sh](./scripts/setup_and_verify.sh)
   ```bash
   bash /home/artur-carvalho/mestrado/.agents/skills/skill-env-jit-smart/scripts/setup_and_verify.sh
   ```
2. O script cria `/home/artur-carvalho/mestrado/repos/06-jit-smart/.venv-jit-smart`, descompacta `data/data.zip` preservando a hierarquia esperada pelos scripts `train_*.sh`, cria os links simbólicos dos rótulos de linha de `JITSmart/process and label defect code lines/*.pkl` em `data/jitsmart/` e verifica `torch`, `transformers`, `scikit-learn`, `pandas`, `numpy` e `openpyxl`.

## 3. Comandos de Execução Individual e Replicação (RQ1 a RQ4 + Baselines)

Com o ambiente `.venv-jit-smart` ativado em `/home/artur-carvalho/mestrado/repos/06-jit-smart/jit-smart`:

```bash
source /home/artur-carvalho/mestrado/repos/06-jit-smart/.venv-jit-smart/bin/activate
cd /home/artur-carvalho/mestrado/repos/06-jit-smart/jit-smart

# 1. Execução dos Baselines Clássicos e Deep Learning (RQ1 & RQ2):
python3 -m baselines.LApredict.lapredict
python3 -m baselines.Deeper.deeper
python3 -m baselines.DeepJIT.deepjit
python3 -m baselines.CC2Vec.cc2vec
python3 -m baselines.JITLine.jitline_rq2
python3 -m baselines.JITLine.jitline_rq3
python3 -m baselines.ngram.evaluate_result

# 2. Execução do JIT-Smart (RQ1: JIT-DP Commit-level & RQ2: JIT-DL Line-level):
bash train_jitsmart.sh
bash train_jitfine.sh

# 3. Execução Cross-Project (RQ3):
python3 "data/jitsmart cross prj data generate.py"
python3 "data/jitfine cross prj data generate.py"
bash train_jitsmart_cross_prj.sh
bash train_jitfine_cross_prj.sh

# 4. Varredura de Pesos da Perda Multi-Tarefa (RQ4: dp_loss_weight 0.1..0.9 vs dl_loss_weight 0.9..0.1):
bash train_jitsmart_loss_weight.sh
```
