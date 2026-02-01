import streamlit as st
import random

# Initialize session state variables
if 'target_number' not in st.session_state:
    st.session_state.target_number = random.randint(1, 50)
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'max_attempts' not in st.session_state:
    st.session_state.max_attempts = 5
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'message' not in st.session_state:
    st.session_state.message = ""
if 'guess_history' not in st.session_state:
    st.session_state.guess_history = []
if 'hint_used' not in st.session_state:
    st.session_state.hint_used = False
if 'score' not in st.session_state:
    st.session_state.score = 0

# Page configuration
st.set_page_config(
    page_title="Test Your Brains Game",
    page_icon="🎮",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #4a4a9c;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #665;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .game-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    .stats-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1.5rem;
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 10px;
    }
    .stat-box {
        text-align: center;
        flex: 1;
        padding: 0.5rem;
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #4a4a9c;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
    .message-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1.5rem 0;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .win-message {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .lose-message {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .hint-message {
        background-color: #cce5ff;
        color: #004085;
        border: 1px solid #b8daff;
    }
    .guess-history {
        margin-top: 1.5rem;
        padding: 1rem;
        background-color: #f0f0f0;
        border-radius: 10px;
    }
    .history-title {
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #555;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5rem 1rem;
    }
    .instructions {
        background-color: #e7f3ff;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 2rem;
        border-left: 5px solid #4a4a9c;
    }
</style>
""", unsafe_allow_html=True)

# Game title
st.markdown("<h1 class='main-title'>🎯 Test Your Brains Game</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Guess the number between 1 and 50. You have 5 attempts!</p>", unsafe_allow_html=True)

# Main game container
with st.container():
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    
    # Game stats
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">{st.session_state.attempts}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Attempts Used</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        remaining = st.session_state.max_attempts - st.session_state.attempts
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">{remaining}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Attempts Left</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">{st.session_state.score}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Score</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Game message
    if st.session_state.message:
        if "Congratulations" in st.session_state.message:
            css_class = "win-message"
        elif "Game Over" in st.session_state.message:
            css_class = "lose-message"
        else:
            css_class = "hint-message"
        
        st.markdown(f'<div class="message-box {css_class}">{st.session_state.message}</div>', unsafe_allow_html=True)
    
    # Game input and controls
    if not st.session_state.game_over:
        # Input for guess
        col1, col2 = st.columns([2, 1])
        with col1:
            guess = st.number_input(
                "Enter your guess (1-50):",
                min_value=1,
                max_value=50,
                value=25,
                step=1,
                key="guess_input"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            submit_guess = st.button("Submit Guess 🎯", use_container_width=True)
        
        # Hint button
        hint_col1, hint_col2 = st.columns([1, 1])
        with hint_col1:
            if st.button("Get a Hint 💡", use_container_width=True) and not st.session_state.hint_used:
                st.session_state.hint_used = True
                if st.session_state.target_number % 2 == 0:
                    st.session_state.message = f"Hint: The number is even."
                else:
                    st.session_state.message = f"Hint: The number is odd."
                st.rerun()
        
        with hint_col2:
            if st.button("Show Range Hint 📊", use_container_width=True):
                lower_bound = max(1, st.session_state.target_number - 10)
                upper_bound = min(50, st.session_state.target_number + 10)
                st.session_state.message = f"Hint: The number is between {lower_bound} and {upper_bound}."
                st.rerun()
        
        # Process guess when submitted
        if submit_guess:
            st.session_state.attempts += 1
            st.session_state.guess_history.append(guess)
            
            if guess == st.session_state.target_number:
                st.session_state.game_over = True
                # Calculate score: more attempts = lower score
                score_earned = max(1, 50 - (st.session_state.attempts * 10))
                st.session_state.score += score_earned
                st.session_state.message = f"🎉 <strong>Congratulations</strong>! You guessed the number {st.session_state.target_number} in {st.session_state.attempts} attempts👌! You earned {score_earned} points😊."
            elif guess < st.session_state.target_number:
                st.session_state.message = f"📈 Too low! Try a higher number."
            else:
                st.session_state.message = f"📉 Too high! Try a lower number."
            
            # Check if max attempts reached
            if st.session_state.attempts >= st.session_state.max_attempts and not st.session_state.game_over:
                st.session_state.game_over = True
                st.session_state.message = f"💀 Ouch Game Over! The number was {st.session_state.target_number}. Better luck next time😂!"
            
            st.rerun()
    else:
        # Game over, show play again button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎮 Play Again", use_container_width=True):
                # Reset game state
                st.session_state.target_number = random.randint(1, 50)
                st.session_state.attempts = 0
                st.session_state.game_over = False
                st.session_state.message = ""
                st.session_state.guess_history = []
                st.session_state.hint_used = False
                st.rerun()
    
    # Display guess history
    if st.session_state.guess_history:
        st.markdown('<div class="guess-history">', unsafe_allow_html=True)
        st.markdown('<div class="history-title">📜 Your Guesses:</div>', unsafe_allow_html=True)
        
        # Create a visual representation of guesses
        for i, g in enumerate(st.session_state.guess_history, 1):
            if g < st.session_state.target_number:
                arrow = "⬆️"
                hint = " (too low)"
            elif g > st.session_state.target_number:
                arrow = "⬇️"
                hint = " (too high)"
            else:
                arrow = "✅"
                hint = " (correct!)"
            
            st.markdown(f"Attempt {i}: **{g}** {arrow}{hint if not st.session_state.game_over else ''}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Instructions section
with st.expander("📖 How to Play & Tips", expanded=False):
    st.markdown("""
    <div class="instructions">
    <h4>Game Rules:</h4>
    <ol>
        <li>Think of a number between <strong>1 and 50</strong>.</li>
        <li>You have <strong>5 attempts</strong> to guess the correct number.</li>
        <li>After each guess, I'll tell you if your guess was too high or too low.</li>
        <li>You can use hints to help you, but try to solve it with as few hints as possible!</li>
    </ol>
    
    <h4>Scoring System:</h4>
    <ul>
        <li>You earn more points for guessing correctly in fewer attempts</li>
        <li>Maximum score per game: 100 points</li>
        <li>Each attempt reduces your potential score by 10 points</li>
        <li>Score carries over between games</li>
    </ul>
    
    <h4>Pro Tips:</h4>
    <ul>
        <li>Start with a guess in the middle (25) to split the range in half</li>
        <li>Use the "too high"/"too low" feedback to eliminate half the possibilities each time</li>
        <li>Save hints for when you're really stuck!</li>
        <li>Good luck, buddy!😎</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #665;'>God loves YOU!• Good luck! 🍀</div>", unsafe_allow_html=True)


