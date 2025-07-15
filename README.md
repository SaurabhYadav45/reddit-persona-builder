# 🤖 Gen AI Internship Assignment – Reddit Persona Builder

## 📝 Project Description

This project generates AI-inferred **user personas** by analyzing Reddit user behavior. For a given Reddit username, the script retrieves public posts and comments and outputs:
- A concise **persona profile**,
- Detailed **inferences** on interests, personality, behavior, hobbies, and frustrations,
- Direct references to Post or Comment IDs used.

Each persona is saved as a `.txt` file.

---

📁 Files & Structure

reddit-persona-builder/
├── main.py                # Entry script
├── reddit_persona.py      # Persona builder logic
├── requirements.txt
├── README.md
└── samples/
    └── kojied.txt

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/SaurabhYadav45/reddit-persona-builder.git
cd reddit-persona-builder

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Add Reddit API Credentials

Create a .env file in the root directory:

REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_custom_user_agent

### 5. 🚀 How to Run
To generate a persona for any Reddit user, run:

python persona_builder.py <reddit_username>

#### Example:
python persona_builder.py kojied

This will create an output file at:
samples/kojied.txt


## Generated Sample output format

**Username:** kojied
**Account Age:** 5 years

- ## Interests
  - Enjoys nightlife and music (Post ID: 1lykkqf).
  - Engages in NBA referee debates (Post ID: 1hcopxo).
  - Concerned about H1B visa exploitation (Post IDs: 1hnx8j0, 1hnx7lj).

- ## Personality Traits
  - Reflective and empathetic.
  - Curious and open to multiple viewpoints.
  - Displays humor in gaming discussions.

- ## Location
  - Based in New York City (inferred from multiple posts).

- ## Hobbies
  - Plays strategy games like ManorLords.
  - Enjoys management/resource gameplay.

- ## Behavioral
  - Active across diverse subreddits.
  - Frequently introspective and self-aware.

- ## Frustrations or Beliefs
  - Dislikes lack of late-game content in strategy games.
  - Expresses concern over immigrant experiences.

*Generated using publicly available Reddit data. Cited Post/Comment IDs included.*


✅ Notes
-> Code follows PEP-8 guidelines.

-> Each .txt file contains a structured persona with categories like interests, personality traits, behaviors, and frustrations.

-> Only public Reddit data is used. No private or sensitive data is collected.


