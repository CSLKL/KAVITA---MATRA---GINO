import re
import streamlit as st

# Define matra values for different Hindi vowels and consonants
matra_dict = {
    'अ': 1, 'आ': 2, 'इ': 1, 'ई': 2, 'उ': 1, 'ऊ': 2, 'ऋ': 1,
    'ए': 2, 'ऐ': 2, 'ओ': 2, 'औ': 2, 'ं': 1, 'ः': 1, 'ँ': 1,
}

# Common word replacements to adjust matra count while keeping meaning
replacement_dict = {
    "सूरज": ["सूर्य"],  # 4 to 3 matras
    "धारा": ["सरिता"],  # 4 to 3 matras
    "चिड़ियों": ["पंछियों"],  # 5 to 4 matras
    "फूलों": ["सुमनों"],  # 4 to 3 matras
    "हवा": ["समीर"],  # 3 to 4 matras
}

# Define half consonants and conjunct consonants (halant cases)
halant_patterns = re.compile(r'([क-ह]्)')

def count_matras(line):
    """
    Function to count matras in a given Hindi line.
    """
    matra_count = 0
    
    # Handle Halant cases (½ consonant = 1 matra)
    halant_matches = halant_patterns.findall(line)
    matra_count += len(halant_matches)

    # Check each character in line
    for char in line:
        if char in matra_dict:
            matra_count += matra_dict[char]
        elif char in 'क-ह':  # Counting consonants that are not halant
            matra_count += 1

    return matra_count

def suggest_replacements(line, target_matras):
    """
    Suggest alternative words from the dictionary to adjust matra count.
    """
    words = line.split()
    suggestions = []

    for word in words:
        if word in replacement_dict:
            for replacement in replacement_dict[word]:
                new_line = line.replace(word, replacement)
                new_count = count_matras(new_line)
                if new_count == target_matras:
                    suggestions.append((word, replacement, new_count))

    return suggestions

# Streamlit Web App UI
st.title("📖 Hindi Poetry Matra Analyzer")
st.write("Paste your Hindi poem below to check its metrical correctness.")

# Text input for poetry
poem_text = st.text_area("Paste your poem here:", height=200)

if st.button("Analyze Matras"):
    if not poem_text.strip():
        st.warning("⚠ Please enter a poem for analysis.")
    else:
        lines = poem_text.split("\n")
        matra_counts = [count_matras(line) for line in lines if line.strip()]
        
        if not matra_counts:
            st.error("No valid lines found. Please enter a proper poem.")
        else:
            ideal_matras = max(set(matra_counts), key=matra_counts.count)  # Most common matra count

            st.subheader("🔍 Matra Analysis:")
            for line in lines:
                if line.strip():
                    matra_count = count_matras(line)
                    suggestion = suggest_replacements(line, ideal_matras) if matra_count != ideal_matras else "✅ Perfect Meter"
                    st.write(f"**Line:** {line}  
**Matras:** {matra_count}  
**Suggestion:** {suggestion}")

st.write("Created for poets who want to perfect their Hindi meter! ✨")
