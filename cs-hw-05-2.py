import requests
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt


def fetch_text(url):
    """Завантажує текст з заданої URL."""
    response = requests.get(url)
    response.raise_for_status()  # Перевірка на помилки HTTP
    return response.text


def map_function(text):
    words = re.findall(r'\w+', text.lower())
    return [(word, 1) for word in words]


def map_reduce(text):
    """Виконує map і reduce кроки для тексту."""
    with ThreadPoolExecutor() as executor:
        parts = [text[i:i+5000] for i in range(0, len(text), 5000)]
        # Map крок
        mapped = executor.map(map_function, parts)
        # Збираємо всі результати в один список
        combined = [item for sublist in mapped for item in sublist]
        # Reduce крок
        reduced = reduce_function(combined)
    return reduced


def reduce_function(mapped_values):
    # Створюємо єдиний Counter для усіх тюплів
    counter = Counter()
    for word, count in mapped_values:
        counter[word] += count
    return counter


def visualize_selected_words(counter, selected_words):
    filtered_counts = {word: count for word,
                       count in counter.items() if word in selected_words}
    words, counts = zip(*filtered_counts.items())
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts, color='blue')
    plt.xlabel('Слова')
    plt.ylabel('Частота')
    plt.title('10 найбільш вживаних слів')
    plt.xticks(rotation=45)
    plt.ylim(0, max(counts) + 50)
    plt.show()


def main(url, selected_words):
    text = fetch_text(url)
    word_count = map_reduce(text)
    visualize_selected_words(word_count, selected_words)


if __name__ == '__main__':
    url = 'https://gutenberg.net.au/ebooks01/0100021.txt'
    selected_words = ['was', 'done', 'of', 'is',
                      'love', 'good', 'the', 'and', 'had', 'it']  # Слова для візуалізації
    main(url, selected_words)
