import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

# 예제 텍스트 파일 생성 및 저장
# 'positive.txt', 'negative.txt', 'neutral.txt' 파일을 작성하고 각 파일에 해당하는 텍스트 데이터를 저장합니다.
# 한 라인에 하나의 텍스트 데이터를 넣어주세요.

# 예제 텍스트 파일 로드
with open('positive.txt', 'r', encoding='utf-8') as file:
    positive_text = file.readlines()

with open('negative.txt', 'r', encoding='utf-8') as file:
    negative_text = file.readlines()

with open('neutral.txt', 'r', encoding='utf-8') as file:
    neutral_text = file.readlines()

# 데이터 프레임 생성
data = {
    'text': positive_text + negative_text + neutral_text,
    'emotion': ['긍정'] * len(positive_text) + ['부정'] * len(negative_text) + ['중립'] * len(neutral_text)
}

df = pd.DataFrame(data)

# 감정을 숫자로 변환
emotion_mapping = {'긍정': 0, '부정': 1, '중립': 2}
df['emotion'] = df['emotion'].map(emotion_mapping)

# 데이터 전처리
tokenizer = Tokenizer(num_words=10000, oov_token='<OOV>')
tokenizer.fit_on_texts(df['text'])
sequences = tokenizer.texts_to_sequences(df['text'])
padded = pad_sequences(sequences, maxlen=10, padding='post', truncating='post')

# Sequential 모델 생성
model = Sequential([
    Embedding(10000, 16, input_length=10),
    LSTM(32),
    Dense(24, activation='relu'),
    Dropout(0.5),
    Dense(3, activation='softmax')
])

# 모델 컴파일
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 모델 학습
model.fit(padded, df['emotion'], epochs=100)

# pandas를 사용하여 CSV 파일에서 데이터 로드
new_data = pd.read_csv('comments.csv')  # 'new_data.csv'에 파일 이름을 맞게 변경하세요
new_texts = new_data['Comment'].tolist()  # 'text' 열에서 텍스트 데이터를 가져옵니다.

# 텍스트 데이터를 시퀀스로 변환
new_sequences = tokenizer.texts_to_sequences(new_texts)
new_padded = pad_sequences(new_sequences, maxlen=10, padding='post', truncating='post')

# 예측 수행
predictions = model.predict(new_padded)

# 예측 결과 출력
for i, pred in enumerate(predictions):
    predicted_label = np.argmax(pred)
    if predicted_label == 0:
        print(f"'{new_texts[i]}'의 예측 감정: 긍정")
    elif predicted_label == 1:
        print(f"'{new_texts[i]}'의 예측 감정: 부정")
    else:
        print(f"'{new_texts[i]}'의 예측 감정: 중립")
