from numpy._core.multiarray import dtype
import gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

env = gym.make('Acrobot-v1', render_mode='human')

class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)

        return x

replay_buffer = deque(maxlen=100000)

#hypers
batch_size = 64
gamma = 0.99
epsilon = 1.0
epsilon_decay = 0.995
epsilon_min = 0.01
learning_rate = 0.001

input_dim = env.observation_space.shape[0]
output_dim = env.action_space.n
dqn = DQN(input_dim, output_dim)
optimizer = optim.Adam(dqn.parameters(), lr=learning_rate)
loss_fn = nn.MSELoss()

def select_action(state, epsilon):
    if random.random() < epsilon:
        return env.action_space.sample()
    else:
        state = torch.tensor(state, dtype=torch.float32)
        q_values = dqn(state)
        return torch.argmax(q_values).item()

#training

episodes = 1001
for episode in range(1, episodes):
    state = env.reset()
    total_reward = 0

    for t in range(1, 501):
        action = select_action(state, epsilon)
        next_state, reward, done, _,_ = env.step(action)
        replay_buffer.append((state, action, reward, next_state, done))

        state = next_state
        total_reward += reward

        if done:
            break

    if len(replay_buffer) > batch_size:
        batch = random.sample(replay_buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.int64).unsqueeze(1)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32)

        current_q = dqn(states).gather(1, actions).squeeze()
        next_q = dqn(next_states).max(1)[0].detach()
        target_q = rewards + (gamma * next_q * (1 - dones))

        loss = loss_fn(current_q, target_q)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()


    if epsilon > epsilon_min:
        epsilon *= epsilon_decay

    print(f"Episode {episode}, Total Reward: {total_reward}")


state = env.reset()

for _ in range(500):
    env.render()
    action = select_action(state, epsilon=0)
    state, _, done, _ = env.step(action)
    if done:
        break

env.close()

