using System;
using System.Windows;

namespace WikiReflectionTool
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        private bool isDarkTheme = false;

        public void ToggleTheme()
        {
            isDarkTheme = !isDarkTheme;
            var themeDictionary = new ResourceDictionary();

            if (isDarkTheme)
            {
                themeDictionary.Source = new Uri("DarkTheme.xaml", UriKind.Relative);
            }
            else
            {
                themeDictionary.Source = new Uri("LightTheme.xaml", UriKind.Relative);
            }

            // Clear existing merged dictionaries and add the new one
            Current.Resources.MergedDictionaries.Clear();
            Current.Resources.MergedDictionaries.Add(themeDictionary);
        }

        public bool IsDarkTheme()
        {
            return isDarkTheme;
        }
    }
} 