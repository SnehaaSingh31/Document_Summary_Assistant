import re
from collections import Counter

STOPWORDS = set("""
a an and the is are was were be been being do does did doing of for to in on
with without at by from up down into over under again further then once here
there when where why how all any both each few more most other some such no
nor not only own same so than too very can will just don don t should shouldn
now you your yours yourself yourselves he him his himself she her hers herself
it its itself they them their theirs themselves we us our ours ourselves i me
my mine myself this that these those as if because while during before after
above below off out over under between through during until against about
""".split())

SENT_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9])')

def sentence_tokenize(text: str):
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return []
    sentences = re.split(SENT_SPLIT, text)
    if len(sentences) == 1:
        sentences = re.split(r'(?<=\n)\s*', text)
    return [s.strip() for s in sentences if s.strip()]

def word_tokenize(sent: str):
    return re.findall(r"[A-Za-z0-9']+", sent.lower())

def build_frequency_table(sentences):
    counts = Counter()
    for s in sentences:
        for w in word_tokenize(s):
            if w not in STOPWORDS and len(w) > 2:
                counts[w] += 1
    if not counts:
        return counts
    max_freq = max(counts.values())
    for w in list(counts.keys()):
        counts[w] = counts[w] / max_freq
    return counts

def score_sentences(sentences, freq_table):
    scores = []
    for i, s in enumerate(sentences):
        words = word_tokenize(s)
        if not words:
            scores.append((i, 0.0))
            continue
        score = sum(freq_table.get(w, 0.0) for w in words) / (len(words) ** 0.7)
        lead_bonus = 1.0 if i < 3 else 0.0
        scores.append((i, score + 0.12 * lead_bonus))
    return scores

def pick_count(total_sentences, length='medium'):
    if length == 'short':
        return max(3, total_sentences // 12 or 3)
    if length == 'long':
        return max(8, total_sentences // 5 or 8)
    return max(5, total_sentences // 8 or 5)

def summarize_text(text: str, length='medium'):
    sentences = sentence_tokenize(text)
    if not sentences:
        return "", []

    freq_table = build_frequency_table(sentences)
    scores = score_sentences(sentences, freq_table)
    scores.sort(key=lambda x: x[1], reverse=True)

    k = pick_count(len(sentences), length=length)
    top_indices = sorted([i for i, _ in scores[:k]])

    summary_sentences = [sentences[i] for i in top_indices]
    summary = ' '.join(summary_sentences)

    top_k = 8 if length == 'long' else (6 if length == 'medium' else 5)
    keywords = [w for w, _ in Counter(freq_table).most_common(top_k)]
    return summary, keywords

def improvement_suggestions(text: str):
    """Very lightweight heuristics to suggest improvements for the original doc."""
    suggestions = []
    # length checks
    if len(text) < 500:
        suggestions.append("Document is quite short; add more context or supporting details.")
    if len(text) > 20000:
        suggestions.append("Document is very long; consider adding headings and an executive summary.")
    # headings presence
    if not re.search(r'\b(introduction|summary|conclusion|references|abstract)\b', text, re.IGNORECASE):
        suggestions.append("Add clear section headings (e.g., Introduction, Method, Conclusion) to improve structure.")
    # sentence length
    long_sentences = sum(1 for s in sentence_tokenize(text) if len(s.split()) > 35)
    if long_sentences > 0:
        suggestions.append(f"Contains {long_sentences} very long sentence(s); break them up for readability.")
    # bullet points
    if not re.search(r'^\s*[-*•]\s+', text, re.MULTILINE):
        suggestions.append("Where appropriate, use bullet points to highlight key lists.")
    # simple jargon check
    jargon = re.findall(r'\b(synergy|leverage|paradigm|robust|granular|scalable)\b', text, re.IGNORECASE)
    if len(set(jargon)) >= 2:
        suggestions.append("Reduce corporate jargon to make writing clearer.")
    # passive voice (very rough)
    passive_hits = re.findall(r'\b(was|were|is|are|be|been|being)\s+\w+ed\b', text, re.IGNORECASE)
    if len(passive_hits) > 5:
        suggestions.append("Heavy passive voice detected; convert some sentences to active voice.")
    # conclude
    if not suggestions:
        suggestions.append("Looks good! Consider adding visuals or examples to enhance engagement.")
    return suggestions
