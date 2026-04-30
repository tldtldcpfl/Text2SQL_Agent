import warnings
warnings.filterwarnings('ignore')

import torch
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
from tqdm.autonotebook import tqdm
from data import train_dataloader

device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"현재 사용 디바이스: {device}")

# 2. 모델 로드
# 다국어 지원되는 인코더로 교체
emb_id = "paraphrase-multilingual-MiniLM-L12-v2"
model = SentenceTransformer(emb_id, device=device) 

# 3. 데이터 준비 (NL user queryion -SQL query 쌍)  

# 4. DataLoader 설정 (M4 성능을 위해 batch_size를 조절해 보세요)
# train_data = train_examples 
# # train_examples list 말고 다른 형식으로 변환 필요 
# train_dataloader = DataLoader(train_data, shuffle=True, batch_size=32)

# 5. 손실 함수 (SentenceTransformer에서 가장 대중적인 Loss)
train_loss = losses.MultipleNegativesRankingLoss(model=model)

# 5. 모델 학습 (Fine-tuning)
num_epochs = 20
warmup_steps = int(len(train_dataloader) * num_epochs * 0.1) # 10% 워밍업

print("Fine-tuning 시작: SQL 에러 수정 궤적 최적화 중...")
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=num_epochs,
    warmup_steps=warmup_steps,
    output_path='./emb_sql_finetuned',
    show_progress_bar=True
) 

# NOTE: 학습된 모델은 허깅페이스 저장소에 얿로드
