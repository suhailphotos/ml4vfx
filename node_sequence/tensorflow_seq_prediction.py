import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

data = """
file normal null polyreduce color uvproject filecache
file normal null remesh color filecache
file normal null remesh polydoctor color filecache
file normal null uvflatten polydoctor color filecache
file normal null attribnoise color normal filecache
file normal null polydoctor attribnoise color filecache
file normal null remesh color normal filecache
file normal null polyreduce normal remesh filecache
file remesh normal groupcreate subdivide uvflatten filecache
file polyreduce subdivide uvflatten normal filecache
file normal uvlayout subdivide remesh filecache
file normal groupcreate uvflatten polyreduce filecache
alembic unpack normal voronoifracture pyrosolver rop_alembic
alembic unpack normal voronoifracture vdbfrompolygons pyrosolver rop_alembic
alembic vdbfrompolygons volume convertvdb cache rop_alembic
alembic unpack normal rbdmaterialfracture rbdbulletsolver rop_alembic
alembic unpack voronoifracture rbdconstraintproperties rbdbulletsolver rop_alembic
alembic unpack booleanfracture rbdconstraintproperties rbdbulletsolver rop_alembic
alembic unpack rbdmaterialfracture normal solver rop_alembic
alembic booleanfracture normal solver remesh rop_alembic
alembic unpack voronoifracture rbdconstraintproperties normal rop_alembic
alembic booleanfracture uvflatten rbdmaterialfracture rbdbulletsolver rop_alembic
"""

#tokens
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data.splitlines())
sequences = tokenizer.texts_to_sequences(data.splitlines())
vocab_size = len(tokenizer.word_index) + 1

input_sequences = []
for seq in sequences:
    for i in range(1, len(seq)):
        input_sequences.append(seq[:i+1])

#pad_sequences
max_length = max(len(x) for x in input_sequences)
input_sequences = pad_sequences(input_sequences, maxlen=max_length, padding='pre')

X, y = input_sequences[:,:-1], input_sequences[:,-1]

y = np.array(y)

model = Sequential([
        Embedding(vocab_size, 50, input_length=max_length -1),
        LSTM(100, return_sequences=False),
        Dense(vocab_size, activation='softmax')
    ])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X,y, epochs=50, verbose=2)

def predict_next_words(seed_text, num_words=1):
    for _ in range(num_words):
        tokenized = tokenizer.texts_to_sequences([seed_text])[0]
        tokenized = pad_sequences([tokenized], maxlen=max_length -1, padding='pre')
        predicted = model.predict(tokenized, verbose=0).argmax(axis=-1)
        output_word = tokenizer.index_word[predicted[0]]
        seed_text += ' ' + output_word
    return seed_text


print(predict_next_words("alembic unpack normal", num_words=3))
