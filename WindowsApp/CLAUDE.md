# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a WPF (.NET 6) desktop application called "Wikipedia Reflection Tool" that fetches random Wikipedia articles and displays their content with internationalization support and theme switching capabilities.

## Build and Run Commands

```bash
# Build the project
dotnet build

# Run the application
dotnet run

# Build for release
dotnet build --configuration Release
```

## Architecture

### Core Components

- **MainWindow.xaml/MainWindow.xaml.cs** - Main application window with Wikipedia API integration
- **App.xaml/App.xaml.cs** - Application entry point with theme management system
- **Translations.cs** - Multi-language support with translations for English, Ukrainian, German, French, Russian, and Romani
- **DarkTheme.xaml/LightTheme.xaml** - Theme resource dictionaries for styling

### Key Features

1. **Wikipedia API Integration**: Fetches random articles from different Wikipedia language editions using REST API
2. **Multi-language Support**: Interface available in 6 languages with translation system via GuiTranslations class
3. **Dynamic Theming**: Runtime switching between light and dark themes via App.ToggleTheme()
4. **Article Display**: Shows article title, summary/extract, sections hierarchy, and categories

### HTTP Client Architecture

The application uses a single HttpClient instance (`httpClient`) initialized in MainWindow constructor with User-Agent header. All Wikipedia API calls go through this client with proper URL encoding and JSON parsing.

### Theme System

Themes are implemented using WPF ResourceDictionaries that are dynamically swapped at runtime. The App class maintains theme state and provides ToggleTheme() and IsDarkTheme() methods.

### Translation System

The T(string key) method provides localized strings with English fallback. Translations are stored in nested dictionaries in the GuiTranslations static class.

## Development Notes

- Target framework: .NET 6 Windows with WPF
- Dependencies: System.Text.Json for API response parsing
- Wikipedia API endpoints use action=query with various props (extracts, categories, sections)
- Article URLs are constructed for browser opening functionality
- Error handling includes DisplayError() method for user feedback