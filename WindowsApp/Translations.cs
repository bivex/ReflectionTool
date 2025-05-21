using System.Collections.Generic;

namespace WikiReflectionTool
{
    public static class GuiTranslations
    {
        public static Dictionary<string, Dictionary<string, string>> Translations = new Dictionary<string, Dictionary<string, string>>
        {
            {
                "English", new Dictionary<string, string>
                {
                    { "window_title", "Wikipedia Reflection Tool" },
                    { "interface_language_label", "Interface Language:" },
                    { "wikipedia_language_label", "Wikipedia Language:" },
                    { "dark_theme", "🌙 Dark Theme" },
                    { "light_theme", "☀️ Light Theme" },
                    { "summary", "Summary" },
                    { "sections", "Sections" },
                    { "categories", "Categories" },
                    { "new_article", "🔄 New Random Article" },
                    { "fetching", "Fetching article..." },
                    { "error", "Error" },
                    { "error_client_not_initialized", "Wikipedia client not initialized. Please check connection or language." }
                }
            },
            {
                "Ukrainian", new Dictionary<string, string>
                {
                    { "window_title", "Інструмент для рефлексії Вікіпедії" },
                    { "interface_language_label", "Мова інтерфейсу:" },
                    { "wikipedia_language_label", "Мова Вікіпедії:" },
                    { "dark_theme", "🌙 Темна тема" },
                    { "light_theme", "☀️ Світла тема" },
                    { "summary", "Короткий опис" },
                    { "sections", "Розділи" },
                    { "categories", "Категорії" },
                    { "new_article", "🔄 Нова випадкова стаття" },
                    { "fetching", "Отримання статті..." },
                    { "error", "Помилка" },
                    { "error_client_not_initialized", "Клієнт Вікіпедії не ініціалізовано. Перевірте з\'єднання або мову." }
                }
            },
            {
                "German", new Dictionary<string, string>
                {
                    { "window_title", "Wikipedia Reflexions-Tool" },
                    { "interface_language_label", "Interface Sprache:" },
                    { "wikipedia_language_label", "Wikipedia Sprache:" },
                    { "dark_theme", "🌙 Dunkles Design" },
                    { "light_theme", "☀️ Helles Design" },
                    { "summary", "Zusammenfassung" },
                    { "sections", "Abschnitte" },
                    { "categories", "Kategorien" },
                    { "new_article", "🔄 Neuer zufälliger Artikel" },
                    { "fetching", "Artikel wird geladen..." },
                    { "error", "Fehler" },
                    { "error_client_not_initialized", "Wikipedia-Client nicht initialisiert. Bitte überprüfen Sie die Verbindung oder Sprache." }
                }
            },
            {
                "French", new Dictionary<string, string>
                {
                    { "window_title", "Outil de Réflexion Wikipédia" },
                    { "interface_language_label", "Langue de l'interface :" },
                    { "wikipedia_language_label", "Langue Wikipédia :" },
                    { "dark_theme", "🌙 Thème sombre" },
                    { "light_theme", "☀️ Thème clair" },
                    { "summary", "Résumé" },
                    { "sections", "Sections" },
                    { "categories", "Catégories" },
                    { "new_article", "🔄 Nouvel article aléatoire" },
                    { "fetching", "Chargement de l'article..." },
                    { "error", "Erreur" },
                    { "error_client_not_initialized", "Client Wikipédia non initialisé. Veuillez vérifier la connexion ou la langue." }
                }
            },
            {
                "Russian", new Dictionary<string, string>
                {
                    { "window_title", "Инструмент для рефлексии Википедии" },
                    { "interface_language_label", "Язык интерфейса:" },
                    { "wikipedia_language_label", "Язык Википедии:" },
                    { "dark_theme", "🌙 Тёмная тема" },
                    { "light_theme", "☀️ Светлая тема" },
                    { "summary", "Обзор" },
                    { "sections", "Разделы" },
                    { "categories", "Категории" },
                    { "new_article", "🔄 Новая случайная статья" },
                    { "fetching", "Загрузка статьи..." },
                    { "error", "Ошибка" },
                    { "error_client_not_initialized", "Клиент Википедии не инициализирован. Проверьте соединение или язык." }
                }
            },
            {
                "Romani", new Dictionary<string, string> // Assuming Romani translations are similar to English as per original
                {
                    { "window_title", "Wikipedia Reflection Tool" },
                    { "interface_language_label", "Chhib:" },
                    { "wikipedia_language_label", "Wikipedia Chhib:" },
                    { "dark_theme", "🌙 Kali Tema" },
                    { "light_theme", "☀️ Parni Tema" },
                    { "summary", "Agor" },
                    { "sections", "Kotor" },
                    { "categories", "Kategorie" },
                    { "new_article", "🔄 Nevo Ramome Artikli" },
                    { "fetching", "Lel artikli..." },
                    { "error", "Dosh" },
                    { "error_client_not_initialized", "Wikipedia client not initialized. Please check connection or language." }
                }
            }
        };
    }
} 