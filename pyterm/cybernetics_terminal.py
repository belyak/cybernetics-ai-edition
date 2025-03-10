#!/usr/bin/env python3
"""
Cybernetics Book Terminal Application

A self-contained, standalone terminal application to explore
"Cybernetics: Fundamentals and Applications" book content.

This version uses the curses library for terminal manipulation
and does not require a Jupyter notebook environment.

Usage:
    python cybernetics_terminal.py

Controls:
    - Enter numbers or letters for menu selection
    - UP/DOWN arrow keys for scrolling content
    - ESC or Q to exit
"""

import curses
import time
import yaml
import textwrap
import random
import re
from curses import wrapper

# Define our YAML data structure based on the book content
CYBERNETICS_BOOK_YAML = """
title:
  en: "Cybernetics: Fundamentals and Applications"
  ru: "Кибернетика: Основы и применение"
  fr: "Cybernétique: Fondements et Applications"

subtitle:
  en: "Interactive Table of Contents"
  ru: "Интерактивное оглавление"
  fr: "Table des matières interactive"

creator:
  en: "Created by AI-Delirium TG Team"
  ru: "Создано командой AI-Delirium TG"
  fr: "Créé par l'équipe AI-Delirium TG"

copyright:
  en: "© 2025 AI-Delirium TG Team. All rights reserved."
  ru: "© 2025 Команда AI-Delirium TG. Все права защищены."
  fr: "© 2025 Équipe AI-Delirium TG. Tous droits réservés."

chapters:
  - number: 1
    title:
      en: "Introduction to Cybernetics"
      ru: "Введение в кибернетику"
    sections:
      - number: "1.1"
        title:
          en: "History of Cybernetics Development"
          ru: "История развития кибернетики"
      - number: "1.2"
        title:
          en: "Norbert Wiener and the Establishment of Science"
          ru: "Норберт Винер и становление науки"
      - number: "1.3"
        title:
          en: "Basic Concepts and Terminology"
          ru: "Основные концепции и терминология"
      - number: "1.4"
        title:
          en: "Cybernetics in the Modern World"
          ru: "Кибернетика в современном мире"

  - number: 2
    title:
      en: "Systems and Control Theory"
      ru: "Теория систем и управления"
    sections:
      - number: "2.1"
        title:
          en: "Basic Concepts of Systems Theory"
          ru: "Основные понятия теории систем"
      - number: "2.2"
        title:
          en: "Principles of Feedback"
          ru: "Принципы обратной связи"
      - number: "2.3"
        title:
          en: "System Stability"
          ru: "Устойчивость систем"
      - number: "2.4"
        title:
          en: "Adaptive Control"
          ru: "Адаптивное управление"

  - number: 3
    title:
      en: "Information and Communication"
      ru: "Информация и коммуникация"
    sections:
      - number: "3.1"
        title:
          en: "Information Theory"
          ru: "Теория информации"
      - number: "3.2"
        title:
          en: "Entropy and Information Entropy"
          ru: "Энтропия и информационная энтропия"
      - number: "3.3"
        title:
          en: "Information Coding"
          ru: "Кодирование информации"
      - number: "3.4"
        title:
          en: "Communication Channels and Noise Immunity"
          ru: "Каналы связи и помехоустойчивость"

  - number: 4
    title:
      en: "Mathematical Apparatus of Cybernetics"
      ru: "Математический аппарат кибернетики"
    sections:
      - number: "4.1"
        title:
          en: "Algorithm Theory"
          ru: "Теория алгоритмов"
      - number: "4.2"
        title:
          en: "Discrete Mathematics"
          ru: "Дискретная математика"
      - number: "4.3"
        title:
          en: "Automata Theory"
          ru: "Теория автоматов"
      - number: "4.4"
        title:
          en: "Optimization Methods"
          ru: "Методы оптимизации"

  - number: 5
    title:
      en: "Technical Systems in Cybernetics"
      ru: "Технические системы в кибернетике"
    sections:
      - number: "5.1"
        title:
          en: "Automated Control Systems"
          ru: "Автоматизированные системы управления"
      - number: "5.2"
        title:
          en: "Robotics"
          ru: "Робототехника"
      - number: "5.3"
        title:
          en: "Mechatronics"
          ru: "Мехатроника"
      - number: "5.4"
        title:
          en: "Measurement Systems and Sensors"
          ru: "Измерительные системы и датчики"

  - number: 6
    title:
      en: "Biological Cybernetics"
      ru: "Биологическая кибернетика"
    sections:
      - number: "6.1"
        title:
          en: "Biological Control Systems"
          ru: "Биологические системы управления"
      - number: "6.2"
        title:
          en: "Neurocybernetics"
          ru: "Нейрокибернетика"
      - number: "6.3"
        title:
          en: "Modeling Biological Processes"
          ru: "Моделирование биологических процессов"
      - number: "6.4"
        title:
          en: "Artificial Neural Networks"
          ru: "Искусственные нейронные сети"

  - number: 7
    title:
      en: "Economic Cybernetics"
      ru: "Экономическая кибернетика"
    sections:
      - number: "7.1"
        title:
          en: "Modeling Economic Processes"
          ru: "Моделирование экономических процессов"
      - number: "7.2"
        title:
          en: "Optimal Resource Management"
          ru: "Оптимальное управление ресурсами"
      - number: "7.3"
        title:
          en: "Decision Support Systems"
          ru: "Системы поддержки принятия решений"
      - number: "7.4"
        title:
          en: "Forecasting Economic Indicators"
          ru: "Прогнозирование экономических показателей"

  - number: 8
    title:
      en: "Social Cybernetics"
      ru: "Социальная кибернетика"
    sections:
      - number: "8.1"
        title:
          en: "Society as a Cybernetic System"
          ru: "Общество как кибернетическая система"
      - number: "8.2"
        title:
          en: "Information Society"
          ru: "Информационное общество"
      - number: "8.3"
        title:
          en: "Modeling Social Processes"
          ru: "Моделирование социальных процессов"
      - number: "8.4"
        title:
          en: "Management of Social Systems"
          ru: "Управление социальными системами"

  - number: 9
    title:
      en: "Artificial Intelligence"
      ru: "Искусственный интеллект"
    sections:
      - number: "9.1"
        title:
          en: "Basic Concepts of Artificial Intelligence"
          ru: "Основные концепции искусственного интеллекта"
      - number: "9.2"
        title:
          en: "Expert Systems"
          ru: "Экспертные системы"
      - number: "9.3"
        title:
          en: "Machine Learning"
          ru: "Машинное обучение"
      - number: "9.4"
        title:
          en: "Computer Vision and Pattern Recognition"
          ru: "Компьютерное зрение и распознавание образов"

  - number: 10
    title:
      en: "Cybersecurity"
      ru: "Кибербезопасность"
    sections:
      - number: "10.1"
        title:
          en: "Information Security Threats"
          ru: "Угрозы информационной безопасности"
      - number: "10.2"
        title:
          en: "Information Protection Methods"
          ru: "Методы защиты информации"
      - number: "10.3"
        title:
          en: "Cryptography"
          ru: "Криптография"
      - number: "10.4"
        title:
          en: "Ethical Aspects of Cybersecurity"
          ru: "Этические аспекты кибербезопасности"

  - number: 11
    title:
      en: "Prospects for Cybernetics Development"
      ru: "Перспективы развития кибернетики"
    sections:
      - number: "11.1"
        title:
          en: "Quantum Cybernetics"
          ru: "Квантовая кибернетика"
      - number: "11.2"
        title:
          en: "Nanocybernetics"
          ru: "Нанокибернетика"
      - number: "11.3"
        title:
          en: "Integration with Other Sciences"
          ru: "Интеграция с другими науками"
      - number: "11.4"
        title:
          en: "Cybernetics of the Future"
          ru: "Кибернетика будущего"

appendices:
  - id: "A"
    title:
      en: "Glossary of Terms"
      ru: "Глоссарий терминов"
  - id: "B"
    title:
      en: "Bibliography"
      ru: "Библиография"
  - id: "C"
    title:
      en: "Index"
      ru: "Указатель"
"""

# Define sample content for sections
SAMPLE_SECTION_CONTENT = {
    "1.1": """
History of Cybernetics Development

The term "cybernetics" comes from the Greek word "κυβερνητική" (kybernētikḗ), meaning "governance" or "steering".

Key historical developments:

1. Early concepts (1940s)
   - Norbert Wiener's work during WWII on anti-aircraft systems
   - Development of feedback mechanisms in engineering

2. Foundation period (1948)
   - Publication of "Cybernetics: Or Control and Communication in the Animal and the Machine"
   - Establishment of core principles of control and communication

3. First wave cybernetics (1950s-1960s)
   - Focus on homeostasis and self-regulating systems
   - Application to various fields including engineering and biology

4. Second wave cybernetics (1970s-1980s)
   - Introduction of self-organization and autopoiesis concepts
   - Emphasis on observer involvement in systems

5. Modern period (1990s-present)
   - Integration with computational systems and AI
   - Application to complex social and economic systems
   - Development of cyber-physical systems
""",

    "1.2": """
Norbert Wiener and the Establishment of Science

Norbert Wiener (1894-1964) is considered the father of cybernetics.

Key contributions:

1. Mathematical foundation
   - Applied mathematical analysis to control problems
   - Developed statistical techniques for signal processing

2. Interdisciplinary approach
   - Connected engineering with biology and social sciences
   - Established the Macy Conferences (1946-1953)

3. Philosophical insights
   - Emphasized ethical implications of automation
   - Published "The Human Use of Human Beings" (1950)

4. Technical innovations
   - Theory of prediction and filtering
   - Stochastic processes in communication

Wiener's legacy continues through the application of cybernetic principles across multiple disciplines, from robotics to organizational theory.
""",

    "2.1": """
Basic Concepts of Systems Theory

Systems theory provides the foundation for cybernetics, focusing on the abstract organization of phenomena.

Key concepts:

1. System definition
   - A set of interrelated components forming a unified whole
   - Characterized by boundaries, inputs, outputs, and internal states

2. System hierarchy
   - Systems can contain subsystems
   - Multiple levels of organization

3. System properties
   - Emergence: properties that exist at system level but not at component level
   - Synergy: combined effect greater than sum of individual effects

4. System classification
   - Open vs. closed systems
   - Natural vs. artificial systems
   - Simple vs. complex systems

5. System behavior
   - State space and trajectories
   - Equilibrium and stability
   - Adaptation and evolution

These concepts provide the framework for analyzing cybernetic systems across different domains.
""",

    "2.2": """
Principles of Feedback

Feedback is a foundational concept in cybernetics, enabling system control and adaptation.

Types of feedback:

1. Negative feedback
   - Error-reducing mechanism
   - Stabilizes system toward equilibrium
   - Examples: thermostats, cruise control, homeostasis

2. Positive feedback
   - Amplifies deviations from equilibrium
   - Can lead to exponential growth or collapse
   - Examples: population growth, financial bubbles

3. Feedforward
   - Anticipatory control based on predicted disturbances
   - Complements feedback by reducing response delay

Feedback loop components:
   - Sensor: measures system output
   - Controller: processes information and determines response
   - Actuator: implements control action
   - Process: the system being controlled

Mathematical representation:
   - Transfer functions
   - Differential equations
   - State-space models

Applications span engineering control systems, biological processes, social dynamics, and economic systems.
""",

    "3.1": """
Information Theory

Information theory, developed by Claude Shannon in 1948, provides mathematical foundations for quantifying and processing information.

Core concepts:

1. Information measure
   - Quantified in bits (binary digits)
   - Information as reduction of uncertainty
   - Surprisal: rare events carry more information

2. Entropy
   - Measure of uncertainty or randomness
   - H(X) = -∑p(x)log₂p(x)
   - Maximum entropy occurs with uniform probability distribution

3. Channel capacity
   - Maximum rate of reliable information transmission
   - C = max I(X;Y) [mutual information between input X and output Y]
   - Fundamental limits on communication

4. Source coding
   - Data compression techniques
   - Huffman coding, arithmetic coding
   - Shannon's source coding theorem

5. Channel coding
   - Error detection and correction
   - Redundancy to overcome noise
   - Shannon's noisy channel coding theorem

Information theory connects directly to cybernetics through its focus on communication, which is essential for control in any system.
""",

    "3.2": """
Entropy and Information Entropy

Entropy concepts bridge thermodynamics, information theory, and cybernetics.

Information entropy:
   - Measures uncertainty in a random variable
   - H(X) = -∑p(x)log₂p(x)
   - Higher entropy means more uncertainty and more potential information

Thermodynamic entropy:
   - Measure of molecular disorder in physical systems
   - S = k·ln(W) [Boltzmann's entropy formula]
   - Tends to increase in isolated systems (Second Law of Thermodynamics)

Connections:
   - Information entropy reduction requires energy expenditure
   - Maxwell's demon thought experiment
   - Landauer's principle: minimum energy to erase one bit of information

Applications in cybernetics:
   - Information entropy in signal processing
   - Maximum entropy methods in pattern recognition
   - Entropy as a measure of system complexity
   - Entropy production in self-organizing systems

Entropy is central to understanding limitations and efficiencies in information processing and control systems.
""",

    "6.4": """
Artificial Neural Networks

Artificial Neural Networks (ANNs) apply biological neural system principles to create computational models for machine learning.

Fundamental concepts:

1. Structure
   - Neurons (processing units)
   - Connections (weights)
   - Layers (input, hidden, output)

2. Activation functions
   - Sigmoid
   - ReLU (Rectified Linear Unit)
   - Tanh (Hyperbolic tangent)

3. Network architectures
   - Feedforward networks
   - Convolutional Neural Networks (CNNs)
   - Recurrent Neural Networks (RNNs)
   - Self-Organizing Maps (SOMs)

4. Learning algorithms
   - Backpropagation
   - Gradient descent optimization
   - Hebbian learning

5. Cybernetic principles in ANNs
   - Feedback mechanisms in recurrent networks
   - Self-organization in unsupervised learning
   - Adaptivity through weight adjustments
   - Distributed control and processing

Neural networks represent a direct application of neurocybernetic principles, implementing biological information processing mechanisms in artificial systems.
""",

    "9.3": """
Machine Learning

Machine Learning (ML) exemplifies cybernetic principles through self-adjusting algorithms that improve with experience.

Learning paradigms:

1. Supervised learning
   - Learning from labeled examples
   - Classification and regression problems
   - Algorithms: decision trees, support vector machines, neural networks

2. Unsupervised learning
   - Finding patterns in unlabeled data
   - Clustering, dimensionality reduction, anomaly detection
   - Algorithms: k-means, hierarchical clustering, principal component analysis

3. Reinforcement learning
   - Learning through reward/penalty feedback
   - Agent-environment interaction
   - Applications: game playing, robotics, control systems

4. Cybernetic aspects of ML
   - Feedback loops in training processes
   - Adaptive behavior through parameter adjustment
   - Error-correction mechanisms
   - Self-improvement over time

5. Current challenges
   - Bias and fairness in algorithms
   - Explainability of complex models
   - Transfer learning across domains
   - Energy efficiency in large models

Machine learning systems embody the cybernetic ideal of systems that regulate themselves based on feedback and adapt to changing environments.
""",

    "11.4": """
Cybernetics of the Future

Emerging trends point to an expanded role for cybernetics in addressing complex global challenges.

Future directions:

1. Integrated cyber-physical-biological systems
   - Seamless interfaces between digital, physical, and biological domains
   - Biomimetic systems that adopt principles from nature
   - Human augmentation technologies

2. Collaborative intelligence
   - Human-AI partnership frameworks
   - Distributed collective intelligence
   - Swarm systems with emergent capabilities

3. Cybernetics for sustainability
   - Ecological system management using cybernetic principles
   - Closed-loop resource management
   - Climate modeling and intervention strategies

4. Ethical cybernetics
   - Value-aligned control systems
   - Responsible autonomy
   - Privacy-preserving information systems

5. Quantum cybernetics
   - Control systems utilizing quantum properties
   - Quantum information theory applications
   - Quantum machine learning

The future of cybernetics likely involves deeper integration with other disciplines and increased responsibility for managing complex socio-technical systems at global scale.
"""
}

# ASCII art for the header
HEADER_ASCII = """
  _____      _                          _   _          
 / ____|    | |                        | | (_)         
| |    _   _| |__   ___ _ __ _ __   ___| |_ _  ___ ___ 
| |   | | | | '_ \\ / _ \\ '__| '_ \\ / _ \\ __| |/ __/ __|
| |___| |_| | |_) |  __/ |  | | | |  __/ |_| | (__\\__ \\
 \\_____\\__, |_.__/ \\___|_|  |_| |_|\\___|\\__|_|\\___|___/
        __/ |                                          
       |___/                                           

=== FUNDAMENTALS AND APPLICATIONS ===
"""

LOADING_ASCII = """
╔══════════════════════════════════════╗
║ INITIALIZING CYBERNETIC SYSTEMS...   ║
╚══════════════════════════════════════╝

[█▒▒▒▒▒▒▒▒▒▒] 10%  Loading core modules
[███▒▒▒▒▒▒▒▒] 30%  Scanning knowledge base
[█████▒▒▒▒▒▒] 50%  Calibrating feedback loops
[███████▒▒▒▒] 70%  Establishing control systems
[█████████▒▒] 90%  Finalizing neural connections
[███████████] 100% System ready
"""


def main(stdscr):
    """Main function that initializes and runs the curses application."""
    app = CursesTui(stdscr)
    app.run()


class CursesTui:
    """Terminal User Interface for Cybernetics Book using curses."""

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.max_y, self.max_x = stdscr.getmaxyx()

        # Set up colors
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Standard terminal green
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Headers
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Prompts
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)  # Errors
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)  # User input
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Special content

        # Hide cursor
        curses.curs_set(0)

        # Enable keypad input
        self.stdscr.keypad(True)

        # Book data
        self.book_data = yaml.safe_load(CYBERNETICS_BOOK_YAML)

        # State
        self.language = "en"
        self.current_state = "main"
        self.current_chapter = None
        self.current_section = None
        self.current_position = 0  # For scrolling

    def clear_screen(self):
        """Clear the screen."""
        self.stdscr.clear()
        self.current_position = 0

    def add_loading_animation(self):
        """Show a loading animation."""
        self.clear_screen()
        lines = LOADING_ASCII.strip().split('\n')

        start_y = max(0, (self.max_y - len(lines)) // 2)
        start_x = max(0, (self.max_x - max(len(line) for line in lines)) // 2)

        for i, line in enumerate(lines):
            y = start_y + i
            if 0 <= y < self.max_y:
                self.stdscr.addstr(y, start_x, line, curses.color_pair(1))
                self.stdscr.refresh()
                time.sleep(0.1)  # Slower for dramatic effect

    def add_header(self):
        """Add the ASCII art header."""
        lines = HEADER_ASCII.strip().split('\n')

        for i, line in enumerate(lines):
            if i < self.max_y:
                center_x = max(0, (self.max_x - len(line)) // 2)
                self.stdscr.addstr(i, center_x, line, curses.color_pair(2))

    def wrap_text(self, text, width=None):
        """Wrap text to fit on screen."""
        if width is None:
            width = self.max_x - 4  # Allow for some margin

        wrapped_lines = []
        for line in text.split('\n'):
            if not line.strip():
                wrapped_lines.append('')
            else:
                wrapped_lines.extend(textwrap.wrap(line, width=width) or [''])

        return wrapped_lines

    def display_content(self, content, start_y=10, color=1):
        """Display wrapped text content starting at a specific Y position."""
        wrapped_lines = self.wrap_text(content)

        # Adjust for scrolling
        display_lines = wrapped_lines[self.current_position:self.current_position + (self.max_y - start_y - 2)]

        for i, line in enumerate(display_lines):
            if start_y + i < self.max_y:
                self.stdscr.addstr(start_y + i, 2, line, curses.color_pair(color))

        # Add scrolling indicators if needed
        if self.current_position > 0:
            self.stdscr.addstr(start_y - 1, 2, "↑ (Use UP arrow to scroll up)", curses.color_pair(3))

        if self.current_position + (self.max_y - start_y - 2) < len(wrapped_lines):
            self.stdscr.addstr(self.max_y - 2, 2, "↓ (Use DOWN arrow to scroll down)", curses.color_pair(3))

        return start_y + len(display_lines)

    def display_prompt(self, prompt, y_position):
        """Display a command prompt at the given Y position."""
        if y_position < self.max_y - 1:
            self.stdscr.addstr(y_position, 2, prompt, curses.color_pair(3))
            self.stdscr.refresh()

    def get_user_input(self, y_position):
        """Get user input at the given Y position."""
        curses.echo()
        curses.curs_set(1)  # Show cursor

        input_str = ""
        input_x = 2 + 20  # Position after prompt

        if y_position < self.max_y - 1:
            self.stdscr.addstr(y_position, 2, "Enter your choice: ", curses.color_pair(3))
            self.stdscr.refresh()

            # Create a input window just for this input
            input_win = curses.newwin(1, self.max_x - input_x - 2, y_position, input_x)
            input_win.keypad(True)

            # Get the input
            curses.curs_set(1)
            input_str = input_win.getstr(0, 0).decode('utf-8')
            curses.curs_set(0)

        curses.noecho()
        curses.curs_set(0)  # Hide cursor again

        return input_str

    def get_search_input(self, y_position):
        """Get search keyword input at the given Y position."""
        curses.echo()
        curses.curs_set(1)  # Show cursor

        input_str = ""
        input_x = 2 + 20  # Position after prompt

        if y_position < self.max_y - 1:
            self.stdscr.addstr(y_position, 2, "Enter search keyword: ", curses.color_pair(3))
            self.stdscr.refresh()

            # Create a input window just for this input
            input_win = curses.newwin(1, self.max_x - input_x - 2, y_position, input_x)
            input_win.keypad(True)

            # Get the input
            curses.curs_set(1)
            input_str = input_win.getstr(0, 0).decode('utf-8')
            curses.curs_set(0)

        curses.noecho()
        curses.curs_set(0)  # Hide cursor again

        return input_str

    def handle_scroll(self, key):
        """Handle scrolling up and down."""
        if key == curses.KEY_UP and self.current_position > 0:
            self.current_position -= 1
            return True
        elif key == curses.KEY_DOWN:
            self.current_position += 1
            return True
        return False

    def search_book(self, keyword):
        """Search the book for a keyword."""
        results = []
        keyword = keyword.lower()

        # Search chapter titles
        for chapter in self.book_data["chapters"]:
            title = chapter["title"].get(self.language, chapter["title"]["en"]).lower()
            if keyword in title:
                ch_num = chapter["number"]
                ch_title = chapter["title"].get(self.language, chapter["title"]["en"])
                results.append(f"Chapter {ch_num}: {ch_title}")

        # Search section titles
        for chapter in self.book_data["chapters"]:
            for section in chapter["sections"]:
                title = section["title"].get(self.language, section["title"]["en"]).lower()
                if keyword in title:
                    ch_num = chapter["number"]
                    sec_num = section["number"]
                    sec_title = section["title"].get(self.language, section["title"]["en"])
                    results.append(f"Section {sec_num}: {sec_title} (Chapter {ch_num})")

        # Search appendix titles
        for appendix in self.book_data["appendices"]:
            title = appendix["title"].get(self.language, appendix["title"]["en"]).lower()
            if keyword in title:
                app_id = appendix["id"]
                app_title = appendix["title"].get(self.language, appendix["title"]["en"])
                results.append(f"Appendix {app_id}: {app_title}")

        # Format search results
        if results:
            search_output = ["==== SEARCH RESULTS ====", f"Keyword: '{keyword}'", ""]
            search_output.extend(results)
        else:
            search_output = ["==== SEARCH RESULTS ====", f"No results found for '{keyword}'"]

        search_output.extend(["", "B. Back to Main Menu", "", "Type B and press ENTER to return:"])

        return "\n".join(search_output)

    def generate_main_menu(self):
        """Generate the main menu content."""
        menu = [
            "==== MAIN MENU ====",
            "",
            "1. Browse by Chapter",
            "2. Search by Keyword",
            "3. View Book Information",
            "4. Change Language",
            "5. Exit",
            "",
            "Type a number and press ENTER:"
        ]
        return "\n".join(menu)

    def generate_chapter_menu(self):
        """Generate the chapter menu content."""
        menu = ["==== CHAPTERS ====", ""]

        for chapter in self.book_data["chapters"]:
            title = chapter["title"].get(self.language, chapter["title"]["en"])
            menu.append(f"{chapter['number']}. {title}")

        menu.append("")
        menu.append("A. View Appendices")
        menu.append("B. Back to Main Menu")
        menu.append("")
        menu.append("Type a number/letter and press ENTER:")

        return "\n".join(menu)