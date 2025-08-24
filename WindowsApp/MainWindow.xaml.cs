using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net.Http;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using static System.Net.WebUtility; // Use static for WebUtility

namespace WikiReflectionTool
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private string currentGuiLanguage = "English";
        private Dictionary<string, string> currentTranslations;
        private string currentWikiLanguageCode = "en";
        private readonly HttpClient httpClient;
        private string currentArticleUrl;

        private readonly Dictionary<string, string> languageCodes = new Dictionary<string, string>
        {
            { "English", "en" },
            { "Ukrainian", "uk" },
            { "German", "de" },
            { "French", "fr" },
            { "Spanish", "es" },
            { "Italian", "it" },
            { "Polish", "pl" },
            { "Russian", "ru" },
            { "Japanese", "ja" },
            { "Chinese", "zh" },
            { "Romani", "rm" }
        };

        public MainWindow()
        {
            InitializeComponent();
            httpClient = new HttpClient();
            httpClient.DefaultRequestHeaders.Add("User-Agent", "WikiReflectionToolWPF/1.0");

            PopulateGuiLanguageComboBox();
            PopulateWikiLanguageComboBox();
            UpdateGuiTexts(); // Initial text setup

            // Event handlers
            GuiLanguageComboBox.SelectionChanged += GuiLanguageComboBox_SelectionChanged;
            WikiLanguageComboBox.SelectionChanged += WikiLanguageComboBox_SelectionChanged;
            ThemeButton.Click += ThemeButton_Click;
            FetchButton.Click += FetchButton_Click;
        }

        private async void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            await FetchRandomArticleAsync();
        }

        private void PopulateGuiLanguageComboBox()
        {
            foreach (var lang in GuiTranslations.Translations.Keys)
            {
                GuiLanguageComboBox.Items.Add(lang);
            }
            GuiLanguageComboBox.SelectedItem = currentGuiLanguage;
        }

        private void PopulateWikiLanguageComboBox()
        {
            foreach (var lang in languageCodes.Keys)
            {
                WikiLanguageComboBox.Items.Add(lang);
            }
            WikiLanguageComboBox.SelectedItem = languageCodes.FirstOrDefault(x => x.Value == currentWikiLanguageCode).Key;
        }

        private string T(string key)
        {
            if (currentTranslations != null && currentTranslations.TryGetValue(key, out var text))
            {
                return text;
            }
            if (GuiTranslations.Translations["English"].TryGetValue(key, out var fallbackText))
            {
                return fallbackText;
            }
            return $"[{key}]";
        }

        private void UpdateGuiTexts()
        {
            currentTranslations = GuiTranslations.Translations[currentGuiLanguage];
            this.Title = T("window_title");
            GuiLanguageLabel.Content = T("interface_language_label");
            WikiLanguageLabel.Content = T("wikipedia_language_label");
            ThemeButton.Content = (Application.Current as App).IsDarkTheme() ? T("light_theme") : T("dark_theme");
            FetchButton.Content = T("new_article");
            SummaryLabel.Content = T("summary");
            SectionsLabel.Content = T("sections");
            CategoriesLabel.Content = T("categories");
        }

        private void GuiLanguageComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (GuiLanguageComboBox.SelectedItem != null)
            {
                currentGuiLanguage = GuiLanguageComboBox.SelectedItem.ToString();
                UpdateGuiTexts();
            }
        }

        private async void WikiLanguageComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (WikiLanguageComboBox.SelectedItem != null && languageCodes.ContainsKey(WikiLanguageComboBox.SelectedItem.ToString()))
            {
                currentWikiLanguageCode = languageCodes[WikiLanguageComboBox.SelectedItem.ToString()];
                await FetchRandomArticleAsync();
            }
        }

        private void ThemeButton_Click(object sender, RoutedEventArgs e)
        {
            (Application.Current as App).ToggleTheme();
            ThemeButton.Content = (Application.Current as App).IsDarkTheme() ? T("light_theme") : T("dark_theme");
        }

        private async void FetchButton_Click(object sender, RoutedEventArgs e)
        {
            await FetchRandomArticleAsync();
        }

        private void TitleTextBlock_MouseDown(object sender, MouseButtonEventArgs e)
        {
            if (!string.IsNullOrEmpty(currentArticleUrl))
            {
                try
                {
                    Process.Start(new ProcessStartInfo(currentArticleUrl) { UseShellExecute = true });
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Could not open URL: {ex.Message}", T("error"), MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }

        private async Task<string> GetRandomArticleTitleAsync()
        {
            try
            {
                string apiUrl = $"https://{currentWikiLanguageCode}.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=json";
                HttpResponseMessage response = await httpClient.GetAsync(apiUrl);
                response.EnsureSuccessStatusCode();

                string jsonResponse = await response.Content.ReadAsStringAsync();
                using (JsonDocument doc = JsonDocument.Parse(jsonResponse))
                {
                    JsonElement root = doc.RootElement;
                    JsonElement query = root.GetProperty("query");
                    JsonElement random = query.GetProperty("random");
                    JsonElement randomArticle = random[0];
                    return randomArticle.GetProperty("title").GetString();
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error fetching random article title: {ex.Message}");
                DisplayError($"Error fetching random title: {ex.Message}");
                return null;
            }
        }

        private async Task FetchRandomArticleAsync()
        {
            TitleTextBlock.Text = T("fetching");
            SummaryTextBox.Clear();
            SectionsTextBox.Clear();
            CategoriesTextBox.Clear();
            SectionsLabel.Visibility = Visibility.Collapsed;
            SectionsTextBox.Visibility = Visibility.Collapsed;
            CategoriesLabel.Visibility = Visibility.Collapsed;
            CategoriesTextBox.Visibility = Visibility.Collapsed;
            FetchButton.IsEnabled = false;
            currentArticleUrl = null;

            try
            {
                string randomTitle = await GetRandomArticleTitleAsync();

                if (!string.IsNullOrEmpty(randomTitle))
                {
                    await FetchArticleContentAsync(randomTitle);
                }
            }
            catch (Exception ex)
            {
                DisplayError($"Error fetching article content: {ex.Message}");
            }
            finally
            {
                FetchButton.IsEnabled = true;
            }
        }

        private async Task FetchArticleContentAsync(string title)
        {
            try
            {
                // URL encode the title
                string encodedTitle = UrlEncode(title);

                // Set the article URL for opening in browser
                currentArticleUrl = $"https://{currentWikiLanguageCode}.wikipedia.org/wiki/{encodedTitle.Replace("+", "_")}";

                // API URL for fetching article content with extract (summary), categories, and sections
                string apiUrl = $"https://{currentWikiLanguageCode}.wikipedia.org/w/api.php?" +
                    $"action=query&prop=extracts|categories|sections&titles={encodedTitle}" +
                    "&explaintext=1&clshow=!hidden&format=json";

                HttpResponseMessage response = await httpClient.GetAsync(apiUrl);
                response.EnsureSuccessStatusCode();

                string jsonResponse = await response.Content.ReadAsStringAsync();
                DisplayArticleFromJson(jsonResponse, title);
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error fetching article content: {ex.Message}");
                DisplayError($"Error fetching article content for '{title}': {ex.Message}");
            }
        }

        private void DisplayArticleFromJson(string jsonResponse, string title)
        {
            try
            {
                using (JsonDocument doc = JsonDocument.Parse(jsonResponse))
                {
                    JsonElement root = doc.RootElement;
                    JsonElement query = root.GetProperty("query");
                    JsonElement pages = query.GetProperty("pages");

                    // Get the first (and only) page
                    string pageId = pages.EnumerateObject().First().Name;
                    JsonElement page = pages.GetProperty(pageId);

                    // Set the title
                    TitleTextBlock.Text = page.GetProperty("title").GetString();

                    // Display the extract (summary)
                    if (page.TryGetProperty("extract", out JsonElement extract))
                    {
                        SummaryTextBox.Text = FormatTextForReading(extract.GetString());
                    }
                    else
                    {
                        SummaryTextBox.Text = "No summary available.";
                    }

                    // Display sections if available
                    if (page.TryGetProperty("sections", out JsonElement sections) && sections.GetArrayLength() > 0)
                    {
                        SectionsLabel.Visibility = Visibility.Visible;
                        SectionsTextBox.Visibility = Visibility.Visible;

                        string sectionsText = "";
                        int sectionCounter = 1;
                        foreach (JsonElement section in sections.EnumerateArray())
                        {
                            if (section.TryGetProperty("line", out JsonElement line) &&
                                section.TryGetProperty("level", out JsonElement level))
                            {
                                int levelNum = level.GetInt32();
                                if (levelNum == 2) // Main sections
                                {
                                    sectionsText += $"\n{sectionCounter}. {line.GetString()}\n";
                                    sectionsText += new string('-', Math.Min(line.GetString().Length + 3, 50)) + "\n";
                                    sectionCounter++;
                                }
                                else if (levelNum > 2) // Sub-sections
                                {
                                    string indent = new string(' ', (levelNum - 2) * 2);
                                    sectionsText += $"{indent}• {line.GetString()}\n";
                                }
                            }
                        }
                        SectionsTextBox.Text = sectionsText;
                    }
                    else
                    {
                        SectionsLabel.Visibility = Visibility.Collapsed;
                        SectionsTextBox.Visibility = Visibility.Collapsed;
                    }

                    // Display categories if available
                    if (page.TryGetProperty("categories", out JsonElement categories) && categories.GetArrayLength() > 0)
                    {
                        CategoriesLabel.Visibility = Visibility.Visible;
                        CategoriesTextBox.Visibility = Visibility.Visible;

                        string categoriesText = "";
                        var categoryList = new List<string>();
                        foreach (JsonElement category in categories.EnumerateArray())
                        {
                            if (category.TryGetProperty("title", out JsonElement categoryTitle))
                            {
                                string catName = categoryTitle.GetString().Replace("Category:", "").Trim();
                                if (!string.IsNullOrEmpty(catName))
                                {
                                    categoryList.Add(catName);
                                }
                            }
                        }
                        
                        if (categoryList.Count > 0)
                        {
                            categoriesText = "📂 Категории:\n\n";
                            for (int i = 0; i < categoryList.Count; i++)
                            {
                                categoriesText += $"  {i + 1}. {categoryList[i]}\n";
                            }
                        }
                        CategoriesTextBox.Text = categoriesText;
                    }
                    else
                    {
                        CategoriesLabel.Visibility = Visibility.Collapsed;
                        CategoriesTextBox.Visibility = Visibility.Collapsed;
                    }
                }
            }
            catch (Exception ex)
            {
                DisplayError($"Error parsing article data: {ex.Message}");
            }
        }

        private string FormatTextForReading(string text)
        {
            if (string.IsNullOrEmpty(text))
                return text;

            // Split into sentences and add proper spacing
            var sentences = text.Split(new char[] { '.', '!', '?' }, StringSplitOptions.RemoveEmptyEntries);
            var formattedText = new System.Text.StringBuilder();

            for (int i = 0; i < sentences.Length; i++)
            {
                string sentence = sentences[i].Trim();
                if (!string.IsNullOrEmpty(sentence))
                {
                    // Add sentence with proper punctuation
                    char lastChar = text.Substring(text.IndexOf(sentence) + sentence.Length).FirstOrDefault();
                    if (".!?".Contains(lastChar))
                    {
                        sentence += lastChar;
                    }
                    
                    formattedText.AppendLine(sentence);
                    
                    // Add extra line after every 2-3 sentences for readability
                    if ((i + 1) % 3 == 0 && i < sentences.Length - 1)
                    {
                        formattedText.AppendLine();
                    }
                }
            }

            return formattedText.ToString().Trim();
        }

        private void DisplayError(string message)
        {
            TitleTextBlock.Text = T("error");
            SummaryTextBox.Text = message;
            SectionsLabel.Visibility = Visibility.Collapsed;
            SectionsTextBox.Visibility = Visibility.Collapsed;
            CategoriesLabel.Visibility = Visibility.Collapsed;
            CategoriesTextBox.Visibility = Visibility.Collapsed;
            currentArticleUrl = null;
            FetchButton.IsEnabled = true;
        }
    }
} 