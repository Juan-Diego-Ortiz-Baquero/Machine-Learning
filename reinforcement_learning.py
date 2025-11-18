"""
Implementación del sistema de Aprendizaje por Refuerzo (Reinforcement Learning)
Incluye un entorno GridWorld y un agente Q-Learning para demostrar conceptos básicos de RL.
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
from collections import defaultdict
import seaborn as sns
import base64
from io import BytesIO

class GridWorldEnvironment:
    """
    Entorno GridWorld: Un mundo en grilla donde el agente debe navegar hasta una meta
    evitando obstáculos y recibiendo recompensas/castigos por sus acciones.
    """
    
    def __init__(self, grid_size=(5, 5), start_pos=(0, 0), goal_pos=(4, 4), obstacles=None):
        self.grid_size = grid_size
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.current_pos = start_pos
        self.obstacles = obstacles or [(1, 1), (2, 2), (3, 1)]
        
        # Definir acciones: 0=arriba, 1=derecha, 2=abajo, 3=izquierda
        self.actions = ['up', 'right', 'down', 'left']
        self.action_space = len(self.actions)
        
        # Definir recompensas
        self.rewards = {
            'goal': 100,      # Llegar a la meta
            'obstacle': -10,   # Chocar con obstáculo
            'step': -1,       # Cada paso (incentiva eficiencia)
            'wall': -5        # Intentar salir del grid
        }
        
        self.max_steps = 50  # Máximo de pasos por episodio
        self.current_step = 0
        
    def reset(self):
        """Reinicia el entorno al estado inicial"""
        self.current_pos = self.start_pos
        self.current_step = 0
        return self._get_state()
    
    def _get_state(self):
        """Convierte la posición actual en un estado numérico"""
        return self.current_pos[0] * self.grid_size[1] + self.current_pos[1]
    
    def _is_valid_position(self, pos):
        """Verifica si una posición es válida (dentro del grid y sin obstáculos)"""
        row, col = pos
        if row < 0 or row >= self.grid_size[0] or col < 0 or col >= self.grid_size[1]:
            return False
        if pos in self.obstacles:
            return False
        return True
    
    def step(self, action):
        """
        Ejecuta una acción en el entorno
        Returns: (next_state, reward, done, info)
        """
        self.current_step += 1
        
        # Mapear acción a movimiento
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left
        move = moves[action]
        new_pos = (self.current_pos[0] + move[0], self.current_pos[1] + move[1])
        
        # Calcular recompensa y nueva posición
        if not self._is_valid_position(new_pos):
            if new_pos in self.obstacles:
                reward = self.rewards['obstacle']
            else:
                reward = self.rewards['wall']
            # No mover el agente si la posición es inválida
            new_pos = self.current_pos
        else:
            self.current_pos = new_pos
            if new_pos == self.goal_pos:
                reward = self.rewards['goal']
            else:
                reward = self.rewards['step']
        
        # Verificar si el episodio terminó
        done = (self.current_pos == self.goal_pos) or (self.current_step >= self.max_steps)
        
        next_state = self._get_state()
        info = {'steps': self.current_step, 'position': self.current_pos}
        
        return next_state, reward, done, info
    
    def render(self):
        """Visualiza el estado actual del entorno"""
        grid = np.zeros(self.grid_size)
        
        # Marcar obstáculos
        for obs in self.obstacles:
            grid[obs] = -1
        
        # Marcar meta
        grid[self.goal_pos] = 2
        
        # Marcar agente
        grid[self.current_pos] = 1
        
        return grid

class QLearningAgent:
    """
    Agente que implementa el algoritmo Q-Learning para aprender políticas óptimas
    """
    
    def __init__(self, state_space, action_space, learning_rate=0.1, 
                 discount_factor=0.95, exploration_rate=1.0, exploration_decay=0.995,
                 min_exploration_rate=0.01):
        
        self.state_space = state_space
        self.action_space = action_space
        self.learning_rate = learning_rate  # α (alpha)
        self.discount_factor = discount_factor  # γ (gamma)
        self.exploration_rate = exploration_rate  # ε (epsilon)
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        
        # Tabla Q: Q(state, action) -> valor esperado
        self.q_table = defaultdict(lambda: np.zeros(action_space))
        
        # Métricas de entrenamiento
        self.episode_rewards = []
        self.episode_steps = []
        self.exploration_rates = []
        
    def choose_action(self, state, training=True):
        """
        Selecciona una acción usando política ε-greedy
        """
        if training and np.random.random() < self.exploration_rate:
            # Exploración: acción aleatoria
            return np.random.randint(0, self.action_space)
        else:
            # Explotación: mejor acción conocida
            return np.argmax(self.q_table[state])
    
    def learn(self, state, action, reward, next_state, done):
        """
        Actualiza la tabla Q usando la ecuación de Q-Learning
        """
        current_q = self.q_table[state][action]
        
        if done:
            # Si el episodio terminó, no hay estado futuro
            target_q = reward
        else:
            # Q-Learning: usa el máximo Q-valor del siguiente estado
            max_next_q = np.max(self.q_table[next_state])
            target_q = reward + self.discount_factor * max_next_q
        
        # Actualización de la tabla Q
        self.q_table[state][action] = current_q + self.learning_rate * (target_q - current_q)
    
    def decay_exploration(self):
        """Reduce la tasa de exploración"""
        self.exploration_rate = max(
            self.min_exploration_rate,
            self.exploration_rate * self.exploration_decay
        )
    
    def save_model(self, filepath):
        """Guarda el modelo entrenado"""
        model_data = {
            'q_table': dict(self.q_table),
            'episode_rewards': self.episode_rewards,
            'episode_steps': self.episode_steps,
            'exploration_rates': self.exploration_rates,
            'parameters': {
                'learning_rate': self.learning_rate,
                'discount_factor': self.discount_factor,
                'exploration_rate': self.exploration_rate
            }
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath):
        """Carga un modelo entrenado"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.q_table = defaultdict(lambda: np.zeros(self.action_space), model_data['q_table'])
            self.episode_rewards = model_data.get('episode_rewards', [])
            self.episode_steps = model_data.get('episode_steps', [])
            self.exploration_rates = model_data.get('exploration_rates', [])
            
            params = model_data.get('parameters', {})
            self.learning_rate = params.get('learning_rate', self.learning_rate)
            self.discount_factor = params.get('discount_factor', self.discount_factor)
            self.exploration_rate = params.get('exploration_rate', self.exploration_rate)
            
            return True
        return False

class RLTrainer:
    """
    Clase para entrenar y visualizar el agente de Reinforcement Learning
    """
    
    def __init__(self, env, agent):
        self.env = env
        self.agent = agent
        self.training_history = []
        
    def train(self, episodes=1000, verbose=True):
        """
        Entrena el agente por un número específico de episodios
        """
        for episode in range(episodes):
            state = self.env.reset()
            total_reward = 0
            steps = 0
            
            while True:
                # Elegir y ejecutar acción
                action = self.agent.choose_action(state, training=True)
                next_state, reward, done, info = self.env.step(action)
                
                # Aprender de la experiencia
                self.agent.learn(state, action, reward, next_state, done)
                
                state = next_state
                total_reward += reward
                steps += 1
                
                if done:
                    break
            
            # Registrar métricas del episodio
            self.agent.episode_rewards.append(total_reward)
            self.agent.episode_steps.append(steps)
            self.agent.exploration_rates.append(self.agent.exploration_rate)
              # Reducir exploración
            self.agent.decay_exploration()
            
            # Mostrar progreso
            if verbose and (episode + 1) % 100 == 0:
                avg_reward = np.mean(self.agent.episode_rewards[-100:])
                print(f"Episodio {episode + 1}/{episodes}, "
                      f"Recompensa promedio: {avg_reward:.2f}, "
                      f"Exploración: {self.agent.exploration_rate:.3f}")
    
    def test_agent(self, episodes=10):
        """
        Prueba el agente entrenado sin exploración
        """
        test_rewards = []
        test_paths = []
        
        for episode in range(episodes):
            state = self.env.reset()
            path = [self.env.current_pos]
            total_reward = 0
            
            while True:
                action = self.agent.choose_action(state, training=False)
                next_state, reward, done, info = self.env.step(action)
                
                path.append(self.env.current_pos)
                total_reward += reward
                state = next_state
                
                if done:
                    break
            
            test_rewards.append(total_reward)
            test_paths.append(path)
        
        return test_rewards, test_paths
    
    def plot_training_progress(self):
        """
        Genera gráficos del progreso de entrenamiento
        """
        try:
            # Clear any existing plots
            plt.clf()
            plt.close('all')
            
            # Verificar que tenemos datos
            if len(self.agent.episode_rewards) == 0:
                print("WARNING: No training data available for plotting")
                return None
            
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
              # 1. Recompensas por episodio
            episodes = range(1, len(self.agent.episode_rewards) + 1)
            ax1.plot(episodes, self.agent.episode_rewards, alpha=0.7, color='blue', linewidth=1.5, label='Recompensas')
            
            # Promedio móvil
            if len(self.agent.episode_rewards) > 10:
                window = min(20, len(self.agent.episode_rewards) // 4)
                if window > 1:
                    moving_avg = np.convolve(self.agent.episode_rewards, 
                                           np.ones(window)/window, mode='valid')
                    ax1.plot(range(window, len(self.agent.episode_rewards) + 1), 
                            moving_avg, color='red', linewidth=2, label=f'Promedio móvil ({window})')
            
            # Marcar la mejor recompensa
            if self.agent.episode_rewards:
                best_episode = np.argmax(self.agent.episode_rewards) + 1
                best_reward = max(self.agent.episode_rewards)
                ax1.axhline(y=best_reward, color='green', linestyle='--', alpha=0.5, label=f'Mejor: {best_reward:.1f}')
                ax1.scatter([best_episode], [best_reward], color='green', s=100, zorder=5)
            
            ax1.set_title(f'Evolución de Recompensas ({len(self.agent.episode_rewards)} episodios)', 
                         fontsize=12, fontweight='bold')
            ax1.set_xlabel('Episodio')
            ax1.set_ylabel('Recompensa Total')
            ax1.legend(fontsize=9)
            ax1.grid(True, alpha=0.3)
              # 2. Pasos por episodio
            if len(self.agent.episode_steps) > 0:
                ax2.plot(episodes, self.agent.episode_steps, alpha=0.7, color='green', linewidth=1.5, label='Pasos')
                
                # Promedio móvil de pasos
                if len(self.agent.episode_steps) > 10:
                    window = min(20, len(self.agent.episode_steps) // 4)
                    if window > 1:
                        steps_avg = np.convolve(self.agent.episode_steps, 
                                              np.ones(window)/window, mode='valid')
                        ax2.plot(range(window, len(self.agent.episode_steps) + 1), 
                                steps_avg, color='darkgreen', linewidth=2, label=f'Promedio móvil ({window})')
                
                # Marcar el menor número de pasos (mejor eficiencia)
                min_steps = min(self.agent.episode_steps)
                min_episode = self.agent.episode_steps.index(min_steps) + 1
                ax2.axhline(y=min_steps, color='red', linestyle='--', alpha=0.5, label=f'Mejor: {min_steps} pasos')
                ax2.scatter([min_episode], [min_steps], color='red', s=100, zorder=5)
                
                ax2.set_title('Eficiencia del Agente (Pasos por Episodio)')
                ax2.set_xlabel('Episodio')
                ax2.set_ylabel('Número de Pasos')
                ax2.legend(fontsize=9)
                ax2.grid(True, alpha=0.3)
            
            # 3. Tasa de exploración
            if len(self.agent.exploration_rates) > 0:
                ax3.plot(episodes, self.agent.exploration_rates, color='orange')
                ax3.set_title('Decaimiento de la Tasa de Exploración')
                ax3.set_xlabel('Episodio')
                ax3.set_ylabel('Tasa de Exploración (ε)')
                ax3.grid(True, alpha=0.3)
            
            # 4. Heatmap de la política aprendida
            try:
                self.plot_policy_heatmap(ax4)
            except Exception as e:
                ax4.text(0.5, 0.5, 'Error generando\nmapa de política', 
                        ha='center', va='center', transform=ax4.transAxes)
                ax4.set_title('Política Aprendida')
            
            plt.tight_layout()
            
            # Guardar gráfico
            base_dir = os.path.dirname(__file__)
            filepath = os.path.join(base_dir, 'rl_training_progress.png')
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except Exception as e:
            print(f"ERROR: Failed to generate training plot: {e}")
            plt.close('all')
            return None
    
    def plot_policy_heatmap(self, ax):
        """
        Visualiza la política aprendida como un mapa de calor
        """
        policy_grid = np.zeros(self.env.grid_size)
        
        for row in range(self.env.grid_size[0]):
            for col in range(self.env.grid_size[1]):
                if (row, col) not in self.env.obstacles and (row, col) != self.env.goal_pos:
                    state = row * self.env.grid_size[1] + col
                    best_action = np.argmax(self.agent.q_table[state])
                    policy_grid[row, col] = best_action
                elif (row, col) in self.env.obstacles:
                    policy_grid[row, col] = -1
                else:  # goal
                    policy_grid[row, col] = 4
        
        # Crear mapa de calor
        sns.heatmap(policy_grid, annot=True, fmt='.0f', cmap='viridis', 
                   ax=ax, cbar_kws={'label': 'Acción'})
        ax.set_title('Política Aprendida\n(0=↑, 1=→, 2=↓, 3=←, 4=Meta, -1=Obstáculo)')
        ax.set_xlabel('Columna')
        ax.set_ylabel('Fila')
    
    def plot_episode_simulation(self, path):
        """
        Visualiza la trayectoria del agente en un episodio
        """
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        
        # Crear grid base
        grid = np.zeros(self.env.grid_size)
        
        # Marcar obstáculos
        for obs in self.env.obstacles:
            grid[obs] = -1
        
        # Marcar meta
        grid[self.env.goal_pos] = 2
        
        # Crear mapa de calor
        sns.heatmap(grid, annot=True, fmt='.0f', cmap='RdYlBu_r', 
                   ax=ax, cbar=False, square=True)
        
        # Dibujar trayectoria
        path_x = [pos[1] + 0.5 for pos in path]
        path_y = [pos[0] + 0.5 for pos in path]
        
        ax.plot(path_x, path_y, 'wo-', linewidth=3, markersize=8, 
               markerfacecolor='yellow', markeredgecolor='black', 
               alpha=0.8, label='Trayectoria')
        
        # Marcar inicio y fin
        ax.plot(path_x[0], path_y[0], 'go', markersize=12, label='Inicio')
        ax.plot(path_x[-1], path_y[-1], 'ro', markersize=12, label='Fin')
        
        ax.set_title(f'Simulación del Agente - {len(path)} pasos')
        ax.set_xlabel('Columna')
        ax.set_ylabel('Fila')
        ax.legend()
        
        # Guardar gráfico
        base_dir = os.path.dirname(__file__)
        filepath = os.path.join(base_dir, 'rl_simulation.png')
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
        
        return filepath

# Instancia global del entorno y agente
env = GridWorldEnvironment()
agent = QLearningAgent(
    state_space=env.grid_size[0] * env.grid_size[1],
    action_space=env.action_space,
    learning_rate=0.1,
    discount_factor=0.95,
    exploration_rate=1.0,
    exploration_decay=0.995,
    min_exploration_rate=0.01
)
trainer = RLTrainer(env, agent)

# Funciones para la interfaz web
def get_training_status():
    """Obtiene el estado actual del entrenamiento"""
    # Verificar si existe un modelo guardado
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, 'rl_model.pkl')
    model_exists = os.path.exists(model_path)
    
    if len(agent.episode_rewards) == 0:
        return {
            'model_exists': model_exists,
            'trained': False,
            'episodes': 0,
            'avg_reward': 0,
            'exploration_rate': agent.exploration_rate,
            'last_reward': 0
        }
    
    return {
        'model_exists': model_exists,
        'trained': True,
        'episodes': len(agent.episode_rewards),
        'avg_reward': np.mean(agent.episode_rewards[-100:]) if len(agent.episode_rewards) >= 100 else np.mean(agent.episode_rewards),
        'exploration_rate': agent.exploration_rate,
        'last_reward': agent.episode_rewards[-1]
    }

def train_agent(episodes=500, learning_rate=None, discount_factor=None, exploration_rate=None, exploration_decay=None, reset=False):
    """Entrena el agente con parámetros configurables y retorna el estado actualizado"""
    global agent, trainer
    
    previous_episodes = len(agent.episode_rewards) if agent.episode_rewards else 0
    
    # Si se solicita reset o es el primer entrenamiento con parámetros muy diferentes
    if reset or (previous_episodes == 0):
        print(f"DEBUG: {'Resetting' if reset else 'Starting new'} training session")
    else:
        print(f"DEBUG: Continuing training from {previous_episodes} episodes")
    
    # Actualizar parámetros si se proporcionan
    if learning_rate is not None:
        agent.learning_rate = learning_rate
    if discount_factor is not None:
        agent.discount_factor = discount_factor
    if exploration_rate is not None:
        agent.exploration_rate = exploration_rate  
    if exploration_decay is not None:
        agent.exploration_decay = exploration_decay
    
    # Entrenar el agente
    trainer.train(episodes=episodes, verbose=True)
    
    # Guardar modelo
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, 'rl_model.pkl')
    agent.save_model(model_path)
    
    # Retornar información detallada del entrenamiento
    status = get_training_status()
    new_episodes = len(agent.episode_rewards) - previous_episodes
    recent_rewards = agent.episode_rewards[previous_episodes:] if previous_episodes > 0 else agent.episode_rewards
    
    status.update({
        'episodes_trained': new_episodes,
        'total_episodes': len(agent.episode_rewards),
        'previous_episodes': previous_episodes,
        'final_exploration_rate': agent.exploration_rate,
        'avg_reward_this_session': np.mean(recent_rewards) if recent_rewards else 0,
        'avg_reward_last_10': np.mean(agent.episode_rewards[-10:]) if len(agent.episode_rewards) >= 10 else np.mean(agent.episode_rewards),
        'best_reward': max(agent.episode_rewards) if agent.episode_rewards else 0,
        'worst_reward': min(agent.episode_rewards) if agent.episode_rewards else 0,
        'success_rate': sum(1 for r in agent.episode_rewards[-50:] if r > 50) / min(50, len(agent.episode_rewards)) if agent.episode_rewards else 0,
        'is_continued_training': previous_episodes > 0
    })
    
    return status

def get_training_plots():
    """Genera gráficos dinámicos de entrenamiento en base64"""
    try:
        if len(agent.episode_rewards) == 0:
            print("DEBUG: No episode rewards available")
            return None
        
        print(f"DEBUG: Generating plot for {len(agent.episode_rewards)} episodes")
        
        # Generar gráfico dinámico actualizado
        plot_path = trainer.plot_training_progress()
        print(f"DEBUG: Plot saved to {plot_path}")
        
        if plot_path and os.path.exists(plot_path):
            with open(plot_path, 'rb') as f:
                plot_data = base64.b64encode(f.read()).decode('utf-8')
            print(f"DEBUG: Plot data length: {len(plot_data)}")
            return plot_data
        else:
            print(f"DEBUG: Plot file not found at {plot_path}")
            return None
    
    except Exception as e:
        print(f"DEBUG: Error generating plot: {e}")
        return None

def get_training_metrics():
    """Retorna métricas actuales para actualización en tiempo real"""
    if len(agent.episode_rewards) == 0:
        return None
    
    recent_rewards = agent.episode_rewards[-10:] if len(agent.episode_rewards) >= 10 else agent.episode_rewards
    recent_steps = agent.episode_steps[-10:] if len(agent.episode_steps) >= 10 else agent.episode_steps
    
    return {
        'current_episode': len(agent.episode_rewards),
        'current_reward': agent.episode_rewards[-1],
        'avg_reward_recent': np.mean(recent_rewards),
        'avg_steps_recent': np.mean(recent_steps),
        'exploration_rate': agent.exploration_rate,
        'best_reward': max(agent.episode_rewards),
        'success_rate': sum(1 for r in recent_rewards if r > 50) / len(recent_rewards)
    }

def simulate_episode():
    """Simula un episodio con el agente entrenado"""
    test_rewards, test_paths = trainer.test_agent(episodes=1)
    
    if test_paths:
        simulation_path = trainer.plot_episode_simulation(test_paths[0])
        
        with open(simulation_path, 'rb') as f:
            simulation_data = base64.b64encode(f.read()).decode('utf-8')
        
        return {
            'reward': test_rewards[0],
            'steps': len(test_paths[0]) - 1,
            'path': test_paths[0],
            'simulation_plot': simulation_data
        }
    
    return None

def reset_agent():
    """Reinicia el agente y el entrenamiento completamente"""
    global agent, trainer
    print("DEBUG: Resetting agent and trainer")
    agent = QLearningAgent(
        state_space=env.grid_size[0] * env.grid_size[1],
        action_space=env.action_space
    )
    trainer = RLTrainer(env, agent)
    
    # Limpiar archivos de gráficos anteriores
    try:
        base_dir = os.path.dirname(__file__)
        training_plot = os.path.join(base_dir, 'rl_training_progress.png')
        simulation_plot = os.path.join(base_dir, 'rl_simulation.png')
        
        if os.path.exists(training_plot):
            os.remove(training_plot)
        if os.path.exists(simulation_plot):
            os.remove(simulation_plot)
    except Exception as e:
        print(f"DEBUG: Error cleaning plots: {e}")
    
    return get_training_status()

def continue_training(episodes=100, learning_rate=None, discount_factor=None, 
                     exploration_rate=None, exploration_decay=None):
    """Continúa el entrenamiento del agente actual con nuevos parámetros"""
    global agent, trainer
    
    # Actualizar parámetros si se proporcionan
    if learning_rate is not None:
        agent.learning_rate = learning_rate
    if discount_factor is not None:
        agent.discount_factor = discount_factor
    if exploration_rate is not None:
        agent.exploration_rate = exploration_rate
    if exploration_decay is not None:
        agent.exploration_decay = exploration_decay
    
    print(f"DEBUG: Continuing training for {episodes} more episodes")
    print(f"DEBUG: Current total episodes: {len(agent.episode_rewards)}")
    
    # Continuar entrenamiento
    trainer.train(episodes=episodes, verbose=True)
    
    return {
        'episodes': episodes,
        'total_episodes': len(agent.episode_rewards),
        'avg_reward': np.mean(agent.episode_rewards[-episodes:]) if agent.episode_rewards else 0,
        'final_exploration': agent.exploration_rate,
        'success': True
    }

# Información para la página de conceptos
rl_concepts_info = {
    'definition': """
    El Aprendizaje por Refuerzo (Reinforcement Learning, RL) es un paradigma de aprendizaje automático 
    donde un agente aprende a tomar decisiones secuenciales en un entorno dinámico a través de la 
    interacción directa, recibiendo retroalimentación en forma de recompensas o castigos por sus acciones.
    """,
    
    'differences': {
        'supervisado': 'Requiere datos etiquetados, aprendizaje de mapeo entrada-salida',
        'no_supervisado': 'Encuentra patrones ocultos en datos sin etiquetas',
        'refuerzo': 'Aprende a través de interacción con el entorno y retroalimentación de recompensas'
    },
    
    'components': {
        'agente': 'Entidad que toma decisiones y ejecuta acciones',
        'entorno': 'Mundo en el que opera el agente',
        'estados': 'Situaciones o configuraciones posibles del entorno',
        'acciones': 'Decisiones que puede tomar el agente',
        'recompensas': 'Señales numéricas que indican qué tan buena fue una acción',
        'politica': 'Estrategia del agente para mapear estados a acciones'
    },
    
    'algorithms': {
        'q_learning': 'Algoritmo libre de modelo que aprende valores Q(s,a) óptimos',
        'sarsa': 'Algoritmo on-policy que actualiza basado en la política actual',
        'dqn': 'Deep Q-Network: combina Q-Learning con redes neuronales profundas'
    }
}

if __name__ == '__main__':
    # Ejemplo de uso
    print("Entrenando agente Q-Learning en GridWorld...")
    trainer.train(episodes=500)
    
    print("\nProbando agente entrenado...")
    test_rewards, test_paths = trainer.test_agent(episodes=5)
    print(f"Recompensa promedio en pruebas: {np.mean(test_rewards):.2f}")
    
    # Generar visualizaciones
    trainer.plot_training_progress()
    if test_paths:
        trainer.plot_episode_simulation(test_paths[0])
    
    print("Entrenamiento completado!")
