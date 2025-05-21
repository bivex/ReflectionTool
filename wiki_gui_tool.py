import sys
import wikipediaapi
import requests
import webbrowser
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QTextBrowser,
    QHBoxLayout, QComboBox, QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QCursor, QPalette, QColor

# GUI translations
GUI_TRANSLATIONS = {
    "English": {
        "window_title": "Wikipedia Reflection Tool",
        "language_label": "Language:",
        "dark_theme": "🌙 Dark Theme",
        "light_theme": "☀️ Light Theme",
        "summary": "Summary",
        "sections": "Sections",
        "categories": "Categories",
        "new_article": "🔄 New Random Article",
        "fetching": "Fetching article...",
        "error": "Error"
    },
    "Ukrainian": {
        "window_title": "Інструмент для рефлексії Вікіпедії",
        "language_label": "Мова:",
        "dark_theme": "🌙 Темна тема",
        "light_theme": "☀️ Світла тема",
        "summary": "Короткий опис",
        "sections": "Розділи",
        "categories": "Категорії",
        "new_article": "🔄 Нова випадкова стаття",
        "fetching": "Отримання статті...",
        "error": "Помилка"
    },
    "German": {
        "window_title": "Wikipedia Reflexions-Tool",
        "language_label": "Sprache:",
        "dark_theme": "🌙 Dunkles Design",
        "light_theme": "☀️ Helles Design",
        "summary": "Zusammenfassung",
        "sections": "Abschnitte",
        "categories": "Kategorien",
        "new_article": "🔄 Neuer zufälliger Artikel",
        "fetching": "Artikel wird geladen...",
        "error": "Fehler"
    },
    "French": {
        "window_title": "Outil de Réflexion Wikipédia",
        "language_label": "Langue:",
        "dark_theme": "🌙 Thème sombre",
        "light_theme": "☀️ Thème clair",
        "summary": "Résumé",
        "sections": "Sections",
        "categories": "Catégories",
        "new_article": "🔄 Nouvel article aléatoire",
        "fetching": "Chargement de l'article...",
        "error": "Erreur"
    },
    "Russian": {
        "window_title": "Инструмент для рефлексии Википедии",
        "language_label": "Язык:",
        "dark_theme": "🌙 Тёмная тема",
        "light_theme": "☀️ Светлая тема",
        "summary": "Обзор",
        "sections": "Разделы",
        "categories": "Категории",
        "new_article": "🔄 Новая случайная статья",
        "fetching": "Загрузка статьи...",
        "error": "Ошибка"
    },
    "Romani": {
        "window_title": "Wikipedia Reflection Tool",
        "language_label": "Language:",
        "dark_theme": "🌙 Dark Theme",
        "light_theme": "☀️ Light Theme",
        "summary": "Summary",
        "sections": "Sections",
        "categories": "Categories",
        "new_article": "🔄 New Random Article",
        "fetching": "Fetching article...",
        "error": "Error"
    }
}

# Reuse the function to get a random article title
def get_random_article_title(language='en'):
    url = f"https://{language}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "random",
        "rnnamespace": 0, # Only get articles (namespace 0)
        "rnlimit": 1,
        "format": "json"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        title = data['query']['random'][0]['title']
        return title
    except requests.exceptions.RequestException as e:
        print(f"Error fetching random article title: {e}")
        return None

# Thread to fetch Wikipedia article data to avoid freezing the GUI
class ArticleFetcher(QThread):
    article_fetched = pyqtSignal(str, str, list, dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, title, user_agent, language):
        super().__init__()
        self.title = title
        self.user_agent = user_agent
        self.language = language

    def run(self):
        try:
            wiki_wiki = wikipediaapi.Wikipedia(
                user_agent=self.user_agent,
                language=self.language,
                extract_format=wikipediaapi.ExtractFormat.WIKI
            )
            page = wiki_wiki.page(self.title)

            if page.exists():
                summary = page.summary
                sections = page.sections # Get sections
                categories = page.categories # Get categories
                self.article_fetched.emit(page.title, summary, sections, categories)
            else:
                self.error_occurred.emit(f"Article '{self.title}' not found.")
        except Exception as e:
            self.error_occurred.emit(f"Error fetching article content: {e}")


class WikiReflectionTool(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize GUI language
        self.gui_language = "English"
        self.translations = GUI_TRANSLATIONS[self.gui_language]

        self.setWindowTitle(self.translations["window_title"])
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
            }
            QTextBrowser {
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
                padding: 10px;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Top controls layout
        controls_layout = QHBoxLayout()
        
        # GUI Language selector
        gui_language_label = QLabel("Interface Language:")
        gui_language_label.setStyleSheet("font-weight: bold;")
        self.gui_language_combo = QComboBox()
        self.gui_language_combo.addItems(GUI_TRANSLATIONS.keys())
        self.gui_language_combo.currentTextChanged.connect(self.change_gui_language)
        self.gui_language_combo.setMinimumWidth(150)
        
        # Wikipedia Language selector
        wiki_language_label = QLabel("Wikipedia Language:")
        wiki_language_label.setStyleSheet("font-weight: bold;")
        self.language_combo = QComboBox()
        self.language_codes = {
            "English": "en",
            "Ukrainian": "uk",
            "German": "de",
            "French": "fr",
            "Spanish": "es",
            "Italian": "it",
            "Polish": "pl",
            "Russian": "ru",
            "Japanese": "ja",
            "Chinese": "zh",
            "Romani": "rm"
        }
        self.language_combo.addItems(self.language_codes.keys())
        self.language_combo.currentTextChanged.connect(self.change_language)
        self.language_combo.setMinimumWidth(150)
        
        # Theme toggle
        self.theme_button = QPushButton(self.translations["dark_theme"])
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setFixedWidth(120)
        
        # Add widgets to controls layout
        controls_layout.addWidget(gui_language_label)
        controls_layout.addWidget(self.gui_language_combo)
        controls_layout.addWidget(wiki_language_label)
        controls_layout.addWidget(self.language_combo)
        controls_layout.addStretch()
        self.fetch_button = QPushButton(self.translations["new_article"])
        self.fetch_button.clicked.connect(self.fetch_random_article)
        self.fetch_button.setMinimumWidth(200)
        controls_layout.addWidget(self.fetch_button)
        controls_layout.addStretch()
        controls_layout.addWidget(self.theme_button)
        
        self.main_layout.addLayout(controls_layout)

        # Article container with shadow effect
        article_container = QFrame()
        article_container.setStyleSheet("""
        """)
        article_layout = QVBoxLayout(article_container)
        article_layout.setSpacing(15)

        # Title with improved styling
        self.title_label = QLabel(self.translations["fetching"])
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
            QLabel:hover {
                color: #3498db;
            }
        """)
        self.title_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.title_label.mousePressEvent = self.open_wiki_article
        article_layout.addWidget(self.title_label)

        # Summary with improved styling
        summary_label = QLabel(self.translations["summary"])
        summary_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        article_layout.addWidget(summary_label)
        
        self.summary_text = QTextBrowser()
        self.summary_text.setStyleSheet("""
            QTextBrowser {
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        article_layout.addWidget(self.summary_text)

        # Sections with improved styling
        self.sections_label = QLabel(self.translations["sections"])
        self.sections_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        self.sections_label.setVisible(False)
        article_layout.addWidget(self.sections_label)

        self.sections_text = QTextBrowser()
        self.sections_text.setStyleSheet("""
            QTextBrowser {
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        self.sections_text.setVisible(False)
        article_layout.addWidget(self.sections_text)

        # Categories with improved styling
        self.categories_label = QLabel(self.translations["categories"])
        self.categories_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        self.categories_label.setVisible(False)
        article_layout.addWidget(self.categories_label)

        self.categories_text = QTextBrowser()
        self.categories_text.setStyleSheet("""
            QTextBrowser {
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        self.categories_text.setVisible(False)
        article_layout.addWidget(self.categories_text)

        # Add article container to main layout
        self.main_layout.addWidget(article_container)

        # Initialize state
        self.user_agent = 'RandomWikiReflectionToolGUI (YourProjectName <your_email@example.com>)'
        self.language = 'en'
        self.current_article_url = None
        self.is_dark_theme = False

        # Fetch first article
        self.fetch_random_article()

    def change_gui_language(self, language):
        """Change the GUI language"""
        self.gui_language = language
        self.translations = GUI_TRANSLATIONS[language]
        
        # Update all GUI elements with new translations
        self.setWindowTitle(self.translations["window_title"])
        self.theme_button.setText(self.translations["dark_theme"] if not self.is_dark_theme else self.translations["light_theme"])
        self.title_label.setText(self.translations["fetching"])
        self.sections_label.setText(self.translations["sections"])
        self.categories_label.setText(self.translations["categories"])
        self.fetch_button.setText(self.translations["new_article"])

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        if self.is_dark_theme:
            # Apply dark theme stylesheet
            dark_stylesheet = """
                /* --- General Styles --- */
                QMainWindow {
                    background-color: #121212; /* Deep dark background */
                    color: #e0e0e0; /* Light gray text for general elements */
                }

                QLabel {
                    color: #e0e0e0; /* Consistent light gray for labels */
                }

                QPushButton {
                    background-color: #0d6efd; /* Vibrant blue */
                    color: #ffffff; /* White text on buttons */
                    border: none;
                    padding: 12px 24px; /* Increased padding for larger buttons */
                    border-radius: 6px;
                    font-size: 15px; /* Slightly larger font */
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0b5ed7; /* Darker blue on hover */
                }
                QPushButton:pressed {
                    background-color: #0a58ca; /* Even darker blue when pressed */
                }
                QPushButton:disabled {
                    background-color: #2d2d2d; /* Dark gray for disabled */
                    color: #808080; /* Lighter gray text for disabled */
                }

                /* --- ComboBox Styles --- */
                QComboBox {
                    min-width: 150px;
                    padding: 8px; /* Padding inside the combobox */
                    border: 1px solid #3d3d3d; /* Subtle dark border */
                    border-radius: 4px; /* Slightly smaller radius */
                    background-color: #1e1e1e; /* Dark background */
                    color: #e0e0e0; /* Light gray text */
                }
                QComboBox:hover {
                    border-color: #0d6efd; /* Highlight border on hover */
                }
                QComboBox::drop-down {
                    border: none; /* No border for dropdown arrow area */
                }
                QComboBox::down-arrow {
                    image: none; /* Hide default arrow */
                    border: none;
                }

                QComboBox QAbstractItemView {
                    background-color: #1e1e1e; /* Dark background for dropdown list */
                    color: #e0e0e0; /* Light gray text for list items */
                    selection-background-color: #0d6efd; /* Blue selection background */
                    selection-color: #ffffff; /* White text on selection */
                    border: 1px solid #3d3d3d; /* Subtle border for the list */
                    font-size: 14px;
                }

                /* --- Article Content Area Styles (Frame and Text Browsers) --- */
                QFrame {
                    background-color: #1a1a1a; /* Slightly lighter dark background for content frame */
                    border-radius: 8px; /* Rounded corners for content frame */
                    border: 1px solid #3d3d3d; /* Subtle border for the frame */
                }

                QTextBrowser {
                    background-color: #1a1a1a; /* Match frame background */
                    color: #e0e0e0; /* Light gray text */
                    border: none; /* No border for text browsers within the frame */
                    padding: 10px; /* Internal padding */
                }

                /* --- Scrollbar Styles --- */
                QScrollBar:vertical {
                    border: none;
                    background: #2d2d2d; /* Darker background for scrollbar area */
                    width: 12px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: #555555; /* Medium gray handle */
                    border-radius: 6px;
                    min-height: 30px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #0d6efd; /* Blue handle on hover */
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                QScrollBar:horizontal {
                    border: none;
                    background: #2d2d2d; /* Darker background for scrollbar area */
                    height: 12px;
                    margin: 0px;
                }
                QScrollBar::handle:horizontal {
                    background: #555555; /* Medium gray handle */
                    border-radius: 6px;
                    min-width: 30px;
                }
                QScrollBar::handle:horizontal:hover {
                    background: #0d6efd; /* Blue handle on hover */
                }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                    width: 0px;
                }
            """
            self.setStyleSheet(dark_stylesheet)
            self.update() # Force a repaint after changing stylesheet

        else:
            # Apply light theme stylesheet
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f8f9fa;
                }
                QLabel {
                    color: #212529;
                }
                QPushButton {
                    background-color: #0d6efd;
                    color: #ffffff;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0b5ed7;
                }
                QPushButton:pressed {
                    background-color: #0a58ca;
                }
                QPushButton:disabled {
                    background-color: #e9ecef;
                    color: #6c757d;
                }
                /* Styling for QComboBox in light theme */
                QComboBox {
                    padding: 8px;
                    border: 2px solid #ced4da;
                    border-radius: 6px;
                    background-color: #ffffff;
                    color: #212529;
                    min-width: 150px;
                }
                QComboBox:hover {
                    border-color: #0d6efd;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border: none;
                }
                 QComboBox QAbstractItemView {
                     background-color: #ffffff;
                     color: #212529;
                     selection-background-color: #0d6efd;
                     selection-color: #ffffff;
                     border: 1px solid #ced4da;
                     font-size: 14px;
                 }
                QTextBrowser {
                    border: 2px solid #ced4da;
                    border-radius: 8px;
                    background-color: #ffffff;
                    color: #212529;
                    padding: 15px;
                    font-size: 14px;
                    line-height: 1.6;
                }
                QTextBrowser:hover {
                    border-color: #0d6efd;
                }
                QFrame {
                    background-color: #ffffff;
                    border-radius: 12px;
                    border: 2px solid #ced4da;
                }
                QFrame:hover {
                    border-color: #0d6efd;
                }
                QScrollBar:vertical {
                    border: none;
                    background-color: #f8f9fa;
                    width: 12px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background-color: #ced4da;
                    border-radius: 6px;
                    min-height: 30px;
                }
                QScrollBar::handle:vertical:hover {
                    background-color: #0d6efd;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                QScrollBar:horizontal {
                    border: none;
                    background-color: #f8f9fa;
                    height: 12px;
                    margin: 0px;
                }
                QScrollBar::handle:horizontal {
                    background-color: #ced4da;
                    border-radius: 6px;
                    min-width: 30px;
                }
                QScrollBar::handle:horizontal:hover {
                    background-color: #0d6efd;
                }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                    width: 0px;
                }
            """)
            self.theme_button.setText(self.translations["dark_theme"])

            # Reset palette for QComboBoxes in light theme to default
            default_palette = QApplication.instance().palette()
            self.language_combo.setPalette(default_palette)
            self.gui_language_combo.setPalette(default_palette)

            # Clear specific stylesheet for QComboBoxes in light theme
            self.language_combo.setStyleSheet("")
            self.gui_language_combo.setStyleSheet("")

    def change_language(self, language_name):
        """Change the Wikipedia language and fetch a new article"""
        self.language = self.language_codes[language_name]
        self.fetch_random_article()

    def open_wiki_article(self, event):
        if self.current_article_url:
            webbrowser.open(self.current_article_url)

    def fetch_random_article(self):
        self.title_label.setText("Fetching article...")
        self.summary_text.clear()
        self.sections_text.clear()
        self.categories_text.clear()
        self.sections_label.setVisible(False)
        self.sections_text.setVisible(False)
        self.categories_label.setVisible(False)
        self.categories_text.clear()
        self.fetch_button.setEnabled(False)  # Disable button while fetching

        random_title = get_random_article_title(self.language)

        if random_title:
            # Use a thread to fetch the article data
            self.fetcher_thread = ArticleFetcher(random_title, self.user_agent, self.language)
            self.fetcher_thread.article_fetched.connect(self.display_article)
            self.fetcher_thread.error_occurred.connect(self.display_error)
            self.fetcher_thread.start()
        else:
            self.display_error("Could not retrieve a random article title.")

    def display_article(self, title, summary, sections, categories):
        self.title_label.setText(title)
        self.summary_text.setText(summary)

        # Create and store the Wikipedia URL
        self.current_article_url = f"https://{self.language}.wikipedia.org/wiki/{title.replace(' ', '_')}"

        # Display sections
        if sections:
            self.sections_label.setVisible(True)
            self.sections_text.setVisible(True)
            
            # Create a list to store HTML content
            sections_content = []
            
            def build_sections_html(secs, level=0):
                for s in secs:
                    indent = "&nbsp;" * level * 4  # Use non-breaking spaces for indentation
                    sections_content.append(f"<h{min(level + 2, 6)}>{indent}{s.title}</h{min(level + 2, 6)}>")
                    # Limit text and add paragraph tags for formatting
                    sections_content.append(f"<p>{indent}{s.text[:500]}...</p>")
                    if s.sections:
                        build_sections_html(s.sections, level + 1)
            
            build_sections_html(sections)
            # Join all HTML content with newlines
            self.sections_text.setHtml("\n".join(sections_content))

        # Display categories
        if categories:
            self.categories_label.setVisible(True)
            self.categories_text.setVisible(True)
            categories_text = ""
            for category_title in sorted(categories.keys()):
                 categories_text += f"- {category_title}\n"
            self.categories_text.setText(categories_text)

        self.fetch_button.setEnabled(True)  # Re-enable button

    def display_error(self, message):
        self.title_label.setText("Error")
        self.summary_text.setText(message)
        self.sections_label.setVisible(False)
        self.sections_text.setVisible(False)
        self.categories_label.setVisible(False)
        self.categories_text.setVisible(False)
        self.fetch_button.setEnabled(True) # Re-enable button


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WikiReflectionTool()
    main_window.show()
    sys.exit(app.exec()) 